"""
Machine Learning Engine Module (Scikit-Learn)
Provides K-Means Student Risk Clustering, Feature Scaling (StandardScaler), 
Elbow Curve Calculation, Silhouette Scoring, Linear Regression, and 
Random Forest Regressor Performance Trajectory Forecasting.
"""

import os
import sys
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Any
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

CODE_DIR = os.path.dirname(os.path.abspath(__file__))
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

from data_utils import compute_class_scores, assign_color_risk


def calculate_gpa(external_score_70: float, internal_marks_30: float = 20.0) -> float:
    """
    Converts combined score (Internal out of 30 + External out of 70) to 10-point GPA scale.
    """
    total_100 = external_score_70 + internal_marks_30
    if total_100 >= 90:
        return 10.0
    elif total_100 >= 80:
        return 9.0
    elif total_100 >= 70:
        return 8.0
    elif total_100 >= 60:
        return 7.0
    elif total_100 >= 50:
        return 6.0
    elif total_100 >= 40:
        return 5.0
    else:
        return 0.0


class MLEngine:
    """ML Engine supporting K-Means Clustering, Linear Regression, and Random Forest Regressor."""
    def __init__(self):
        self.scaler = StandardScaler()
        self.kmeans_model = None
        self.linear_model = None
        self.rf_model = None
        self.cluster_mapping = {}

    def prepare_features(self, students: List[Dict[str, Any]], semester: str = "sem1_1") -> Tuple[np.ndarray, np.ndarray, List[Dict[str, Any]]]:
        """Extracts feature array: [attendance_pct, avg_marks, backlog_count]."""
        students_scored = compute_class_scores(students, semester=semester)
        pfx = semester
        feature_list = []

        for s in students_scored:
            att = float(s.get(f"{pfx}_attendance_pct", s.get("attendance_pct", 0)))
            m1 = float(s.get(f"{pfx}_mid1", s.get("mid1", 0)))
            m2 = float(s.get(f"{pfx}_mid2", s.get("mid2", 0)))
            ext = float(s.get(f"{pfx}_external", s.get("external", 0)))
            back = float(s.get(f"{pfx}_backlog_count", s.get("backlog_count", 0)))

            avg_m = (m1 + m2 + ext) / 3.0
            feature_list.append([att, avg_m, back])

        X_raw = np.array(feature_list, dtype=np.float64)
        X_scaled = self.scaler.fit_transform(X_raw)

        return X_raw, X_scaled, students_scored

    def compute_elbow_curve(self, X_scaled: np.ndarray, max_k: int = 8) -> Dict[int, float]:
        inertias = {}
        for k in range(1, max_k + 1):
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            km.fit(X_scaled)
            inertias[k] = float(km.inertia_)
        return inertias

    def run_kmeans_clustering(self, students: List[Dict[str, Any]], semester: str = "sem1_1", k: int = 3) -> Dict[str, Any]:
        """Executes K-Means (k=3) on standardized features."""
        X_raw, X_scaled, students_scored = self.prepare_features(students, semester=semester)

        self.kmeans_model = KMeans(n_clusters=k, random_state=42, n_init=10)
        raw_labels = self.kmeans_model.fit_predict(X_scaled)

        sil_score = float(silhouette_score(X_scaled, raw_labels)) if len(set(raw_labels)) > 1 else 0.0

        cluster_scores = {}
        for c_idx in range(k):
            indices = np.where(raw_labels == c_idx)[0]
            scores = [students_scored[i]["composite_score"] for i in indices]
            cluster_scores[c_idx] = np.mean(scores) if len(scores) > 0 else 0.0

        sorted_clusters = sorted(cluster_scores.items(), key=lambda item: item[1], reverse=True)
        label_names = ["High Achievers", "Moderate Learners", "At-Risk"]
        mapping = {}
        for order, (c_idx, _) in enumerate(sorted_clusters):
            mapping[c_idx] = label_names[min(order, len(label_names) - 1)]

        self.cluster_mapping = mapping

        clustered_students = []
        for i, s in enumerate(students_scored):
            c_idx = raw_labels[i]
            s_copy = dict(s)
            s_copy["cluster_id"] = int(c_idx)
            s_copy["risk_cluster"] = mapping[c_idx]
            s_copy["color_risk"] = assign_color_risk(s, semester=semester)
            clustered_students.append(s_copy)

        os.makedirs("output", exist_ok=True)
        df_out = pd.DataFrame(clustered_students)
        df_out.to_csv(os.path.join("output", "clustered_students.csv"), index=False)

        return {
            "clustered_students": clustered_students,
            "silhouette_score": round(sil_score, 4),
            "centroids": self.kmeans_model.cluster_centers_,
            "elbow_data": self.compute_elbow_curve(X_scaled)
        }

    def train_predictive_trajectory_model(self, students: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Trains BOTH Linear Regression AND Random Forest Regressor models 
        to project Semester 1-2 external marks, expected GPA, and trajectory risk.
        """
        students_scored = compute_class_scores(students, semester="sem1_1")

        X_train, y_train = [], []
        for s in students_scored:
            att_11 = float(s.get("sem1_1_attendance_pct", 75.0))
            m1_11 = float(s.get("sem1_1_mid1", 20.0))
            m2_11 = float(s.get("sem1_1_mid2", 20.0))
            back_11 = float(s.get("sem1_1_backlog_count", 0))
            ext_12 = float(s.get("sem1_2_external", s.get("sem1_1_external", 40.0)))

            X_train.append([att_11, m1_11, m2_11, back_11])
            y_train.append(ext_12)

        X_mat = np.array(X_train)
        y_vec = np.array(y_train)

        # 1. Linear Regression Model
        self.linear_model = LinearRegression()
        self.linear_model.fit(X_mat, y_vec)
        pred_lr = self.linear_model.predict(X_mat)
        r2_lr = float(r2_score(y_vec, pred_lr))
        rmse_lr = float(np.sqrt(mean_squared_error(y_vec, pred_lr)))

        # 2. Random Forest Regressor Model
        self.rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.rf_model.fit(X_mat, y_vec)
        pred_rf = self.rf_model.predict(X_mat)
        r2_rf = float(r2_score(y_vec, pred_rf))
        rmse_rf = float(np.sqrt(mean_squared_error(y_vec, pred_rf)))

        results = []
        for i, s in enumerate(students_scored):
            pred_ext_lr = round(float(pred_lr[i]), 1)
            pred_ext_rf = round(float(pred_rf[i]), 1)
            
            # Use Random Forest prediction as primary ensemble output
            pred_ext = pred_ext_rf
            
            # Estimate Internal Marks
            m1 = float(s.get("sem1_1_mid1", 20.0))
            m2 = float(s.get("sem1_1_mid2", 20.0))
            avg_internal = (m1 + m2) / 2.0
            
            predicted_gpa = calculate_gpa(pred_ext, avg_internal)
            actual_ext = float(s.get("sem1_2_external", 40.0))
            actual_gpa = calculate_gpa(actual_ext, avg_internal)
            back_12 = int(s.get("sem1_2_backlog_count", 0))

            if pred_ext >= 50.0 and back_12 == 0:
                traj_status = "Safe / High Trajectory (Green)"
            elif pred_ext >= 35.0:
                traj_status = "Moderate Trajectory (Yellow)"
            else:
                traj_status = "High Risk / Remedial Trajectory (Red)"

            res = dict(s)
            res["predicted_sem1_2_external_lr"] = pred_ext_lr
            res["predicted_sem1_2_external_rf"] = pred_ext_rf
            res["predicted_sem1_2_external"] = pred_ext
            res["actual_sem1_2_external"] = actual_ext
            res["predicted_sem1_2_gpa"] = predicted_gpa
            res["actual_sem1_2_gpa"] = actual_gpa
            res["trajectory_status"] = traj_status
            results.append(res)

        os.makedirs("output", exist_ok=True)
        df_pred = pd.DataFrame(results)
        df_pred.to_csv(os.path.join("output", "risk_predictions.csv"), index=False)

        return {
            "predictions": results,
            "r2_score": round(r2_rf, 4),
            "r2_linear": round(r2_lr, 4),
            "r2_rf": round(r2_rf, 4),
            "rmse_linear": round(rmse_lr, 4),
            "rmse_rf": round(rmse_rf, 4),
            "rf_feature_importances": {
                "attendance_pct": round(float(self.rf_model.feature_importances_[0]), 4),
                "mid1": round(float(self.rf_model.feature_importances_[1]), 4),
                "mid2": round(float(self.rf_model.feature_importances_[2]), 4),
                "backlog_count": round(float(self.rf_model.feature_importances_[3]), 4)
            }
        }

    def predict_individual_student(self, attendance_pct: float, mid1: float, mid2: float, backlog_count: int) -> Dict[str, Any]:
        """Predict Sem 1-2 external exam score, GPA, and risk tier for single student input."""
        input_feats = np.array([[attendance_pct, mid1, mid2, backlog_count]])
        
        if self.rf_model is not None:
            pred_ext = float(self.rf_model.predict(input_feats)[0])
        elif self.linear_model is not None:
            pred_ext = float(self.linear_model.predict(input_feats)[0])
        else:
            pred_ext = 0.4 * attendance_pct + 0.8 * mid1 + 0.9 * mid2 - 4.0 * backlog_count

        pred_ext = max(0.0, min(70.0, round(pred_ext, 1)))
        avg_internal = (mid1 + mid2) / 2.0
        predicted_gpa = calculate_gpa(pred_ext, avg_internal)

        avg_m = (mid1 + mid2 + pred_ext) / 3.0

        if attendance_pct >= 75.0 and avg_m >= 35.0 and backlog_count == 0:
            cluster_name = "High Achievers (Safe / Green)"
            color_risk = "Safe"
            rec = "Maintain current academic trajectory. Recommended for advanced projects."
        elif attendance_pct >= 65.0 and backlog_count <= 1:
            cluster_name = "Moderate Learners (Yellow)"
            color_risk = "Moderate"
            rec = "Focus on Mid exam preparation & practical lab sessions."
        else:
            cluster_name = "At-Risk (Red)"
            color_risk = "High Risk"
            rec = "Mandatory attendance counseling & remedial lab/theory classes required."

        return {
            "predicted_external_score": pred_ext,
            "predicted_gpa": predicted_gpa,
            "predicted_cluster": cluster_name,
            "color_risk": color_risk,
            "recommendation": rec
        }


# Global Instance Singleton
ml_engine = MLEngine()
