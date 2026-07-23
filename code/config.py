"""
================================================================================
CONFIG.PY — Centralized Configuration & Constants
JNTUK R23 B.Tech AI & Data Science — Project 17 (V2)
================================================================================
All file paths, color palettes, JNTUK thresholds, and credit weights are
defined here so every other module can import them from a single source.
================================================================================
"""

import os

# ==============================================================================
# PATH RESOLUTION
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "sample_data")
DAILY_DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Primary dataset (enriched V2)
STUDENT_CSV_V2 = os.path.join(DATA_DIR, "student_records_v2.csv")
# Legacy dataset (original)
STUDENT_CSV_V1 = os.path.join(DATA_DIR, "student_records.csv")
# Daily attendance persistence
DAILY_ATTENDANCE_JSON = os.path.join(DAILY_DATA_DIR, "daily_attendance.json")

# ==============================================================================
# JNTUK ACADEMIC THRESHOLDS
# ==============================================================================
JNTUK_ATTENDANCE_CUTOFF = 75.0       # Mandatory minimum attendance %
JNTUK_AT_RISK_SCORE_CUTOFF = 50.0    # Composite score below which student is "at-risk"

# ==============================================================================
# CREDIT WEIGHT VECTOR (for Matrix Dot Product S = M · W)
# ==============================================================================
# LA&Calculus: 18% | C Prog: 16% | Python: 16% | DS: 16% |
# Physics: 12% | BEEE: 12% | IT Workshop: 10%
SUBJECT_COLUMNS = [
    'LA_Calculus_Marks', 'C_Programming_Marks', 'Python_Programming_Marks',
    'Data_Structures_Marks', 'Eng_Physics_Marks', 'BEEE_Marks', 'IT_Workshop_Marks'
]
SUBJECT_LABELS = ['LA & Calc', 'C Prog', 'Python', 'Data Struct', 'Physics', 'BEEE', 'IT Workshop']
CREDIT_WEIGHTS = [0.18, 0.16, 0.16, 0.16, 0.12, 0.12, 0.10]

# ==============================================================================
# K-MEANS CLUSTERING
# ==============================================================================
N_CLUSTERS = 3
KMEANS_FEATURES = ['Overall_Attendance_Pct', 'Composite_Score', 'Backlogs']

# ==============================================================================
# PREDICTIVE MODEL FEATURES (Sem 1-1 → Sem 1-2)
# ==============================================================================
PREDICTOR_FEATURES = [
    'Sem1_1_Mid1', 'Sem1_1_Mid2', 'Sem1_1_Internal',
    'Sem1_1_External', 'Sem1_1_Attendance_Pct'
]
PREDICTOR_TARGET = 'Sem1_2_Total'

# ==============================================================================
# COLOR PALETTE — Modern Indigo-Violet-Emerald Theme
# ==============================================================================
COLORS = {
    'primary':      '#4F46E5',   # Indigo
    'primary_dark':  '#3730A3',
    'secondary':    '#7C3AED',   # Violet
    'success':      '#10B981',   # Emerald
    'warning':      '#F59E0B',   # Amber
    'danger':       '#F43F5E',   # Rose
    'info':         '#06B6D4',   # Cyan
    'bg_dark':      '#0F172A',   # Slate-900
    'bg_card':      '#F8FAFC',   # Slate-50
    'text_primary': '#0F172A',   # Slate-900
    'text_muted':   '#64748B',   # Slate-500
    'border':       '#E2E8F0',   # Slate-200
}

# ==============================================================================
# BATCH INFORMATION
# ==============================================================================
BATCH_INFO = {
    'institution': 'JNTUK R23 Curriculum',
    'branch': 'B.Tech AI & Data Science',
    'batch': '2025–2029',
    'total_students': 80,
    'girls': 30,
    'boys': 50,
    'roll_start': '25A91A4201',
    'roll_end': '25A91A4280',
}
