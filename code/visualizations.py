"""
Visualizations Module (Matplotlib & Seaborn)
Generates high-quality analytical charts styled with high-contrast Light Theme aesthetics:
1. Attendance vs. Marks correlation
2. Gender-wise backlog distribution
3. Semester growth trajectory (Sem 1-1 -> Sem 1-2)
4. K-Means Risk Cluster scatter plot
5. Elbow curve plot
6. Individual Student Historical vs Predicted Drill-Down Comparison Chart
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from typing import List, Dict, Any

CODE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CODE_DIR)
CHARTS_DIR = os.path.join(ROOT_DIR, "output", "charts")

plt.style.use('default')
BG_COLOR = '#f8fafc'
CARD_BG = '#ffffff'
TEXT_COLOR = '#0f172a'
LABEL_COLOR = '#334155'
GRID_COLOR = '#e2e8f0'

RISK_COLORS = {
    "Safe": "#16a34a",         # Emerald Green
    "Moderate": "#d97706",     # Amber Yellow
    "High Risk": "#dc2626"      # Rose Red
}

CLUSTER_COLORS = {
    "High Achievers": "#16a34a",
    "Moderate Learners": "#d97706",
    "At-Risk": "#dc2626"
}


def _apply_chart_styling(fig, ax, title: str, xlabel: str, ylabel: str):
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(CARD_BG)
    ax.set_title(title, fontsize=13, fontweight='bold', color=TEXT_COLOR, pad=12)
    ax.set_xlabel(xlabel, fontsize=10, fontweight='semibold', color=LABEL_COLOR)
    ax.set_ylabel(ylabel, fontsize=10, fontweight='semibold', color=LABEL_COLOR)
    ax.tick_params(colors=LABEL_COLOR, labelsize=9)
    ax.grid(True, linestyle='--', alpha=0.6, color=GRID_COLOR)
    for spine in ax.spines.values():
        spine.set_color('#cbd5e1')


def plot_attendance_vs_marks(students: List[Dict[str, Any]], semester_pfx: str = "sem1_1", save_png: bool = True) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(7, 4.2))
    att = [float(s.get(f"{semester_pfx}_attendance_pct", s.get("attendance_pct", 0))) for s in students]
    ext = [float(s.get(f"{semester_pfx}_external", s.get("external", 0))) for s in students]

    ax.scatter(att, ext, color='#0284c7', alpha=0.85, edgecolors='#0369a1', s=45, label='Student')

    if len(att) > 1:
        z = np.polyfit(att, ext, 1)
        p = np.poly1d(z)
        x_trend = np.linspace(min(att), max(att), 100)
        ax.plot(x_trend, p(x_trend), color='#4f46e5', linestyle='--', linewidth=2, label='Linear Trendline')

    _apply_chart_styling(fig, ax, f"Attendance % vs External Marks ({semester_pfx.upper().replace('_', '-')})", "Attendance Percentage (%)", "External Score (0-70)")
    ax.legend(facecolor=CARD_BG, edgecolor='#cbd5e1', labelcolor=TEXT_COLOR)

    if save_png:
        os.makedirs(CHARTS_DIR, exist_ok=True)
        fig.savefig(os.path.join(CHARTS_DIR, "attendance_vs_marks.png"), dpi=300, bbox_inches='tight', facecolor=BG_COLOR)

    return fig


def plot_gender_backlog_distribution(students: List[Dict[str, Any]], semester_pfx: str = "sem1_1", save_png: bool = True) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(7, 4.2))
    df = pd.DataFrame(students)
    back_col = f"{semester_pfx}_backlog_count" if f"{semester_pfx}_backlog_count" in df.columns else "backlog_count"
    
    if "gender" in df.columns and back_col in df.columns:
        grouped = df.groupby(["gender", back_col]).size().unstack(fill_value=0)
        x = np.arange(len(grouped.columns))
        width = 0.35
        
        fem_vals = grouped.loc["Female"].values if "Female" in grouped.index else [0]*len(x)
        male_vals = grouped.loc["Male"].values if "Male" in grouped.index else [0]*len(x)
        
        rects1 = ax.bar(x - width/2, fem_vals, width, label='Female (30)', color='#db2777', edgecolor='#be185d')
        rects2 = ax.bar(x + width/2, male_vals, width, label='Male (50)', color='#2563eb', edgecolor='#1d4ed8')
        
        ax.set_xticks(x)
        ax.set_xticklabels([f"{c} Backlog(s)" if c > 0 else "0 Backlogs" for c in grouped.columns])
        
        for bar in rects1:
            if bar.get_height() > 0:
                ax.annotate(f'{int(bar.get_height())}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                            xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', color=TEXT_COLOR, fontsize=8, fontweight='bold')
        for bar in rects2:
            if bar.get_height() > 0:
                ax.annotate(f'{int(bar.get_height())}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                            xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', color=TEXT_COLOR, fontsize=8, fontweight='bold')

    _apply_chart_styling(fig, ax, "Gender-Wise Backlog Distribution", "Backlog Count Category", "Number of Students")
    ax.legend(facecolor=CARD_BG, edgecolor='#cbd5e1', labelcolor=TEXT_COLOR)

    if save_png:
        os.makedirs(CHARTS_DIR, exist_ok=True)
        fig.savefig(os.path.join(CHARTS_DIR, "gender_backlog_distribution.png"), dpi=300, bbox_inches='tight', facecolor=BG_COLOR)

    return fig


def plot_growth_trajectory(students: List[Dict[str, Any]], save_png: bool = True) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ext_11 = [float(s.get("sem1_1_external", 40.0)) for s in students]
    ext_12 = [float(s.get("sem1_2_external", 42.0)) for s in students]

    indices = np.argsort(ext_11)
    s_11 = np.array(ext_11)[indices]
    s_12 = np.array(ext_12)[indices]

    ax.plot(range(len(students)), s_11, color='#4f46e5', label='Sem 1-1 External Marks', linewidth=1.8, alpha=0.85)
    ax.plot(range(len(students)), s_12, color='#16a34a', label='Sem 1-2 External Marks', linewidth=1.8, linestyle='--')
    
    ax.fill_between(range(len(students)), s_11, s_12, where=(s_12 >= s_11), color='#16a34a', alpha=0.15, label='Positive Growth')
    ax.fill_between(range(len(students)), s_11, s_12, where=(s_12 < s_11), color='#dc2626', alpha=0.15, label='Academic Decline')

    _apply_chart_styling(fig, ax, "Academic Performance Growth Trajectory (Sem 1-1 -> Sem 1-2)", "Students (Sorted by Sem 1-1)", "External Exam Score (0-70)")
    ax.legend(facecolor=CARD_BG, edgecolor='#cbd5e1', labelcolor=TEXT_COLOR, loc='upper left')

    if save_png:
        os.makedirs(CHARTS_DIR, exist_ok=True)
        fig.savefig(os.path.join(CHARTS_DIR, "growth_trajectory.png"), dpi=300, bbox_inches='tight', facecolor=BG_COLOR)

    return fig


def plot_student_drilldown(student: Dict[str, Any]) -> plt.Figure:
    """Individual Student Drill-Down Comparison Chart (Sem 1-1 vs Sem 1-2 Predicted & Actual)."""
    fig, ax = plt.subplots(figsize=(7, 4.0))

    categories = ["Attendance %", "Mid-1 (/30)", "Mid-2 (/30)", "External (/70)", "Backlogs"]
    
    sem1_1_vals = [
        float(student.get("sem1_1_attendance_pct", 0)),
        float(student.get("sem1_1_mid1", 0)),
        float(student.get("sem1_1_mid2", 0)),
        float(student.get("sem1_1_external", 0)),
        float(student.get("sem1_1_backlog_count", 0))
    ]

    sem1_2_pred_vals = [
        float(student.get("sem1_2_attendance_pct", student.get("sem1_1_attendance_pct", 0))),
        float(student.get("sem1_2_mid1", student.get("sem1_1_mid1", 0))),
        float(student.get("sem1_2_mid2", student.get("sem1_1_mid2", 0))),
        float(student.get("predicted_sem1_2_external", student.get("sem1_2_external", 0))),
        float(student.get("sem1_2_backlog_count", 0))
    ]

    x = np.arange(len(categories))
    width = 0.35

    rects1 = ax.bar(x - width/2, sem1_1_vals, width, label='Sem 1-1 (Actual)', color='#4f46e5', edgecolor=BG_COLOR)
    rects2 = ax.bar(x + width/2, sem1_2_pred_vals, width, label='Sem 1-2 (Predicted)', color='#16a34a', edgecolor=BG_COLOR)

    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9, fontweight='bold')

    for bar in rects1:
        h = bar.get_height()
        if h > 0:
            ax.annotate(f'{h:.1f}', xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', color=TEXT_COLOR, fontsize=8, fontweight='bold')
    for bar in rects2:
        h = bar.get_height()
        if h > 0:
            ax.annotate(f'{h:.1f}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()), xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', color=TEXT_COLOR, fontsize=8, fontweight='bold')

    title_str = f"Drill-Down Comparison: {student.get('roll_no', '')} - {student.get('name', '')}"
    _apply_chart_styling(fig, ax, title_str, "Academic Metric", "Metric Value")
    ax.legend(facecolor=CARD_BG, edgecolor='#cbd5e1', labelcolor=TEXT_COLOR)

    return fig


def plot_kmeans_clusters(clustered_students: List[Dict[str, Any]], save_png: bool = True) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(7.5, 4.5))

    df = pd.DataFrame(clustered_students)
    if "risk_cluster" not in df.columns:
        df["risk_cluster"] = "Moderate Learners"

    for cluster_name, color in CLUSTER_COLORS.items():
        subset = df[df["risk_cluster"].str.contains(cluster_name, case=False, na=False)]
        if not subset.empty:
            att = subset.get("sem1_1_attendance_pct", subset.get("attendance_pct"))
            ax.scatter(att, subset["composite_score"], c=color, label=f"{cluster_name} ({len(subset)})", s=60, alpha=0.9, edgecolor='white')

    _apply_chart_styling(fig, ax, "K-Means Student Risk Clusters (k=3)", "Attendance Percentage (%)", "Linear Algebra Composite Score")
    ax.legend(facecolor=CARD_BG, edgecolor='#cbd5e1', labelcolor=TEXT_COLOR, loc='upper left')

    if save_png:
        os.makedirs(CHARTS_DIR, exist_ok=True)
        fig.savefig(os.path.join(CHARTS_DIR, "kmeans_clusters.png"), dpi=300, bbox_inches='tight', facecolor=BG_COLOR)

    return fig


def plot_elbow_curve(elbow_data: Dict[int, float], save_png: bool = True) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ks, inertias = list(elbow_data.keys()), list(elbow_data.values())
    ax.plot(ks, inertias, marker='o', color='#0284c7', linewidth=2.5, markersize=8, label='Inertia')
    if 3 in elbow_data:
        ax.plot(3, elbow_data[3], marker='*', color='#d97706', markersize=16, label='Optimal k=3')

    _apply_chart_styling(fig, ax, "Elbow Method Curve for Optimal Cluster Count", "Number of Clusters (k)", "Inertia (WCSS)")
    ax.legend(facecolor=CARD_BG, edgecolor='#cbd5e1', labelcolor=TEXT_COLOR)

    if save_png:
        os.makedirs(CHARTS_DIR, exist_ok=True)
        fig.savefig(os.path.join(CHARTS_DIR, "elbow_curve.png"), dpi=300, bbox_inches='tight', facecolor=BG_COLOR)

    return fig


def export_all_charts(students: List[Dict[str, Any]], ml_results: Dict[str, Any]):
    os.makedirs(CHARTS_DIR, exist_ok=True)
    plot_attendance_vs_marks(students, save_png=True)
    plot_gender_backlog_distribution(students, save_png=True)
    plot_growth_trajectory(students, save_png=True)
    plot_kmeans_clusters(ml_results.get("clustered_students", students), save_png=True)
    plot_elbow_curve(ml_results.get("elbow_data", {1: 100, 2: 50, 3: 20}), save_png=True)
    plt.close('all')
