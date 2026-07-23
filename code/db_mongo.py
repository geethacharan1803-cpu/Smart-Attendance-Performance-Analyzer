"""
================================================================================
DB_MONGO.PY — MongoDB Database Abstraction Layer
JNTUK R23 B.Tech AI & Data Science — Project 17 (V2 + MongoDB)
================================================================================
Core database module using PyMongo providing:
  - Singleton connection management with graceful fallback
  - Student CRUD: bulk seed from CSV, fetch all/one, update fields
  - Daily Attendance CRUD: save/fetch per-day records, student history
  - ML Results CRUD: persist model run metadata and prediction snapshots
  - CSV → MongoDB migration utility

Collections:
  - students          — 80 student documents with nested marks/attendance
  - daily_attendance  — per-day attendance records for the full class
  - ml_results        — model run snapshots with predictions
================================================================================
"""

import datetime
import pandas as pd
import numpy as np
import streamlit as st

from pymongo import MongoClient
from pymongo.errors import (
    ConnectionFailure, ServerSelectionTimeoutError, OperationFailure
)

from config import MONGO_URI, MONGO_DB_NAME, MONGO_TIMEOUT_MS


# ==============================================================================
# CONNECTION MANAGEMENT (Singleton Pattern)
# ==============================================================================

_client_cache = {"client": None, "checked": False, "available": False}


def get_mongo_client() -> MongoClient | None:
    """
    Returns a cached MongoClient singleton.
    Creates the connection on first call; reuses it afterward.
    Returns None if connection fails.
    """
    if _client_cache["client"] is not None:
        return _client_cache["client"]

    try:
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=MONGO_TIMEOUT_MS,
            connectTimeoutMS=MONGO_TIMEOUT_MS,
            socketTimeoutMS=5000,
        )
        # Force a connection check — this will raise if server is unreachable
        client.admin.command("ping")
        _client_cache["client"] = client
        _client_cache["available"] = True
        _client_cache["checked"] = True
        return client
    except (ConnectionFailure, ServerSelectionTimeoutError, Exception):
        _client_cache["client"] = None
        _client_cache["available"] = False
        _client_cache["checked"] = True
        return None


def get_database():
    """
    Returns the project database object, or None if unavailable.
    """
    client = get_mongo_client()
    if client is None:
        return None
    return client[MONGO_DB_NAME]


def is_mongo_available() -> bool:
    """
    Checks whether MongoDB is reachable.
    Uses cached result after the first check to avoid repeated timeouts.
    """
    if _client_cache["checked"]:
        return _client_cache["available"]
    get_mongo_client()
    return _client_cache["available"]


def get_connection_info() -> dict:
    """
    Returns a summary dict about the current MongoDB connection status.
    Useful for sidebar status indicators.
    """
    available = is_mongo_available()
    db = get_database()

    info = {
        "available": available,
        "uri": MONGO_URI[:40] + "..." if len(MONGO_URI) > 40 else MONGO_URI,
        "db_name": MONGO_DB_NAME,
        "collections": [],
        "student_count": 0,
        "attendance_days": 0,
    }

    if available and db is not None:
        try:
            info["collections"] = db.list_collection_names()
            if "students" in info["collections"]:
                info["student_count"] = db["students"].count_documents({})
            if "daily_attendance" in info["collections"]:
                info["attendance_days"] = db["daily_attendance"].count_documents({})
        except Exception:
            pass

    return info


# ==============================================================================
# STUDENT CRUD OPERATIONS
# ==============================================================================

