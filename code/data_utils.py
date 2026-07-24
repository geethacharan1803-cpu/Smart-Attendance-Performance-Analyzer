"""
Data Utilities Module — Smart Attendance & Performance Analyzer
Integrates Linear Algebra (Matrix Ops, Dot Product, Credit-Weighted Scoring),
Data Structures (Custom QuickSort with Median-of-Three), and File I/O.
"""

import csv
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Any

# =============================================================================
# SEMESTER 1-1 SUBJECTS  (Aug 4, 2025 – Jan 21, 2026)
# =============================================================================
SEM_1_1_SUBJECTS = [
    "Linear Algebra & Calculus (LA&C)",
    "C Programming",
    "Engineering Physics",
    "Engineering Graphics",
    "Basic Electrical & Electronics Engineering (BEEE)"
]

# =============================================================================
# SEMESTER 1-2 SUBJECTS  (Jan 26, 2026 – Jul 9, 2026)
# =============================================================================
SEM_1_2_SUBJECTS = [
    "Differential Equations & Vector Calculus (DEVC)",
    "Communicative English",
    "Applied Chemistry",
    "Data Structures",
    "Basic Civil & Mechanical Engineering (BCME)"
]

# Weight Vector W for composite dot-product scoring
# W = [Attendance_%, Mid1, Mid2, External, Backlog_count]
WEIGHT_VECTOR = np.array([0.25, 0.15, 0.15, 0.35, -0.10])

# Attendance threshold (JNTUK R23 mandatory minimum)
ATTENDANCE_THRESHOLD = 75.0


# ==============================================================================
# SECTION 1  — LINEAR ALGEBRA: FEATURE MATRICES & WEIGHTED SCORING
# ==============================================================================

def extract_feature_matrix(students: List[Dict[str, Any]],
                           semester: str = "sem1_1") -> Tuple[np.ndarray, List[str]]:
    """
    Constructs feature matrix X of shape (N, 5) for a given semester prefix.

    Feature Vector per student S_i:
        S_i = [attendance_pct, mid1, mid2, external, backlog_count]
    """
    pfx = semester  # e.g. "sem1_1" or "sem1_2"
    matrix_rows, roll_nos = [], []
    for s in students:
        row = [
            float(s.get(f"{pfx}_attendance_pct", s.get("attendance_pct", 0.0))),
            float(s.get(f"{pfx}_mid1", s.get("mid1", 0.0))),
            float(s.get(f"{pfx}_mid2", s.get("mid2", 0.0))),
            float(s.get(f"{pfx}_external", s.get("external", 0.0))),
            float(s.get(f"{pfx}_backlog_count", s.get("backlog_count", 0))),
        ]
        matrix_rows.append(row)
        roll_nos.append(s["roll_no"])
    return np.array(matrix_rows, dtype=np.float64), roll_nos


def calculate_composite_score(student_vector: np.ndarray,
                               weights: np.ndarray = WEIGHT_VECTOR) -> float:
    """
    Computes composite performance score via the vector dot product:

        score_i  =  S_i . W  =  SUM( S_i[j] * W[j] )
    """
    return float(np.dot(student_vector, weights))


def calculate_credit_weighted_score(internal_marks: float,
                                     attendance_pct: float) -> float:
    """
    Credit-weighted scoring formula (per JNTUK R23 rubric):
        Weighted_Score = (Internal_Marks * 0.4) + (Attendance_% * 0.6)
    """
    return round(internal_marks * 0.4 + attendance_pct * 0.6, 2)


def compute_class_scores(students: List[Dict[str, Any]],
                          semester: str = "sem1_1") -> List[Dict[str, Any]]:
    """Attaches composite_score and credit_weighted_score to each student."""
    pfx = semester
    X, _ = extract_feature_matrix(students, semester)
    scores = np.dot(X, WEIGHT_VECTOR)

    updated = []
    for idx, s in enumerate(students):
        c = dict(s)
        c["composite_score"] = round(float(scores[idx]), 2)

        att = float(s.get(f"{pfx}_attendance_pct", s.get("attendance_pct", 0)))
        mid1 = float(s.get(f"{pfx}_mid1", s.get("mid1", 0)))
        mid2 = float(s.get(f"{pfx}_mid2", s.get("mid2", 0)))
        internal = (mid1 + mid2) / 2.0
        c["credit_weighted_score"] = calculate_credit_weighted_score(internal, att)

        c["attendance_alert"] = att < ATTENDANCE_THRESHOLD
        updated.append(c)
    return updated


