"""
Flask Backend API for Vercel Serverless Deployment
Serves cohort analysis data, ML predictions, and handles attendance logging.
"""

import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS

# Resolve absolute paths to import modules from code/
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE_DIR = os.path.join(ROOT_DIR, "code")

for d in [CODE_DIR, ROOT_DIR]:
    if d not in sys.path:
        sys.path.insert(0, d)

from db import db_manager
from data_utils import compute_class_scores, custom_quicksort, compute_pearson_correlation
from ml_engine import ml_engine

app = Flask(__name__)
CORS(app)

@app.route("/api/students", methods=["GET"])
def get_students():
    """
    Returns the complete list of students with composite scores, ML risk clusters,
    and projected GPA/exam predictions.
    """
    try:
        raw_students = db_manager.get_all_students()
        semester = request.args.get("semester", "sem1_1")
        sem_pfx = "sem1_1" if "1-1" in semester else "sem1_2"
        
        scored_students = compute_class_scores(raw_students, semester=sem_pfx)
        ml_results = ml_engine.run_kmeans_clustering(scored_students, semester=sem_pfx, k=3)
        clustered_students = ml_results["clustered_students"]
        regression_results = ml_engine.train_predictive_trajectory_model(clustered_students)
        dataset = regression_results["predictions"]
        
        # Sort using Custom QuickSort if requested
        sort_by_score = request.args.get("sort", "true") == "true"
        if sort_by_score:
            dataset = custom_quicksort(dataset, key="composite_score", descending=True)
            
        return jsonify({
            "status": "success",
            "data": dataset
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/api/stats", methods=["GET"])
def get_stats():
    """
    Computes and returns cohort-level aggregate metrics, correlation matrices,
    and machine learning model accuracies.
    """
    try:
        raw_students = db_manager.get_all_students()
        semester = request.args.get("semester", "sem1_1")
        sem_pfx = "sem1_1" if "1-1" in semester else "sem1_2"
        
        scored_students = compute_class_scores(raw_students, semester=sem_pfx)
        ml_results = ml_engine.run_kmeans_clustering(scored_students, semester=sem_pfx, k=3)
        clustered_students = ml_results["clustered_students"]
        regression_results = ml_engine.train_predictive_trajectory_model(clustered_students)
        dataset = regression_results["predictions"]
        
        total_st = len(dataset)
        avg_att_val = sum(float(s.get(f"{sem_pfx}_attendance_pct", 0)) for s in dataset) / total_st if total_st > 0 else 0.0
        avg_score_val = sum(float(s.get("composite_score", 0)) for s in dataset) / total_st if total_st > 0 else 0.0
        total_backlogs_val = sum(int(s.get(f"{sem_pfx}_backlog_count", 0)) for s in dataset)
        alert_count = sum(1 for s in dataset if float(s.get(f"{sem_pfx}_attendance_pct", 0)) < 75.0)
        
        # Pearson correlation
        att_vals = [float(s.get(f"{sem_pfx}_attendance_pct", 0)) for s in dataset]
        ext_vals = [float(s.get(f"{sem_pfx}_external", 0)) for s in dataset]
        r_val = compute_pearson_correlation(att_vals, ext_vals)
        
        return jsonify({
            "status": "success",
            "stats": {
                "total_students": total_st,
                "avg_attendance": round(avg_att_val, 2),
                "avg_score": round(avg_score_val, 2),
                "total_backlogs": total_backlogs_val,
                "alert_count": alert_count,
                "pearson_correlation": round(r_val, 4),
                "silhouette_score": round(ml_results.get("silhouette_score", 0.0), 4),
                "r2_rf": round(regression_results.get("r2_rf", 0.0), 4),
                "r2_linear": round(regression_results.get("r2_linear", 0.0), 4)
            }
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Runs ML trajectory predictions for an individual input.
    """
    try:
        data = request.get_json() or {}
        att = float(data.get("attendance_pct", 76.0))
        mid1 = float(data.get("mid1", 21.0))
        mid2 = float(data.get("mid2", 22.0))
        backlog = int(data.get("backlog_count", 0))
        
        pred_res = ml_engine.predict_individual_student(att, mid1, mid2, backlog)
        return jsonify({
            "status": "success",
            "prediction": pred_res
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/api/log_attendance", methods=["POST"])
def log_attendance():
    """
    Logs class session attendance, recalculates student averages, and triggers
    at-risk threshold alerts (<75%).
    """
    try:
        data = request.get_json() or {}
        date_str = data.get("date_str")
        subject = data.get("subject")
        semester = data.get("semester")
        present_rolls = data.get("present_rolls", [])
        absent_rolls = data.get("absent_rolls", [])
        faculty_remarks = data.get("faculty_remarks", "")
        
        res = db_manager.insert_attendance_log(
            date_str=date_str,
            subject=subject,
            semester=semester,
            present_rolls=present_rolls,
            absent_rolls=absent_rolls,
            faculty_remarks=faculty_remarks
        )
        return jsonify({
            "status": "success",
            "result": res
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Vercel serverless functions handle requests via the WSGI application 'app'
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