def seed_students_from_dataframe(df: pd.DataFrame) -> tuple[int, str]:
    """
    Bulk-inserts (or upserts) all students from a pandas DataFrame into
    the 'students' collection. Each row becomes one MongoDB document with
    nested sub-documents for attendance, marks, and semesters.

    Args:
        df: Student DataFrame (from CSV or enriched V2 dataset).

    Returns:
        tuple: (count of upserted documents, status message)
    """
    db = get_database()
    if db is None:
        return 0, "MongoDB is not available."

    collection = db["students"]
    upserted = 0

    # Subject column mapping for nested document
    subject_map = {
        'LA_Calculus_Marks': 'LA_Calculus',
        'C_Programming_Marks': 'C_Programming',
        'Python_Programming_Marks': 'Python_Programming',
        'Data_Structures_Marks': 'Data_Structures',
        'Eng_Physics_Marks': 'Eng_Physics',
        'BEEE_Marks': 'BEEE',
        'IT_Workshop_Marks': 'IT_Workshop',
    }

    for _, row in df.iterrows():
        doc = {
            "_id": row["Roll_No"],
            "roll_no": row["Roll_No"],
            "student_name": row["Student_Name"],
            "gender": row["Gender"],
            "attendance": {
                "sem1_1_pct": _safe_float(row.get("Sem1_1_Attendance_Pct")),
                "sem1_2_pct": _safe_float(row.get("Sem1_2_Attendance_Pct")),
                "overall_pct": _safe_float(row.get("Overall_Attendance_Pct")),
                "lab_pct": _safe_float(row.get("Lab_Attendance_Pct")),
            },
            "marks": {
                "subjects": {
                    v: _safe_float(row.get(k))
                    for k, v in subject_map.items()
                },
                "sem1_1": {
                    "mid1": _safe_float(row.get("Sem1_1_Mid1")),
                    "mid2": _safe_float(row.get("Sem1_1_Mid2")),
                    "internal": _safe_float(row.get("Sem1_1_Internal")),
                    "external": _safe_float(row.get("Sem1_1_External")),
                    "total": _safe_float(row.get("Sem1_1_Total")),
                },
                "sem1_2": {
                    "mid1": _safe_float(row.get("Sem1_2_Mid1")),
                    "mid2": _safe_float(row.get("Sem1_2_Mid2")),
                    "internal": _safe_float(row.get("Sem1_2_Internal")),
                    "external": _safe_float(row.get("Sem1_2_External")),
                    "total": _safe_float(row.get("Sem1_2_Total")),
                },
            },
            "backlogs": int(row.get("Backlogs", 0)),
            "predictions": {},  # Populated later by ML module
        }

        # Upsert: insert if not exists, update if exists
        collection.replace_one({"_id": row["Roll_No"]}, doc, upsert=True)
        upserted += 1

    return upserted, f"Successfully seeded {upserted} student records into MongoDB."


def get_all_students() -> pd.DataFrame | None:
    """
    Fetches all student documents from MongoDB and flattens them into
    a pandas DataFrame matching the CSV column schema.

    Returns:
        pd.DataFrame if successful, None if MongoDB is unavailable or empty.
    """
    db = get_database()
    if db is None:
        return None

    collection = db["students"]
    docs = list(collection.find({}).sort("roll_no", 1))

    if not docs:
        return None

    # Flatten nested documents back to flat DataFrame columns
    rows = []
    for doc in docs:
        att = doc.get("attendance", {})
        marks = doc.get("marks", {})
        subjects = marks.get("subjects", {})
        sem1_1 = marks.get("sem1_1", {})
        sem1_2 = marks.get("sem1_2", {})
        preds = doc.get("predictions", {})

        row = {
            "Roll_No": doc.get("roll_no", doc["_id"]),
            "Student_Name": doc.get("student_name", ""),
            "Gender": doc.get("gender", ""),
            "Sem1_1_Attendance_Pct": att.get("sem1_1_pct", 0),
            "Sem1_2_Attendance_Pct": att.get("sem1_2_pct", 0),
            "Overall_Attendance_Pct": att.get("overall_pct", 0),
            "LA_Calculus_Marks": subjects.get("LA_Calculus", 0),
            "C_Programming_Marks": subjects.get("C_Programming", 0),
            "Python_Programming_Marks": subjects.get("Python_Programming", 0),
            "Data_Structures_Marks": subjects.get("Data_Structures", 0),
            "Eng_Physics_Marks": subjects.get("Eng_Physics", 0),
            "BEEE_Marks": subjects.get("BEEE", 0),
            "IT_Workshop_Marks": subjects.get("IT_Workshop", 0),
            "Lab_Attendance_Pct": att.get("lab_pct", 0),
            "Backlogs": doc.get("backlogs", 0),
            # V2 enriched columns
            "Sem1_1_Mid1": sem1_1.get("mid1", 0),
            "Sem1_1_Mid2": sem1_1.get("mid2", 0),
            "Sem1_1_Internal": sem1_1.get("internal", 0),
            "Sem1_1_External": sem1_1.get("external", 0),
            "Sem1_1_Total": sem1_1.get("total", 0),
            "Sem1_2_Mid1": sem1_2.get("mid1", 0),
            "Sem1_2_Mid2": sem1_2.get("mid2", 0),
            "Sem1_2_Internal": sem1_2.get("internal", 0),
            "Sem1_2_External": sem1_2.get("external", 0),
            "Sem1_2_Total": sem1_2.get("total", 0),
            "Sem1_2_Predicted_GPA": sem1_2.get("predicted_gpa",
                                                preds.get("predicted_gpa", 0)),
        }
        rows.append(row)

    return pd.DataFrame(rows)


