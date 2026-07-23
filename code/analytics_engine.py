"""
================================================================================
ANALYTICS_ENGINE.PY — Machine Learning, Statistics & Sorting Algorithms
JNTUK R23 B.Tech AI & Data Science — Project 17 (V2)
================================================================================
Contains all analytical computation functions:
  Module 3: Linear Algebra Matrix Dot Product (Feature Matrix × Weight Vector)
  Module 4: Custom QuickSort Algorithm (Data Structures)
  Module 5: K-Means Clustering, Pearson Correlation, OLS Regression,
            Growth Trajectory, Parent Alerts, LLM Advisory Notes
================================================================================
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from config import (
    SUBJECT_COLUMNS, CREDIT_WEIGHTS, N_CLUSTERS, KMEANS_FEATURES,
    JNTUK_ATTENDANCE_CUTOFF
)


# ==============================================================================
# MODULE 3: LINEAR ALGEBRA — MATRIX TRANSFORMATION & WEIGHTED SCORING
# [R23 Subject: Linear Algebra & Calculus — Matrices & Vector Spaces]
# ==============================================================================

def compute_linear_algebra_matrix_scores(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """
    [R23 Topic: Linear Algebra — Feature Matrix & Linear Combinations]
    Constructs Feature Matrix M (80 × 7) and computes composite scores via
    dot product with Credit Weight Vector W (7 × 1):

        S = M · W

    Weight allocation:
        LA&Calculus: 18% | C Prog: 16% | Python: 16% | DS: 16% |
        Physics: 12% | BEEE: 12% | IT Workshop: 10%

    Args:
        df: DataFrame containing all 7 subject mark columns.

    Returns:
        tuple: (M: ndarray shape (n,7), S: ndarray shape (n,))
    """
    M = df[SUBJECT_COLUMNS].to_numpy()
    W = np.array(CREDIT_WEIGHTS)
    S = np.dot(M, W)
    return M, S


# ==============================================================================
# MODULE 4: DATA STRUCTURES — QUICKSORT ALGORITHM
# [R23 Subject: Data Structures — Sorting Algorithms]
# ==============================================================================

def quicksort_student_records(records: list[dict], low: int, high: int) -> None:
    """
    [R23 Topic: Data Structures — QuickSort (Divide and Conquer)]
    Custom QuickSort algorithm sorting student records by 'Composite_Score'
    in DESCENDING order.

    Time Complexity:  Average O(n log n), Worst O(n^2)
    Space Complexity: O(log n) recursive stack

    Args:
        records: List of student dictionaries with 'Composite_Score' key.
        low: Starting index.
        high: Ending index.
    """
    if low < high:
        pi = _partition(records, low, high)
        quicksort_student_records(records, low, pi - 1)
        quicksort_student_records(records, pi + 1, high)


def _partition(arr: list[dict], low: int, high: int) -> int:
    """Lomuto partition scheme: pivot = last element, descending order."""
    pivot = arr[high]['Composite_Score']
    i = low - 1
    for j in range(low, high):
        if arr[j]['Composite_Score'] >= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# ==============================================================================
# MODULE 5: MACHINE LEARNING & ADVANCED FEATURE ENGINES
# [R23 Subject: AI & Machine Learning Foundations]
# ==============================================================================

def perform_kmeans_clustering(df: pd.DataFrame) -> tuple[pd.DataFrame, KMeans]:
    """
    [R23 Topic: Machine Learning — Unsupervised K-Means Clustering]
    Segments students into 3 Risk Cohorts based on attendance, composite
    score, and backlog count:
      - Cohort 0: High Achievers
      - Cohort 1: Moderate Learners
      - Cohort 2: At-Risk & Backlog Vulnerable

    Args:
        df: DataFrame with 'Overall_Attendance_Pct', 'Composite_Score', 'Backlogs'.

    Returns:
        tuple: (df with 'Cohort' column added, fitted KMeans model)
    """
    X = df[KMEANS_FEATURES].to_numpy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_scaled)

    # Map cluster IDs to meaningful cohort names based on mean composite score
    temp_df = df.copy()
    temp_df['Cluster'] = cluster_labels
    cluster_means = (
        temp_df.groupby('Cluster')['Composite_Score']
        .mean()
        .sort_values(ascending=False)
    )

    rank_to_cohort = {
        cluster_means.index[0]: "High Achievers",
        cluster_means.index[1]: "Moderate Learners",
        cluster_means.index[2]: "At-Risk & Backlog Vulnerable",
    }

    df = df.copy()
    df['Cohort'] = [rank_to_cohort[c] for c in cluster_labels]
    return df, kmeans


def compute_growth_trajectory(row: pd.Series) -> str:
    """
    [Feature: Semester-over-Semester Growth Trajectory Predictor]
    Compares Sem 1-1 vs Sem 1-2 attendance to classify trajectory.

    Returns:
        str: Trajectory label with emoji indicator.
    """
    delta = row['Sem1_2_Attendance_Pct'] - row['Sem1_1_Attendance_Pct']
    if delta > 3.0:
        return "Upward Trajectory"
    elif delta < -3.0:
        return "Declining Trajectory"
    else:
        return "Stable Progression"


def generate_parent_alerts(df: pd.DataFrame) -> list[dict]:
    """
    [Feature: Automated Parent Alert Simulator]
    Generates simulated SMS/WhatsApp alert payloads for students
    with attendance below the JNTUK 75% mandatory cutoff.

    Returns:
        list[dict]: Alert records with Roll_No, Student_Name, Attendance_Pct,
                    Backlogs, and Payload message.
    """
    alerts = []
    at_risk_df = df[df['Overall_Attendance_Pct'] < JNTUK_ATTENDANCE_CUTOFF]

    for _, row in at_risk_df.iterrows():
        alerts.append({
            'Roll_No': row['Roll_No'],
            'Student_Name': row['Student_Name'],
            'Attendance_Pct': row['Overall_Attendance_Pct'],
            'Backlogs': row['Backlogs'],
            'Payload': (
                f"ALERT: Parent of {row['Student_Name']} ({row['Roll_No']}): "
                f"Attendance is {row['Overall_Attendance_Pct']}%, BELOW 75% JNTUK cutoff. "
                f"Backlogs: {int(row['Backlogs'])}. Mandatory counseling required."
            ),
        })
    return alerts


def compute_statistical_trends(df: pd.DataFrame) -> dict:
    """
    [R23 Topic: AI/ML Foundations — Pearson Correlation & OLS Linear Regression]
    Computes the Pearson correlation coefficient (r) and OLS regression line
    (y = mx + c) between overall attendance and composite score.

    Returns:
        dict with keys: pearson_r, slope, intercept
    """
    x = df['Overall_Attendance_Pct'].to_numpy()
    y = df['Composite_Score'].to_numpy()

    r = np.corrcoef(x, y)[0, 1]
    m, c = np.polyfit(x, y, 1)

    return {'pearson_r': r, 'slope': m, 'intercept': c}


def generate_llm_advisory_note(row: pd.Series) -> str:
    """
    [R23 Topic: LLM Advisory Prompt Engineering]
    Generates a rule-based advisory recommendation note based on student's
    cohort classification.
    """
    cohort = row['Cohort']
    name = row['Student_Name']
    att = row['Overall_Attendance_Pct']
    backlogs = row['Backlogs']

    if "High Achievers" in cohort:
        return f"Encourage {name} to take up AI/ML research projects and mentor junior peers."
    elif "Moderate Learners" in cohort:
        return f"Counsel {name} on maintaining >80% attendance to improve mid-term performance."
    else:
        return (
            f"CRITICAL: Mandatory faculty counseling for {name} "
            f"({att}% att, {int(backlogs)} backlogs). Schedule remedial classes."
        )
