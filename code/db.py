"""
Database & Persistence Layer (MongoDB PyMongo + Offline CSV Fallback)
Handles connection management, CRUD operations, daily attendance logging with 
faculty remarks & alert triggering, and automatic fallback to local CSV files.
"""

import os
import csv
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = "smart_attendance_db"
CSV_PATH = os.path.join("sample_data", "student_records.csv")

try:
    import pymongo
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False


class DatabaseManager:
    """Database Manager class supporting MongoDB with graceful offline CSV fallback."""
    def __init__(self, uri: str = MONGODB_URI, db_name: str = DB_NAME):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None
        self.is_offline = True
        self.status_message = ""
        self._connect()

    def _connect(self):
        if not PYMONGO_AVAILABLE:
            self.is_offline = True
            self.status_message = "PyMongo package not installed. Operating in local CSV Fallback mode."
            return

        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=2000)
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            self.is_offline = False
            self.status_message = f"Connected successfully to MongoDB Database '{self.db_name}'."
            self._initialize_collections()
        except (ConnectionFailure, ServerSelectionTimeoutError, Exception) as e:
            self.is_offline = True
            self.status_message = f"MongoDB unavailable ({type(e).__name__}). Fallback mode active (CSV)."

    def _initialize_collections(self):
        if self.is_offline or self.db is None:
            return
        if "students" not in self.db.list_collection_names() or self.db.students.count_documents({}) == 0:
            students_csv = self._read_csv_file()
            if students_csv:
                self.db.students.insert_many(students_csv)

    def _read_csv_file(self) -> List[Dict[str, Any]]:
        records = []
        if not os.path.exists(CSV_PATH):
            return records

        with open(CSV_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Type cast numerical fields for both Sem 1-1 and Sem 1-2
                for pfx in ["sem1_1", "sem1_2"]:
                    for key_num in ["attendance_pct", "mid1", "mid2", "external"]:
                        col = f"{pfx}_{key_num}"
                        if col in row:
                            try:
                                row[col] = float(row[col])
                            except (ValueError, TypeError):
                                pass
                    col_back = f"{pfx}_backlog_count"
                    if col_back in row:
                        try:
                            row[col_back] = int(row[col_back])
                        except (ValueError, TypeError):
                            pass
                records.append(dict(row))
        return records

    def _write_csv_file(self, records: List[Dict[str, Any]]) -> bool:
        if not records:
            return False
        fieldnames = list(records[0].keys())
        try:
            with open(CSV_PATH, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(records)
            return True
        except Exception as e:
            print(f"Error writing fallback CSV: {e}")
            return False

    def get_all_students(self) -> List[Dict[str, Any]]:
        """Retrieves all 80 student records from MongoDB or local CSV fallback."""
        if not self.is_offline and self.db is not None:
            try:
                docs = list(self.db.students.find({}, {'_id': 0}))
                if docs:
                    return docs
            except Exception:
                pass
        return self._read_csv_file()

    def get_student_by_roll(self, roll_no: str) -> Optional[Dict[str, Any]]:
        students = self.get_all_students()
        for s in students:
            if s.get("roll_no") == roll_no:
                return s
        return None

    def insert_attendance_log(self, date_str: str, subject: str, semester: str,
                              present_rolls: List[str], absent_rolls: List[str],
                              faculty_remarks: str = "") -> Dict[str, Any]:
        """
        Log daily classroom attendance, update attendance percentage, and 
        trigger mandatory alerts for students dropping below 75%.
        """
        log_doc = {
            "date": date_str,
            "subject": subject,
            "semester": semester,
            "present_rollnos": present_rolls,
            "absent_rollnos": absent_rolls,
            "faculty_remarks": faculty_remarks,
            "created_at": datetime.now().isoformat()
        }

        if not self.is_offline and self.db is not None:
            try:
                self.db.attendance_logs.insert_one(log_doc)
            except Exception as e:
                print(f"MongoDB attendance log error: {e}")

        # Update CSV fallback records and detect threshold alerts
        records = self._read_csv_file()
        triggered_alerts = []
        pfx = "sem1_1" if "1-1" in semester else "sem1_2"
        att_col = f"{pfx}_attendance_pct"
        rem_col = f"{pfx}_remarks"

        for s in records:
            if s["roll_no"] in absent_rolls:
                curr_att = float(s.get(att_col, 75.0))
                new_att = round(max(0.0, curr_att - 0.5), 1)
                s[att_col] = new_att
                
                # Check for 75% attendance alert threshold crossing
                if curr_att >= 75.0 and new_att < 75.0:
                    triggered_alerts.append({
                        "roll_no": s["roll_no"],
                        "name": s["name"],
                        "new_att": new_att,
                        "message": f"ATTENDANCE CRITICAL: Dropped below 75% threshold ({new_att}%)"
                    })
                
                if faculty_remarks:
                    existing_rem = s.get(rem_col, "")
                    s[rem_col] = f"[{date_str}] {faculty_remarks} | {existing_rem}"

        self._write_csv_file(records)

        return {
            "success": True,
            "log_doc": log_doc,
            "triggered_alerts": triggered_alerts
        }

    def cache_ml_results(self, clustered_data: List[Dict[str, Any]], model_info: Dict[str, Any]) -> bool:
        doc = {
            "timestamp": datetime.now().isoformat(),
            "model_info": model_info,
            "sample_clusters": clustered_data[:10]
        }
        if not self.is_offline and self.db is not None:
            try:
                self.db.ml_results.insert_one(doc)
                return True
            except Exception as e:
                print(f"Failed to cache ML results in MongoDB: {e}")
        return True


# Global Instance Singleton
db_manager = DatabaseManager()