def get_student(roll_no: str) -> dict | None:
    """
    Fetches a single student document by Roll No.
    Returns None if not found or MongoDB unavailable.
    """
    db = get_database()
    if db is None:
        return None
    return db["students"].find_one({"_id": roll_no})


def update_student_field(roll_no: str, field_path: str, value) -> bool:
    """
    Updates a specific field in a student document using MongoDB dot notation.

    Example:
        update_student_field("25A91A4201", "attendance.overall_pct", 72.5)
        update_student_field("25A91A4201", "marks.sem1_1.mid1", 22.5)

    Returns:
        True if the update was acknowledged, False otherwise.
    """
    db = get_database()
    if db is None:
        return False

    result = db["students"].update_one(
        {"_id": roll_no},
        {"$set": {field_path: value}}
    )
    return result.modified_count > 0


def upsert_student_predictions(roll_no: str, predictions: dict) -> bool:
    """
    Writes ML prediction results into the 'predictions' sub-document
    of a specific student.

    Args:
        roll_no: Student roll number (document _id).
        predictions: Dict with keys like predicted_sem1_2_total,
                     predicted_gpa, risk_level, cohort, trajectory.

    Returns:
        True if update succeeded.
    """
    db = get_database()
    if db is None:
        return False

    predictions["updated_at"] = datetime.datetime.utcnow().isoformat()

    result = db["students"].update_one(
        {"_id": roll_no},
        {"$set": {"predictions": predictions}}
    )
    return result.modified_count > 0 or result.matched_count > 0


def bulk_upsert_predictions(prediction_records: list[dict]) -> int:
    """
    Bulk-updates predictions for multiple students.

    Args:
        prediction_records: List of dicts, each with 'roll_no' key
                            and prediction fields.

    Returns:
        Number of documents updated.
    """
    db = get_database()
    if db is None:
        return 0

    updated = 0
    timestamp = datetime.datetime.utcnow().isoformat()

    for record in prediction_records:
        roll_no = record.pop("roll_no", record.pop("Roll_No", None))
        if roll_no is None:
            continue
        record["updated_at"] = timestamp
        result = db["students"].update_one(
            {"_id": roll_no},
            {"$set": {"predictions": record}}
        )
        if result.modified_count > 0 or result.matched_count > 0:
            updated += 1

    return updated


# ==============================================================================
# DAILY ATTENDANCE CRUD OPERATIONS
# ==============================================================================

def save_daily_attendance_db(date_str: str, records: dict) -> bool:
    """
    Upserts a single day's attendance into the 'daily_attendance' collection.

    Args:
        date_str: Date string in "YYYY-MM-DD" format.
        records: Dict mapping Roll_No → {"status": "Present"/"Absent", "remark": "..."}.

    Returns:
        True if operation succeeded.
    """
    db = get_database()
    if db is None:
        return False

    # Build records array and summary
    records_list = []
    present_count = 0
    for roll_no, info in records.items():
        status = info.get("status", "Absent")
        records_list.append({
            "roll_no": roll_no,
            "status": status,
            "remark": info.get("remark", ""),
        })
        if status == "Present":
            present_count += 1

    total = len(records_list)
    absent_count = total - present_count

    doc = {
        "_id": date_str,
        "date": date_str,
        "records": records_list,
        "summary": {
            "total": total,
            "present": present_count,
            "absent": absent_count,
            "attendance_rate": round(
                present_count / total * 100, 1
            ) if total > 0 else 0,
        },
        "created_at": datetime.datetime.utcnow().isoformat(),
    }

    try:
        db["daily_attendance"].replace_one(
            {"_id": date_str}, doc, upsert=True
        )
        return True
    except Exception:
        return False


def get_daily_attendance_db(date_str: str) -> dict:
    """
    Fetches a single day's attendance from MongoDB.

    Args:
        date_str: Date in "YYYY-MM-DD" format.

    Returns:
        Dict mapping Roll_No → {"status": ..., "remark": ...},
        or empty dict if not found / unavailable.
    """
    db = get_database()
    if db is None:
        return {}

    doc = db["daily_attendance"].find_one({"_id": date_str})
    if doc is None:
        return {}

    # Convert records array back to dict format (for compatibility with
    # existing admin_panel.py code)
    result = {}
    for record in doc.get("records", []):
        result[record["roll_no"]] = {
            "status": record.get("status", "Absent"),
            "remark": record.get("remark", ""),
        }
    return result


