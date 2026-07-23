"""
================================================================================
DATA_LOADER.PY — File I/O & Data Ingestion Layer
JNTUK R23 B.Tech AI & Data Science — Project 17 (V2)
================================================================================
[R23 Topic: Programming & Problem Solving — File Handling Unit]
Handles all data persistence:
  - CSV ingestion with schema validation and median imputation
  - Daily attendance JSON read/write
================================================================================
"""

import os
import json
import pandas as pd
import streamlit as st

from config import (
    STUDENT_CSV_V2, STUDENT_CSV_V1, DAILY_ATTENDANCE_JSON, DAILY_DATA_DIR
)


# ==============================================================================
# CSV DATA INGESTION
# ==============================================================================

@st.cache_data
def load_student_dataset(filepath: str = None) -> pd.DataFrame:
    """
    [R23 Topic: File I/O & Data Cleaning]
    Loads student academic records from CSV storage with schema validation.
    Imputes missing numeric values with column medians.

    Args:
        filepath: Path to CSV file. Defaults to enriched V2 dataset.

    Returns:
        pd.DataFrame: Validated and cleaned student records.
    """
    if filepath is None:
        # Prefer V2 enriched dataset; fall back to V1 if V2 doesn't exist
        filepath = STUDENT_CSV_V2 if os.path.exists(STUDENT_CSV_V2) else STUDENT_CSV_V1

    if not os.path.exists(filepath):
        st.error(f"Dataset file '{filepath}' not found!")
        st.stop()

    df = pd.read_csv(filepath)

    # Schema validation — check required columns
    required_cols = [
        'Roll_No', 'Student_Name', 'Gender', 'Sem1_1_Attendance_Pct',
        'Sem1_2_Attendance_Pct', 'Overall_Attendance_Pct', 'LA_Calculus_Marks',
        'C_Programming_Marks', 'Python_Programming_Marks', 'Data_Structures_Marks',
        'Eng_Physics_Marks', 'BEEE_Marks', 'IT_Workshop_Marks',
        'Lab_Attendance_Pct', 'Backlogs'
    ]
    for col in required_cols:
        if col not in df.columns:
            st.error(f"Missing required CSV column: {col}")
            st.stop()

    # Median imputation for missing numeric values
    numeric_cols = [c for c in df.columns if c not in ['Roll_No', 'Student_Name', 'Gender']]
    for col in numeric_cols:
        if df[col].dtype in ['float64', 'int64', 'float32', 'int32']:
            df[col] = df[col].fillna(df[col].median())

    return df


# ==============================================================================
# DAILY ATTENDANCE JSON I/O
# ==============================================================================

def load_daily_attendance() -> dict:
    """
    Loads the daily attendance JSON store from disk.
    Returns an empty dict if the file doesn't exist yet.

    Schema:
        {
            "YYYY-MM-DD": {
                "Roll_No": {"status": "Present"|"Absent", "remark": "..."},
                ...
            }
        }
    """
    if not os.path.exists(DAILY_ATTENDANCE_JSON):
        return {}

    try:
        with open(DAILY_ATTENDANCE_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_daily_attendance(data: dict) -> None:
    """
    Persists the daily attendance dictionary to the JSON file.
    Creates the data directory if it doesn't exist.
    """
    os.makedirs(DAILY_DATA_DIR, exist_ok=True)
    with open(DAILY_ATTENDANCE_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_student_cumulative_attendance(roll_no: str, daily_data: dict) -> dict:
    """
    Computes cumulative attendance statistics for a specific student
    across all recorded daily entries.

    Returns:
        dict with keys: total_days, present_days, absent_days, cumulative_pct
    """
    total_days = 0
    present_days = 0

    for date_str, entries in daily_data.items():
        if roll_no in entries:
            total_days += 1
            if entries[roll_no].get('status') == 'Present':
                present_days += 1

    absent_days = total_days - present_days
    cumulative_pct = (present_days / total_days * 100) if total_days > 0 else 0.0

    return {
        'total_days': total_days,
        'present_days': present_days,
        'absent_days': absent_days,
        'cumulative_pct': round(cumulative_pct, 1),
    }
