"""
================================================================================
JNTUK R23 CURRICULUM - B.TECH ARTIFICIAL INTELLIGENCE & DATA SCIENCE (YEAR 1)
PROJECT 17: SMART ATTENDANCE & PERFORMANCE ANALYZER — V2 (MASTER UPGRADE)
================================================================================
Main Orchestrator — Imports all modular components and renders a 7-tab
Streamlit dashboard:
  1. Home              — Enhanced hero section with animated calendar stats
  2. Curriculum        — Integrated R23 subject explanations
  3. Programming Logic — Step-by-step code algorithm walkthroughs
  4. AI/ML Layer       — K-Means clustering + Predictive model explanation
  5. Live Dashboard    — Modernized analytics with advanced filters & graphs
  6. Admin Panel       — Daily attendance management & threshold monitor
  7. Predictive Analytics — Sem 1-1 → 1-2 prediction & student drill-down

Architecture: Thin orchestrator pattern — all heavy logic lives in:
  config.py, data_loader.py, academic_calendar.py, analytics_engine.py,
  predictive_model.py, ui_components.py, admin_panel.py
================================================================================
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Ensure UTF-8 output encoding for Windows terminals
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ==============================================================================
# STREAMLIT PAGE CONFIGURATION (must be first Streamlit call)
# ==============================================================================
st.set_page_config(
    page_title="Smart Attendance & Performance Analyzer | JNTUK R23 V2",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# MODULE IMPORTS (after st.set_page_config)
# ==============================================================================
from config import (
    BASE_DIR, COLORS, BATCH_INFO, SUBJECT_COLUMNS, SUBJECT_LABELS,
    CREDIT_WEIGHTS, JNTUK_ATTENDANCE_CUTOFF
)
from data_loader import load_student_dataset
from academic_calendar import JNTUKAcademicCalendar
from analytics_engine import (
    compute_linear_algebra_matrix_scores, quicksort_student_records,
    perform_kmeans_clustering, compute_growth_trajectory,
    compute_statistical_trends, generate_llm_advisory_note,
    generate_parent_alerts,
)
from predictive_model import (
    train_performance_predictor, predict_semester_performance,
    get_student_prediction_detail,
)
from ui_components import (
    inject_custom_css, render_metric_card, render_student_profile_card,
    render_sidebar_filters, get_risk_badge_html,
)
from admin_panel import render_admin_panel

# ==============================================================================
# APPLY CUSTOM CSS THEME
# ==============================================================================
inject_custom_css()

# Configure Matplotlib styling
plt.style.use(
    'seaborn-v0_8-whitegrid'
    if 'seaborn-v0_8-whitegrid' in plt.style.available
    else 'default'
)
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica', 'sans-serif']
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['figure.facecolor'] = '#FAFBFF'
plt.rcParams['axes.facecolor'] = '#FAFBFF'

# ==============================================================================
# SIDEBAR NAVIGATION
# ==============================================================================
st.sidebar.markdown("""
<div style="text-align: center; padding: 0.5rem 0 1rem 0;">
    <div style="font-size: 2.5rem; margin-bottom: 0.3rem;">🎓</div>
    <div style="font-size: 1.1rem; font-weight: 700; color: #F1F5F9;">Smart Attendance</div>
    <div style="font-size: 0.8rem; color: #94A3B8;">Performance Analyzer V2</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