def get_all_daily_attendance_db() -> dict:
    """
    Fetches ALL daily attendance entries from MongoDB.

    Returns:
        Dict mapping date_str → {Roll_No → {"status": ..., "remark": ...}},
        compatible with the JSON file format.
    """
    db = get_database()
    if db is None:
        return {}

    all_data = {}
    try:
        docs = db["daily_attendance"].find({}).sort("date", 1)
        for doc in docs:
            date_str = doc["_id"]
            entry = {}
            for record in doc.get("records", []):
                entry[record["roll_no"]] = {
                    "status": record.get("status", "Absent"),
                    "remark": record.get("remark", ""),
                }
            all_data[date_str] = entry
    except Exception:
        pass

    return all_data


def get_student_attendance_history(roll_no: str) -> list[dict]:
    """
    Fetches all attendance entries for a specific student across all dates.

    Returns:
        List of dicts: [{"date": "...", "status": "...", "remark": "..."}]
    """
    db = get_database()
    if db is None:
        return []

    history = []
    try:
        docs = db["daily_attendance"].find(
            {"records.roll_no": roll_no}
        ).sort("date", 1)

        for doc in docs:
            for record in doc.get("records", []):
                if record["roll_no"] == roll_no:
                    history.append({
                        "date": doc["date"],
                        "status": record.get("status", "Absent"),
                        "remark": record.get("remark", ""),
                    })
                    break
    except Exception:
        pass

    return history


# ==============================================================================
# ML RESULTS CRUD OPERATIONS
# ==============================================================================

def save_ml_run(metrics: dict, predictions_df: pd.DataFrame) -> bool:
    """
    Persists a model run's metadata and per-student prediction snapshot
    into the 'ml_results' collection.

    Args:
        metrics: Model performance metrics dict (R2, MAE, feature importances).
        predictions_df: DataFrame with prediction columns per student.

    Returns:
        True if saved successfully.
    """
    db = get_database()
    if db is None:
        return False

    timestamp = datetime.datetime.utcnow().isoformat()
    run_id = f"run_{timestamp}"

    # Build per-student prediction list
    pred_list = []
    pred_cols = [
        "Roll_No", "Student_Name", "Predicted_Sem1_2_Total",
        "Predicted_GPA", "Risk_Level"
    ]
    available_cols = [c for c in pred_cols if c in predictions_df.columns]

    for _, row in predictions_df.iterrows():
        entry = {}
        for col in available_cols:
            val = row[col]
            # Convert numpy types to native Python types for MongoDB
            if isinstance(val, (np.integer,)):
                val = int(val)
            elif isinstance(val, (np.floating,)):
                val = float(val)
            entry[col.lower()] = val
        pred_list.append(entry)

    doc = {
        "_id": run_id,
        "model_type": "RandomForestRegressor",
        "run_timestamp": timestamp,
        "metrics": _sanitize_for_mongo(metrics),
        "predictions": pred_list,
    }

    try:
        db["ml_results"].insert_one(doc)

        # Also update each student's predictions sub-document
        for entry in pred_list:
            roll = entry.get("roll_no", "")
            if roll:
                upsert_student_predictions(roll, {
                    "predicted_sem1_2_total": entry.get("predicted_sem1_2_total", 0),
                    "predicted_gpa": entry.get("predicted_gpa", 0),
                    "risk_level": entry.get("risk_level", ""),
                })

        return True
    except Exception:
        return False


def get_latest_ml_run() -> dict | None:
    """
    Fetches the most recent ML model run from the 'ml_results' collection.

    Returns:
        Dict with model metadata and predictions, or None if unavailable.
    """
    db = get_database()
    if db is None:
        return None

    try:
        doc = db["ml_results"].find_one(
            {}, sort=[("run_timestamp", -1)]
        )
        return doc
    except Exception:
        return None


# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def _safe_float(value, default=0.0) -> float:
    """Safely convert a value to float, handling NaN and None."""
    if value is None:
        return default
    try:
        result = float(value)
        if np.isnan(result):
            return default
        return round(result, 2)
    except (ValueError, TypeError):
        return default


def _sanitize_for_mongo(obj):
    """
    Recursively converts numpy types to native Python types
    so they can be serialized to MongoDB.
    """
    if isinstance(obj, dict):
        return {k: _sanitize_for_mongo(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_sanitize_for_mongo(v) for v in obj]
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


def drop_all_collections() -> bool:
    """
    WARNING: Drops all collections in the database. For development/reset only.
    """
    db = get_database()
    if db is None:
        return False
    try:
        for name in db.list_collection_names():
            db[name].drop()
        return True
    except Exception:
        return False
