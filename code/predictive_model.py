"""
================================================================================
PREDICTIVE_MODEL.PY — Sem 1-1 → Sem 1-2 Performance Predictor
JNTUK R23 B.Tech AI & Data Science — Project 17 (V2)
================================================================================
[NEW Feature: Predictive Analytics]
Implements a Random Forest Regressor using Scikit-Learn that:
  - Takes Sem 1-1 inputs (Mid-1, Mid-2, Internal, External, Attendance)
  - Predicts individual student Sem 1-2 total score & expected GPA
  - Classifies students into risk levels (Safe / Watch / Critical)
  - Provides model transparency via feature importances & metrics
================================================================================
"""

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error, r2_score

from config import PREDICTOR_FEATURES, PREDICTOR_TARGET


# ==============================================================================
# MODEL TRAINING
# ==============================================================================

def train_performance_predictor(df: pd.DataFrame) -> tuple[RandomForestRegressor, dict]:
    """
    Trains a Random Forest Regressor on Sem 1-1 features to predict Sem 1-2
    total performance score.

    Uses 5-fold cross-validation to estimate generalization performance.

    Args:
        df: DataFrame containing both PREDICTOR_FEATURES and PREDICTOR_TARGET columns.

    Returns:
        tuple: (trained RandomForestRegressor model, metrics dict)
            metrics dict keys:
                - cv_r2_mean: Mean R^2 across 5 folds
                - cv_r2_std: Std of R^2 across 5 folds
                - train_r2: R^2 on full training data
                - train_mae: MAE on full training data
                - feature_importances: dict mapping feature name → importance
    """
    # Validate that required columns exist
    missing = [c for c in PREDICTOR_FEATURES + [PREDICTOR_TARGET] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns for predictive model: {missing}")

    X = df[PREDICTOR_FEATURES].to_numpy()
    y = df[PREDICTOR_TARGET].to_numpy()

    # Train Random Forest
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=8,
        min_samples_split=5,
        min_samples_leaf=3,
        random_state=42,
        n_jobs=-1,
    )

    # Cross-validation for honest performance estimate
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')

    # Fit on full data for production use
    model.fit(X, y)
    y_pred = model.predict(X)

    # Compute metrics
    metrics = {
        'cv_r2_mean': round(float(np.mean(cv_scores)), 4),
        'cv_r2_std': round(float(np.std(cv_scores)), 4),
        'train_r2': round(float(r2_score(y, y_pred)), 4),
        'train_mae': round(float(mean_absolute_error(y, y_pred)), 2),
        'feature_importances': dict(
            zip(PREDICTOR_FEATURES, [round(float(x), 4) for x in model.feature_importances_])
        ),
    }

    return model, metrics


# ==============================================================================
# PREDICTION & RISK CLASSIFICATION
# ==============================================================================

def predict_semester_performance(
    model: RandomForestRegressor, df: pd.DataFrame
) -> pd.DataFrame:
    """
    Generates per-student Sem 1-2 predictions and enriches the DataFrame
    with predicted scores, predicted GPA, and risk levels.

    Args:
        model: Trained RandomForestRegressor.
        df: DataFrame with PREDICTOR_FEATURES columns.

    Returns:
        pd.DataFrame: Copy of df with added columns:
            - Predicted_Sem1_2_Total
            - Predicted_GPA
            - Risk_Level
            - Prediction_Delta (predicted - actual, if actual exists)
    """
    X = df[PREDICTOR_FEATURES].to_numpy()
    predictions = model.predict(X)

    result = df.copy()
    result['Predicted_Sem1_2_Total'] = np.round(predictions, 1)

    # Convert to 10-point GPA scale (total is a percentage)
    result['Predicted_GPA'] = np.round(predictions / 10.0, 2).clip(2.0, 10.0)

    # Classify risk levels
    result['Risk_Level'] = result['Predicted_Sem1_2_Total'].apply(classify_risk_level)

    # Compute prediction delta if actual Sem 1-2 data exists
    if PREDICTOR_TARGET in df.columns:
        result['Prediction_Delta'] = np.round(
            result['Predicted_Sem1_2_Total'] - df[PREDICTOR_TARGET], 1
        )

    return result


def classify_risk_level(predicted_score: float) -> str:
    """
    Maps a predicted Sem 1-2 total score to a risk classification.

    Thresholds:
        >= 65%  → Safe (on track for good performance)
        45-65%  → Watch (needs monitoring and support)
        < 45%   → Critical (immediate intervention required)

    Args:
        predicted_score: Predicted percentage score for Sem 1-2.

    Returns:
        str: Risk level label.
    """
    if predicted_score >= 65.0:
        return "Safe"
    elif predicted_score >= 45.0:
        return "Watch"
    else:
        return "Critical"


def get_student_prediction_detail(
    model: RandomForestRegressor, student_row: pd.Series
) -> dict:
    """
    Generates a detailed prediction breakdown for a single student,
    including per-feature contributions.

    Args:
        model: Trained RandomForestRegressor.
        student_row: A single row (pd.Series) from the student DataFrame.

    Returns:
        dict with keys:
            - predicted_total: float
            - predicted_gpa: float
            - risk_level: str
            - sem1_1_total: float (actual Sem 1-1 total if available)
            - feature_values: dict mapping feature name → value
    """
    X = student_row[PREDICTOR_FEATURES].to_numpy().reshape(1, -1)
    predicted = float(model.predict(X)[0])

    detail = {
        'predicted_total': round(predicted, 1),
        'predicted_gpa': round(min(max(predicted / 10.0, 2.0), 10.0), 2),
        'risk_level': classify_risk_level(predicted),
        'feature_values': {
            feat: round(float(student_row[feat]), 1) for feat in PREDICTOR_FEATURES
        },
    }

    if 'Sem1_1_Total' in student_row.index:
        detail['sem1_1_total'] = round(float(student_row['Sem1_1_Total']), 1)

    if PREDICTOR_TARGET in student_row.index:
        actual = float(student_row[PREDICTOR_TARGET])
        detail['actual_sem1_2_total'] = round(actual, 1)
        detail['prediction_error'] = round(predicted - actual, 1)

    return detail