def compute_pearson_correlation(x: List[float], y: List[float]) -> float:
    """Pearson correlation coefficient r."""
    ax, ay = np.array(x, dtype=np.float64), np.array(y, dtype=np.float64)
    if len(ax) != len(ay) or len(ax) == 0:
        return 0.0
    mx, my = np.mean(ax), np.mean(ay)
    num = np.sum((ax - mx) * (ay - my))
    den = np.sqrt(np.sum((ax - mx) ** 2) * np.sum((ay - my) ** 2))
    return float(num / den) if den != 0 else 0.0


def assign_color_risk(student: Dict[str, Any], semester: str = "sem1_1") -> str:
    """Assign color risk tier based on marks and attendance."""
    pfx = semester
    mid1 = float(student.get(f"{pfx}_mid1", student.get("mid1", 0)))
    mid2 = float(student.get(f"{pfx}_mid2", student.get("mid2", 0)))
    ext = float(student.get(f"{pfx}_external", student.get("external", 0)))
    att = float(student.get(f"{pfx}_attendance_pct", student.get("attendance_pct", 0)))

    avg_pct = ((mid1 / 30.0) + (mid2 / 30.0) + (ext / 70.0)) / 3.0 * 100.0

    if avg_pct >= 60 and att >= 75:
        return "Safe"        # Green
    elif avg_pct >= 40 or att >= 65:
        return "Moderate"    # Yellow
    else:
        return "High Risk"   # Red


# ==============================================================================
# SECTION 2  — DATA STRUCTURES: CUSTOM QUICKSORT
# ==============================================================================

def _median_of_three(arr, lo, hi, key):
    mid = (lo + hi) // 2
    vl, vm, vh = arr[lo].get(key, 0), arr[mid].get(key, 0), arr[hi].get(key, 0)
    if (vl - vm) * (vh - vl) >= 0:
        return lo
    elif (vm - vl) * (vh - vm) >= 0:
        return mid
    return hi


def _partition(arr, lo, hi, key, descending):
    pi = _median_of_three(arr, lo, hi, key)
    arr[pi], arr[hi] = arr[hi], arr[pi]
    pv = arr[hi].get(key, 0)
    i = lo - 1
    for j in range(lo, hi):
        cv = arr[j].get(key, 0)
        cond = (cv >= pv) if descending else (cv <= pv)
        if cond:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    return i + 1


def custom_quicksort(arr: List[Dict[str, Any]], low: int = 0, high: int = -1,
                     key: str = "composite_score", descending: bool = True) -> List[Dict[str, Any]]:
    """Custom QuickSort with median-of-three pivot selection."""
    arr_copy = list(arr)
    if high == -1:
        high = len(arr_copy) - 1

    def _qs(a, l, h):
        if l < h:
            p = _partition(a, l, h, key, descending)
            _qs(a, l, p - 1)
            _qs(a, p + 1, h)

    _qs(arr_copy, low, high)
    return arr_copy


# ==============================================================================
# SECTION 3  — FILE I/O MECHANICS
# ==============================================================================

def read_csv_buffered(file_path: str) -> List[Dict[str, Any]]:
    records = []
    try:
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                for k in row:
                    if any(t in k for t in ("attendance", "mid1", "mid2", "external")):
                        try:
                            row[k] = float(row[k])
                        except (ValueError, TypeError):
                            pass
                    if "backlog" in k:
                        try:
                            row[k] = int(row[k])
                        except (ValueError, TypeError):
                            pass
                records.append(dict(row))
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"Error reading CSV: {e}")
    return records


def read_csv_pandas(file_path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Pandas read error: {e}")
        return pd.DataFrame()


def save_csv_pandas(df: pd.DataFrame, file_path: str) -> bool:
    try:
        df.to_csv(file_path, index=False, encoding="utf-8")
        return True
    except Exception as e:
        print(f"CSV save error: {e}")
        return False