selected_tab = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📚 Curriculum Subjects",
        "💻 Programming Logic",
        "🤖 AI/ML Layer",
        "⚡ Live Dashboard",
        "📋 Admin Panel",
        "🔮 Predictive Analytics",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div style="background: rgba(79,70,229,0.15); border-radius: 10px; padding: 12px; margin-top: 8px;">
    <div style="font-size: 0.8rem; font-weight: 600; color: #A5B4FC; margin-bottom: 4px;">PROJECT 17</div>
    <div style="font-size: 0.75rem; color: #CBD5E1;">
        JNTUK R23 &middot; AI & DS<br>
        Batch {BATCH_INFO['batch']}<br>
        {BATCH_INFO['total_students']} Students ({BATCH_INFO['girls']}G / {BATCH_INFO['boys']}B)
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# TAB 1: HOME
# ==============================================================================
if selected_tab == "🏠 Home":
    st.markdown(
        '<p class="hero-header">Smart Attendance & Performance Analyzer</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="hero-subtitle">'
        'JNTUK R23 Curriculum &mdash; B.Tech Artificial Intelligence & Data Science (2025 Batch) &mdash; V2 Upgrade'
        '</p>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="section-header">Project Overview</div>',
                    unsafe_allow_html=True)
        st.write("""
        Welcome to **Project 17: Smart Attendance & Performance Analyzer V2**!

        This upgraded platform tracks **80 students (30 Girls, 50 Boys)** from the 
        2025 AI & DS batch across Semester 1-1 and Semester 1-2 with:

        - **Linear Algebra Matrix Multiplication** for weighted composite scoring
        - **Custom QuickSort** for O(n log n) leaderboard ranking
        - **K-Means Clustering** for 3-cohort risk segmentation
        - **Random Forest Predictor** for Sem 1-1 → 1-2 performance forecasting
        - **Smart Admin Panel** for daily attendance tracking & JNTUK compliance
        - **Modernized Dashboard** with glassmorphism UI and advanced filters
        """)

        # Calendar Stats
        stats = JNTUKAcademicCalendar.get_semester_stats()
        st.markdown('<div class="section-header">Academic Calendar Stats</div>',
                    unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            render_metric_card("📅", str(stats['sem1_1_working_days']),
                               "Sem 1-1 Working Days", accent="indigo")
        with k2:
            render_metric_card("🧪", str(stats['sem1_1_lab_slots']),
                               "Sem 1-1 Lab Slots", accent="emerald")
        with k3:
            render_metric_card("📅", str(stats['sem1_2_working_days']),
                               "Sem 1-2 Working Days", accent="cyan")
        with k4:
            render_metric_card("🧪", str(stats['sem1_2_lab_slots']),
                               "Sem 1-2 Lab Slots", accent="amber")

    with col2:
        st.markdown('<div class="section-header">Batch Information</div>',
                    unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="student-profile">
            <div class="profile-stat"><span>Institution</span><strong>JNTUK R23</strong></div>
            <div class="profile-stat"><span>Branch</span><strong>AI & DS</strong></div>
            <div class="profile-stat"><span>Batch</span><strong>{BATCH_INFO['batch']}</strong></div>
            <div class="profile-stat"><span>Total Strength</span><strong>{BATCH_INFO['total_students']}</strong></div>
            <div class="profile-stat"><span>Girls</span><strong>{BATCH_INFO['girls']}</strong></div>
            <div class="profile-stat"><span>Boys</span><strong>{BATCH_INFO['boys']}</strong></div>
            <div class="profile-stat"><span>Semesters</span><strong>1-1 & 1-2</strong></div>
            <div class="profile-stat"><span>Roll Range</span><strong>{BATCH_INFO['roll_start']} — {BATCH_INFO['roll_end']}</strong></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['secondary']});
                    border-radius: 12px; padding: 16px; text-align: center;">
            <div style="color: white; font-size: 0.85rem; font-weight: 600; letter-spacing: 0.5px;">
                V2 FEATURES
            </div>
            <div style="color: #E0E7FF; font-size: 0.75rem; margin-top: 6px; line-height: 1.6;">
                Predictive Analytics &middot; Admin Panel<br>
                Advanced Filters &middot; Modern UI
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# TAB 2: CURRICULUM SUBJECTS
# ==============================================================================
elif selected_tab == "📚 Curriculum Subjects":
    st.markdown(
        '<p class="hero-header">Integrated JNTUK R23 Subjects</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="hero-subtitle">'
        'Detailed Explanations & Concrete Examples on 80 Student Records'
        '</p>',
        unsafe_allow_html=True
    )

    # Subject 1: File I/O
    st.markdown("""
    <div class="content-card">
        <h4>1. Programming & Problem Solving (File I/O & CSV Ingestion)</h4>
        <p><strong>R23 Syllabus Topic:</strong> File Handling, Pandas CSV Ingestion, Exception Handling, Data Imputation.</p>
        <p><strong>Application on 80 Students:</strong> Ingests <code>sample_data/student_records_v2.csv</code> containing 80 rows 
        and 26 academic columns (roll numbers <code>25A91A4201</code> to <code>25A91A4280</code>). Validates schema integrity 
        and performs median imputation for any missing marks.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="example-box">
        <strong>Beginner Example (File I/O in Action):</strong><br>
        <code>import pandas as pd</code><br>
        <code>df = pd.read_csv('sample_data/student_records_v2.csv')  # Ingests 80 student records</code><br>
        <code>df['LA_Calculus_Marks'].fillna(df['LA_Calculus_Marks'].median(), inplace=True)  # Clean missing data</code>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Subject 2: Linear Algebra
    st.markdown("""
    <div class="content-card">
        <h4>2. Linear Algebra & Calculus (Feature Matrix & Vector Dot Product)</h4>
        <p><strong>R23 Syllabus Topic:</strong> Vectors, 2D Feature Matrices, Credit Weight Vectors, Matrix Transformations.</p>
        <p><strong>Application on 80 Students:</strong> Represents all 80 students as an 80 &times; 7 Feature Matrix M, 
        where each row contains 7 normalized subject marks. Computes composite performance scores in a single 
        linear algebra step: <em>S = M &middot; W</em>.</p>
    </div>
    """, unsafe_allow_html=True)

    st.latex(
        r"M_{80 \times 7} = \begin{bmatrix} m_{1,1} & m_{1,2} & \dots & m_{1,7} \\"
        r" m_{2,1} & m_{2,2} & \dots & m_{2,7} \\"
        r" \vdots & \vdots & \ddots & \vdots \\"
        r" m_{80,1} & m_{80,2} & \dots & m_{80,7} \end{bmatrix}"
        r", \quad W_{7 \times 1} = \begin{bmatrix} 0.18 \\ 0.16 \\ 0.16 \\ 0.16 \\ 0.12 \\ 0.12 \\ 0.10 \end{bmatrix}"
    )
    st.latex(r"S_{80 \times 1} = M_{80 \times 7} \cdot W_{7 \times 1}")

    st.markdown("""
    <div class="example-box">
        <strong>Concrete Numerical Example (Student 25A91A4201 — Ananya Verma):</strong><br>
        &bull; Marks Vector: <code>[LA=56.2, C=59.6, Python=52.9, DS=50.2, Physics=46.7, BEEE=42.6, IT=45.0]</code><br>
        &bull; Weight Vector W: <code>[0.18, 0.16, 0.16, 0.16, 0.12, 0.12, 0.10]</code><br>
        &bull; Composite Score S = (56.2&times;0.18) + (59.6&times;0.16) + (52.9&times;0.16) + (50.2&times;0.16) + (46.7&times;0.12) + (42.6&times;0.12) + (45.0&times;0.10) = <strong>51.35%</strong>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Subject 3: Data Structures
    st.markdown("""
    <div class="content-card">
        <h4>3. Data Structures (QuickSort Algorithm)</h4>
        <p><strong>R23 Syllabus Topic:</strong> Array Data Structures, Divide-and-Conquer Sorting, Partitioning Logic.</p>
        <p><strong>Application on 80 Students:</strong> Custom QuickSort algorithm sorts the array of 80 student 
        dictionary records by composite score in descending order in average <em>O(n log n)</em> time complexity.</p>
    </div>
    """, unsafe_allow_html=True)

    st.latex(
        r"\text{Average Time Complexity: } \mathcal{O}(n \log_2 n) = 80 \times \log_2(80) \approx 506 \text{ comparisons}"
    )

    st.markdown("""
    <div class="example-box">
        <strong>QuickSort Partitioning Example:</strong><br>
        1. Select last student's composite score as Pivot (e.g. 72.5%).<br>
        2. Partition array: Students with score &ge; 72.5% move to the left; students &lt; 72.5% move to the right.<br>
        3. Recursively repeat on left and right partitions until all 80 students are sorted into Leaderboard Ranks #1 to #80.
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# TAB 3: PROGRAMMING LOGIC
# ==============================================================================
elif selected_tab == "💻 Programming Logic":
    st.markdown(
        '<p class="hero-header">Programming & Data Structures Logic</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="hero-subtitle">'
        'Step-by-Step Explanation of Code Algorithms & Matrix Math'
        '</p>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="section-header">1. Linear Algebra Matrix Multiplication (NumPy)</div>',
                unsafe_allow_html=True)
    st.code("""
# Feature Matrix M (80 x 7) multiplied by Weight Vector W (7 x 1)
def compute_linear_algebra_matrix_scores(df: pd.DataFrame):
    subject_cols = [
        'LA_Calculus_Marks', 'C_Programming_Marks', 'Python_Programming_Marks',
        'Data_Structures_Marks', 'Eng_Physics_Marks', 'BEEE_Marks', 'IT_Workshop_Marks'
    ]
    M = df[subject_cols].to_numpy()
    W = np.array([0.18, 0.16, 0.16, 0.16, 0.12, 0.12, 0.10])  # Weight vector summing to 1.0
    S = np.dot(M, W)  # Matrix Dot Product: S = M · W
    return M, S
    """, language="python")

    st.markdown('<div class="section-header">2. Custom QuickSort Algorithm (Data Structures)</div>',
                unsafe_allow_html=True)
    st.code("""
# Divide-and-Conquer QuickSort operating on array of student dictionary objects
def quicksort_student_records(records: list[dict], low: int, high: int) -> None:
    if low < high:
        pi = _partition(records, low, high)
        quicksort_student_records(records, low, pi - 1)
        quicksort_student_records(records, pi + 1, high)

def _partition(arr: list[dict], low: int, high: int) -> int:
    pivot = arr[high]['Composite_Score']
    i = low - 1
    for j in range(low, high):
        if arr[j]['Composite_Score'] >= pivot:  # Descending order
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
    """, language="python")

    st.markdown('<div class="section-header">3. Random Forest Performance Predictor (NEW)</div>',
                unsafe_allow_html=True)
    st.code("""
# Sem 1-1 → Sem 1-2 Performance Prediction using Random Forest
from sklearn.ensemble import RandomForestRegressor

def train_performance_predictor(df):
    features = ['Sem1_1_Mid1', 'Sem1_1_Mid2', 'Sem1_1_Internal',
                'Sem1_1_External', 'Sem1_1_Attendance_Pct']
    X = df[features].to_numpy()
    y = df['Sem1_2_Total'].to_numpy()
    
    model = RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42)
    model.fit(X, y)
    return model
    """, language="python")


# ==============================================================================
# TAB 4: AI/ML LAYER
# ==============================================================================
elif selected_tab == "🤖 AI/ML Layer":
    st.markdown(
        '<p class="hero-header">Machine Learning & Predictive Modeling</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="hero-subtitle">'
        'K-Means Clustering, OLS Regression & Random Forest Prediction'
        '</p>',
        unsafe_allow_html=True
    )

    # K-Means formulas
    st.markdown('<div class="section-header">Unsupervised K-Means Clustering</div>',
                unsafe_allow_html=True)
    st.latex(r"\text{K-Means Objective: } J = \sum_{i=1}^{k} \sum_{x \in S_i} \|x - \mu_i\|^2")
    st.latex(r"\text{Pearson Correlation: } r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}")
    st.latex(r"\text{OLS Linear Regression: } y = m \cdot x + c")

    st.markdown('<div class="section-header">K-Means Risk Cohort Definitions</div>',
                unsafe_allow_html=True)
    st.table(pd.DataFrame({
        "Risk Cohort": ["High Achievers", "Moderate Learners", "At-Risk & Backlog Vulnerable"],
        "Attendance Range": [">= 82%", "70% — 82%", "< 70%"],
        "Backlog Expectation": ["0 Backlogs", "0 — 1 Backlog", "1 — 4 Backlogs"],
        "Targeted Action": [
            "Advanced research projects & peer mentoring",
            "Attendance tracking & assignment guidance",
            "Mandatory faculty counseling & remedial classes",
        ],
    }))

    st.divider()

    # Random Forest explanation
    st.markdown(
        '<div class="section-header">Predictive Model: Random Forest Regressor (NEW)</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="content-card">
        <h4>Sem 1-1 → Sem 1-2 Performance Prediction</h4>
        <p>A <strong>Random Forest Regressor</strong> (ensemble of 100 decision trees) is trained on 
        Sem 1-1 inputs to predict individual student Sem 1-2 total performance scores.</p>
        <p><strong>Input Features (Sem 1-1):</strong> Mid-1 Marks, Mid-2 Marks, Internal Marks, External Marks, Attendance %</p>
        <p><strong>Output:</strong> Predicted Sem 1-2 Total Score (%) → Converted to 10-point GPA → Risk Classification</p>
        <p><strong>Risk Levels:</strong></p>
        <ul>
            <li><strong style="color:#10B981;">Safe (≥ 65%)</strong> — On track for good performance</li>
            <li><strong style="color:#F59E0B;">Watch (45% — 65%)</strong> — Needs monitoring and support</li>
            <li><strong style="color:#F43F5E;">Critical (< 45%)</strong> — Immediate intervention required</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# TAB 5: LIVE DASHBOARD
# ==============================================================================
elif selected_tab == "⚡ Live Dashboard":
    st.markdown(
        '<p class="hero-header">Live Student Performance Dashboard</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="hero-subtitle">'
        'Real-Time Analytics, K-Means Clustering & Interactive Visualizations'
        '</p>',
        unsafe_allow_html=True
    )

    # ── Data Loading & Processing Pipeline ──
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Dataset Controls")
    uploaded_file = st.sidebar.file_uploader("Upload Custom CSV", type=["csv"])

    if uploaded_file is not None:
        df_raw = pd.read_csv(uploaded_file)
        st.sidebar.success("Custom CSV Loaded!")
    else:
        df_raw = load_student_dataset()

    df = df_raw.copy()

    # Step 1: Matrix Operations — Composite Scores
    _, S = compute_linear_algebra_matrix_scores(df)
    df['Composite_Score'] = S

    # Step 2: K-Means Clustering & Growth Trajectory
    df, kmeans_model = perform_kmeans_clustering(df)
    df['Trajectory'] = df.apply(compute_growth_trajectory, axis=1)

    # Step 3: Statistical Trends & Advisory Notes
    stats = compute_statistical_trends(df)
    df['LLM_Advisory_Note'] = df.apply(generate_llm_advisory_note, axis=1)

    # Step 4: QuickSort Ranking
    records = df.to_dict('records')
    quicksort_student_records(records, 0, len(records) - 1)
    sorted_df = pd.DataFrame(records)
    sorted_df['Rank'] = range(1, len(sorted_df) + 1)

    # ── Advanced Sidebar Filters ──
    filtered = render_sidebar_filters(sorted_df)

    # ── KPI Metric Cards ──
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        render_metric_card("👥", str(len(filtered)), "Students Shown", accent="indigo")
    with m2:
        avg_att = filtered['Overall_Attendance_Pct'].mean()
        render_metric_card("📊", f"{avg_att:.1f}%", "Avg Attendance", accent="emerald")
    with m3:
        avg_score = filtered['Composite_Score'].mean()
        render_metric_card("🎯", f"{avg_score:.1f}%", "Avg Score", accent="cyan")
    with m4:
        total_backlogs = int(filtered['Backlogs'].sum())
        render_metric_card("📚", str(total_backlogs), "Total Backlogs",
                           delta=f"-{total_backlogs}" if total_backlogs > 0 else "0",
                           accent="amber")
    with m5:
        at_risk_cnt = len(filtered[filtered['Cohort'].str.contains('At-Risk')])
        render_metric_card("⚠️", str(at_risk_cnt), "At-Risk Students",
                           delta=f"-{at_risk_cnt}" if at_risk_cnt > 0 else "0",
                           accent="rose")

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # ── Parent Alert Simulator ──
    st.markdown(
        '<div class="section-header">Automated Parent Alert Simulator (< 75% Attendance)</div>',
        unsafe_allow_html=True
    )
    parent_alerts = generate_parent_alerts(filtered)

    with st.expander(
        f"View Simulated Parent SMS/WhatsApp Alerts ({len(parent_alerts)} Triggered)",
        expanded=False
    ):
        if parent_alerts:
            for alert in parent_alerts[:8]:
                st.markdown(f"""
                <div class="alert-card">
                    <strong>Notification to Parent of {alert['Student_Name']} ({alert['Roll_No']})</strong><br>
                    <small>{alert['Payload']}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("No alerts — all displayed students have >= 75% attendance!")

    st.divider()

    # ── Leaderboard Table ──
    st.markdown(
        '<div class="section-header">Student Leaderboard</div>',
        unsafe_allow_html=True
    )

    disp_cols = [
        'Rank', 'Roll_No', 'Student_Name', 'Gender', 'Overall_Attendance_Pct',
        'Composite_Score', 'Backlogs', 'Trajectory', 'Cohort'
    ]
    available_disp = [c for c in disp_cols if c in filtered.columns]

    st.dataframe(
        filtered[available_disp].style.format({
            'Overall_Attendance_Pct': '{:.1f}%',
            'Composite_Score': '{:.2f}%',
        }),
        use_container_width=True,
        height=350,
    )

    # Export button
    csv_bytes = filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Institutional Audit CSV Report",
        data=csv_bytes,
        file_name="institutional_audit_report.csv",
        mime="text/csv",
    )

    st.divider()

    # ── Visual Analytics Graphs ──
    st.markdown(
        '<div class="section-header">Visual Analytics</div>',
        unsafe_allow_html=True
    )

    g1, g2 = st.columns(2)

    with g1:
        fig1, ax1 = plt.subplots(figsize=(8, 5.5))
        cohort_palette = {
            "High Achievers": COLORS['success'],
            "Moderate Learners": COLORS['warning'],
            "At-Risk & Backlog Vulnerable": COLORS['danger'],
        }
        sns.scatterplot(
            data=filtered, x='Overall_Attendance_Pct', y='Composite_Score',
            hue='Cohort', palette=cohort_palette, s=80, ax=ax1, edgecolor='white', linewidth=0.5,
        )
        x_line = np.linspace(
            filtered['Overall_Attendance_Pct'].min() - 2,
            filtered['Overall_Attendance_Pct'].max() + 2, 100
        )
        y_line = stats['slope'] * x_line + stats['intercept']
        ax1.plot(x_line, y_line, color=COLORS['danger'], linestyle='--', linewidth=2,
                 label=f"OLS Trendline (r={stats['pearson_r']:.2f})")
        ax1.axvline(75, color=COLORS['warning'], linestyle=':', linewidth=1.5,
                    label='JNTUK 75% Cutoff')
        ax1.set_title("Attendance % vs Composite Score", fontweight='bold', fontsize=12)
        ax1.set_xlabel("Overall Attendance (%)")
        ax1.set_ylabel("Composite Score (%)")
        ax1.legend(fontsize=8)
        plt.tight_layout()
        st.pyplot(fig1)

    with g2:
        fig2, ax2 = plt.subplots(figsize=(8, 5.5))
        sns.countplot(
            data=filtered, x='Backlogs', hue='Gender',
            palette={
                'Female': COLORS['danger'],
                'Male': COLORS['primary']
            }, ax=ax2
        )
        ax2.set_title("Gender-Wise Backlog Distribution", fontweight='bold', fontsize=12)
        ax2.set_xlabel("Number of Backlogs")
        ax2.set_ylabel("Student Count")
        for p in ax2.patches:
            h = p.get_height()
            if h > 0:
                ax2.annotate(f'{int(h)}', (p.get_x() + p.get_width() / 2., h),
                             ha='center', va='bottom', fontweight='bold', fontsize=9)
        plt.tight_layout()
        st.pyplot(fig2)

    g3, g4 = st.columns(2)

    with g3:
        fig3, ax3 = plt.subplots(figsize=(8, 5.5))
        sns.scatterplot(
            data=filtered, x='Overall_Attendance_Pct', y='Backlogs',
            hue='Cohort', palette=cohort_palette, s=100, ax=ax3,
            edgecolor='white', linewidth=0.5,
        )
        ax3.set_title("K-Means: Attendance vs Backlogs", fontweight='bold', fontsize=12)
        ax3.set_xlabel("Overall Attendance (%)")
        ax3.set_ylabel("Backlog Count")
        plt.tight_layout()
        st.pyplot(fig3)

    with g4:
        fig4, ax4 = plt.subplots(figsize=(8, 5.5))
        means = filtered[SUBJECT_COLUMNS].mean()
        bars = ax4.bar(SUBJECT_LABELS, means.values,
                       color=[COLORS['primary'], COLORS['secondary'], COLORS['success'],
                              COLORS['info'], COLORS['warning'], COLORS['danger'], '#8B5CF6'],
                       edgecolor='white', linewidth=0.5, width=0.65)
        ax4.set_title("Class Avg Subject Performance", fontweight='bold', fontsize=12)
        ax4.set_ylabel("Average Marks (out of 100)")
        ax4.set_ylim(0, 100)
        plt.xticks(rotation=20, fontsize=9)
        for bar, v in zip(bars, means.values):
            ax4.text(bar.get_x() + bar.get_width() / 2., v + 1.5,
                     f"{v:.1f}", ha='center', fontweight='bold', fontsize=9)
        plt.tight_layout()
        st.pyplot(fig4)

    # ── NEW: Attendance Distribution Histogram ──
    g5, g6 = st.columns(2)

    with g5:
        fig5, ax5 = plt.subplots(figsize=(8, 5.5))
        sns.histplot(
            data=filtered, x='Overall_Attendance_Pct', bins=15,
            kde=True, color=COLORS['primary'], edgecolor='white', linewidth=0.5, ax=ax5,
        )
        ax5.axvline(75, color=COLORS['danger'], linestyle='--', linewidth=2,
                    label='JNTUK 75% Cutoff')
        ax5.set_title("Attendance Distribution", fontweight='bold', fontsize=12)
        ax5.set_xlabel("Overall Attendance (%)")
        ax5.set_ylabel("Student Count")
        ax5.legend(fontsize=9)
        plt.tight_layout()
        st.pyplot(fig5)

    with g6:
        # Subject performance heatmap by cohort
        if 'Cohort' in filtered.columns and len(filtered) > 0:
            fig6, ax6 = plt.subplots(figsize=(8, 5.5))
            heatmap_data = filtered.groupby('Cohort')[SUBJECT_COLUMNS].mean()
            heatmap_data.columns = SUBJECT_LABELS
            sns.heatmap(
                heatmap_data, annot=True, fmt='.1f', cmap='YlOrRd',
                linewidths=0.5, ax=ax6, cbar_kws={'label': 'Avg Marks'},
            )
            ax6.set_title("Subject Performance by Cohort", fontweight='bold', fontsize=12)
            ax6.set_ylabel("")
            plt.tight_layout()
            st.pyplot(fig6)

    st.divider()

    # ── Student Deep-Dive & AI Advisory ──
    st.markdown(
        '<div class="section-header">Student Deep-Dive & AI Advisory</div>',
        unsafe_allow_html=True
    )

    sel_student = st.selectbox(
        "Select Student",
        options=sorted_df['Student_Name'].tolist(),
        key="live_student_select"
    )
    s_row = sorted_df[sorted_df['Student_Name'] == sel_student].iloc[0]

    c1, c2 = st.columns([1, 2])
    with c1:
        render_student_profile_card(s_row)

    with c2:
        st.markdown(f"""
        <div class="content-card">
            <h4>AI Advisory Recommendation</h4>
            <p>{s_row['LLM_Advisory_Note']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Radar chart for the selected student
        fig_radar, ax_radar = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
        values = s_row[SUBJECT_COLUMNS].values.astype(float).tolist()
        values += values[:1]  # Close the polygon
        angles = np.linspace(0, 2 * np.pi, len(SUBJECT_LABELS), endpoint=False).tolist()
        angles += angles[:1]

        ax_radar.fill(angles, values, alpha=0.2, color=COLORS['primary'])
        ax_radar.plot(angles, values, color=COLORS['primary'], linewidth=2)
        ax_radar.set_xticks(angles[:-1])
        ax_radar.set_xticklabels(SUBJECT_LABELS, fontsize=8)
        ax_radar.set_ylim(0, 100)
        ax_radar.set_title(f"{sel_student} — Subject Profile", fontsize=11, fontweight='bold', pad=20)
        plt.tight_layout()
        st.pyplot(fig_radar)


# ==============================================================================
# TAB 6: ADMIN PANEL
# ==============================================================================
elif selected_tab == "📋 Admin Panel":
    # Load full dataset for admin operations
    df_admin = load_student_dataset()
    render_admin_panel(df_admin)


# ==============================================================================
# TAB 7: PREDICTIVE ANALYTICS
# ==============================================================================
elif selected_tab == "🔮 Predictive Analytics":
    st.markdown(
        '<p class="hero-header">Predictive Analytics Engine</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="hero-subtitle">'
        'Sem 1-1 → Sem 1-2 Performance Prediction using Random Forest Regressor'
        '</p>',
        unsafe_allow_html=True
    )

    # ── Load & Process Data ──
    df_pred = load_student_dataset()

    # Check if V2 columns exist
    required_pred_cols = ['Sem1_1_Mid1', 'Sem1_1_Mid2', 'Sem1_1_Internal',
                          'Sem1_1_External', 'Sem1_2_Total']
    missing_pred = [c for c in required_pred_cols if c not in df_pred.columns]

    if missing_pred:
        st.error(
            f"Predictive analytics requires the enriched V2 dataset with columns: "
            f"{missing_pred}. Please ensure 'student_records_v2.csv' is loaded."
        )
        st.stop()

    # Compute composite scores for display
    _, S = compute_linear_algebra_matrix_scores(df_pred)
    df_pred['Composite_Score'] = S

    # ── Train Model ──
    with st.spinner("Training Random Forest model..."):
        model, metrics = train_performance_predictor(df_pred)
        df_pred = predict_semester_performance(model, df_pred)

    # ── Model Performance Metrics ──
    st.markdown(
        '<div class="section-header">Model Performance</div>',
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    pm1, pm2, pm3, pm4 = st.columns(4)
    with pm1:
        render_metric_card("🎯", f"{metrics['train_r2']:.3f}", "Train R² Score", accent="indigo")
    with pm2:
        render_metric_card("📐", f"{metrics['cv_r2_mean']:.3f}", "CV R² (5-Fold)", accent="emerald")
    with pm3:
        render_metric_card("📏", f"{metrics['train_mae']:.1f}%", "Train MAE", accent="amber")
    with pm4:
        render_metric_card("±", f"{metrics['cv_r2_std']:.3f}", "CV Std Dev", accent="cyan")

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # ── Risk Distribution ──
    st.markdown(
        '<div class="section-header">Predicted Risk Distribution</div>',
        unsafe_allow_html=True
    )

    risk_counts = df_pred['Risk_Level'].value_counts()
    rc1, rc2, rc3 = st.columns(3)
    with rc1:
        safe_cnt = risk_counts.get('Safe', 0)
        render_metric_card("🟢", str(safe_cnt), "Safe (>= 65%)", accent="emerald")
    with rc2:
        watch_cnt = risk_counts.get('Watch', 0)
        render_metric_card("🟡", str(watch_cnt), "Watch (45-65%)", accent="amber")
    with rc3:
        critical_cnt = risk_counts.get('Critical', 0)
        render_metric_card("🔴", str(critical_cnt), "Critical (< 45%)", accent="rose")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Visualization Graphs ──
    v1, v2 = st.columns(2)

    with v1:
        # Predicted vs Actual scatter
        fig_pa, ax_pa = plt.subplots(figsize=(8, 5.5))
        risk_colors = {
            'Safe': COLORS['success'],
            'Watch': COLORS['warning'],
            'Critical': COLORS['danger'],
        }
        for risk_level, color in risk_colors.items():
            mask = df_pred['Risk_Level'] == risk_level
            ax_pa.scatter(
                df_pred.loc[mask, 'Sem1_2_Total'],
                df_pred.loc[mask, 'Predicted_Sem1_2_Total'],
                c=color, label=risk_level, s=60, alpha=0.8, edgecolors='white', linewidth=0.5,
            )
        # Diagonal line
        lims = [
            min(df_pred['Sem1_2_Total'].min(), df_pred['Predicted_Sem1_2_Total'].min()) - 2,
            max(df_pred['Sem1_2_Total'].max(), df_pred['Predicted_Sem1_2_Total'].max()) + 2,
        ]
        ax_pa.plot(lims, lims, '--', color='#94A3B8', linewidth=1.5, label='Perfect Prediction')
        ax_pa.set_title("Predicted vs Actual Sem 1-2 Score", fontweight='bold', fontsize=12)
        ax_pa.set_xlabel("Actual Sem 1-2 Total (%)")
        ax_pa.set_ylabel("Predicted Sem 1-2 Total (%)")
        ax_pa.legend(fontsize=8)
        plt.tight_layout()
        st.pyplot(fig_pa)

    with v2:
        # Feature Importance bar chart
        fig_fi, ax_fi = plt.subplots(figsize=(8, 5.5))
        feat_imp = metrics['feature_importances']
        feat_names = list(feat_imp.keys())
        feat_vals = list(feat_imp.values())
        # Sort by importance
        sorted_idx = np.argsort(feat_vals)
        feat_colors = [COLORS['primary'], COLORS['secondary'], COLORS['success'],
                       COLORS['warning'], COLORS['info']]
        bars = ax_fi.barh(
            [feat_names[i].replace('Sem1_1_', '').replace('_Pct', ' %') for i in sorted_idx],
            [feat_vals[i] for i in sorted_idx],
            color=[feat_colors[i % len(feat_colors)] for i in range(len(sorted_idx))],
            edgecolor='white', linewidth=0.5, height=0.55,
        )
        ax_fi.set_title("Feature Importance (Random Forest)", fontweight='bold', fontsize=12)
        ax_fi.set_xlabel("Importance Score")
        for bar, val in zip(bars, [feat_vals[i] for i in sorted_idx]):
            ax_fi.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height() / 2.,
                       f'{val:.3f}', va='center', fontweight='bold', fontsize=9)
        plt.tight_layout()
        st.pyplot(fig_fi)

    st.divider()

    # ── Prediction Leaderboard ──
    st.markdown(
        '<div class="section-header">Student Prediction Table</div>',
        unsafe_allow_html=True
    )

    pred_display = df_pred[[
        'Roll_No', 'Student_Name', 'Gender',
        'Sem1_1_Total', 'Sem1_2_Total', 'Predicted_Sem1_2_Total',
        'Predicted_GPA', 'Risk_Level', 'Prediction_Delta',
    ]].copy()
    pred_display = pred_display.sort_values('Predicted_Sem1_2_Total', ascending=False)

    st.dataframe(
        pred_display.style.format({
            'Sem1_1_Total': '{:.1f}%',
            'Sem1_2_Total': '{:.1f}%',
            'Predicted_Sem1_2_Total': '{:.1f}%',
            'Predicted_GPA': '{:.2f}',
            'Prediction_Delta': '{:+.1f}%',
        }),
        use_container_width=True,
        height=350,
    )

    st.divider()

    # ── Individual Student Drill-Down ──
    st.markdown(
        '<div class="section-header">Individual Student Drill-Down</div>',
        unsafe_allow_html=True
    )

    sel_pred_student = st.selectbox(
        "Select Student for Detailed Prediction",
        options=df_pred['Student_Name'].tolist(),
        key="pred_student_select"
    )
    s_pred_row = df_pred[df_pred['Student_Name'] == sel_pred_student].iloc[0]
    detail = get_student_prediction_detail(model, s_pred_row)

    d1, d2 = st.columns([1, 2])

    with d1:
        risk_badge = get_risk_badge_html(detail['risk_level'])
        sem1_1_total = detail.get('sem1_1_total', 'N/A')
        actual_1_2 = detail.get('actual_sem1_2_total', 'N/A')
        pred_error = detail.get('prediction_error', 'N/A')

        st.markdown(f"""
        <div class="student-profile">
            <div class="profile-name">{sel_pred_student}</div>
            <div class="profile-roll">{s_pred_row['Roll_No']} &middot; {s_pred_row['Gender']}</div>
            <hr style="margin: 0.8rem 0; border-color: #F1F5F9;">
            <div class="profile-stat"><span>Sem 1-1 Total</span><strong>{sem1_1_total}%</strong></div>
            <div class="profile-stat"><span>Actual Sem 1-2 Total</span><strong>{actual_1_2}%</strong></div>
            <div class="profile-stat"><span>Predicted Sem 1-2</span><strong>{detail['predicted_total']}%</strong></div>
            <div class="profile-stat"><span>Predicted GPA</span><strong>{detail['predicted_gpa']}</strong></div>
            <div class="profile-stat"><span>Prediction Error</span><strong>{pred_error}%</strong></div>
            <div class="profile-stat"><span>Risk Level</span>{risk_badge}</div>
        </div>
        """, unsafe_allow_html=True)

    with d2:
        # Historical vs Predicted bar comparison
        fig_comp, ax_comp = plt.subplots(figsize=(8, 5))

        feature_labels = [k.replace('Sem1_1_', '').replace('_Pct', ' %')
                          for k in detail['feature_values'].keys()]
        feature_vals = list(detail['feature_values'].values())

        bars_comp = ax_comp.bar(
            feature_labels, feature_vals,
            color=[COLORS['primary'], COLORS['secondary'], COLORS['success'],
                   COLORS['warning'], COLORS['info']],
            edgecolor='white', linewidth=0.5, width=0.55,
        )
        # Add prediction as a reference line
        ax_comp.axhline(
            y=detail['predicted_total'], color=COLORS['danger'],
            linestyle='--', linewidth=2,
            label=f"Predicted Sem 1-2: {detail['predicted_total']}%"
        )
        ax_comp.set_title(
            f"{sel_pred_student} — Sem 1-1 Features & Prediction",
            fontweight='bold', fontsize=12
        )
        ax_comp.set_ylabel("Score / Percentage")
        for bar, v in zip(bars_comp, feature_vals):
            ax_comp.text(bar.get_x() + bar.get_width() / 2., v + 0.8,
                         f"{v:.1f}", ha='center', fontweight='bold', fontsize=9)
        ax_comp.legend(fontsize=9)
        plt.tight_layout()
        st.pyplot(fig_comp)

    # ── Attendance Correlation with Prediction ──
    st.divider()
    st.markdown(
        '<div class="section-header">Attendance vs Predicted Semester Outcome</div>',
        unsafe_allow_html=True
    )

    fig_att_pred, ax_att_pred = plt.subplots(figsize=(10, 5.5))
    for risk_level, color in risk_colors.items():
        mask = df_pred['Risk_Level'] == risk_level
        ax_att_pred.scatter(
            df_pred.loc[mask, 'Overall_Attendance_Pct'],
            df_pred.loc[mask, 'Predicted_Sem1_2_Total'],
            c=color, label=risk_level, s=70, alpha=0.8,
            edgecolors='white', linewidth=0.5,
        )
    ax_att_pred.axvline(75, color=COLORS['warning'], linestyle=':', linewidth=2,
                        label='JNTUK 75% Cutoff')
    ax_att_pred.set_title("Overall Attendance vs Predicted Sem 1-2 Score",
                          fontweight='bold', fontsize=12)
    ax_att_pred.set_xlabel("Overall Attendance (%)")
    ax_att_pred.set_ylabel("Predicted Sem 1-2 Total (%)")
    ax_att_pred.legend(fontsize=9)
    plt.tight_layout()
    st.pyplot(fig_att_pred)
