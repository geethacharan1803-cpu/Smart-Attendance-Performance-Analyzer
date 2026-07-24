"""
Streamlit Web Application Entry Point
JNTUK R23 B.Tech AI & Data Science — Interdisciplinary Project 17
"Smart Attendance & Performance Analyzer"
"""

import os
import sys
import importlib

CODE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CODE_DIR)
sys.path.insert(0, CODE_DIR)
sys.path.insert(0, ROOT_DIR)

from datetime import date, timedelta
import pandas as pd
import numpy as np
import streamlit as st

import styles
import db
import data_utils
import ml_engine
import visualizations

# Force importlib reload so Streamlit hot-reloading always loads updated light theme styles
importlib.reload(styles)
importlib.reload(db)
importlib.reload(data_utils)
importlib.reload(ml_engine)
importlib.reload(visualizations)

from styles import inject_custom_css
from db import db_manager
from data_utils import (
    compute_class_scores,
    custom_quicksort,
    compute_pearson_correlation,
    SEM_1_1_SUBJECTS,
    SEM_1_2_SUBJECTS,
    ATTENDANCE_THRESHOLD
)
from ml_engine import ml_engine
from visualizations import (
    plot_attendance_vs_marks,
    plot_gender_backlog_distribution,
    plot_growth_trajectory,
    plot_kmeans_clusters,
    plot_elbow_curve,
    plot_student_drilldown,
    export_all_charts
)

st.set_page_config(
    page_title="Smart Attendance & Performance Analyzer | JNTUK R23 Project 17",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

inject_custom_css()


def main():
    raw_students = db_manager.get_all_students()
    scored_students = compute_class_scores(raw_students, semester="sem1_1")
    
    ml_results = ml_engine.run_kmeans_clustering(scored_students, semester="sem1_1", k=3)
    clustered_students = ml_results["clustered_students"]
    regression_results = ml_engine.train_predictive_trajectory_model(clustered_students)
    dataset = regression_results["predictions"]

    export_all_charts(dataset, ml_results)

    # Header Card
    st.markdown("""
    <div class="header-card">
        <div class="header-title">🎓 Smart Attendance & Performance Analyzer</div>
        <div class="header-subtitle">JNTUK R23 B.Tech Curriculum — Department of CSE (AI & Data Science) | Cohort 2025 Admitted Batch (80 Students: 30 Female, 50 Male)</div>
    </div>
    """, unsafe_allow_html=True)

    # ==========================================================================
    # MAIN-PAGE HIGH-CONTRAST COHORT CONTROL PANEL
    # ==========================================================================
    with st.expander("🎛️ Main Control Panel — Filter & Cohort Controls", expanded=True):
        fc1, fc2, fc3, fc4, fc5 = st.columns(5)
        
        with fc1:
            selected_sem = st.selectbox("Active Semester", options=["Sem 1-1 (Aug 2025 - Jan 2026)", "Sem 1-2 (Jan 2026 - Jul 2026)"])
            sem_pfx = "sem1_1" if "1-1" in selected_sem else "sem1_2"

        with fc2:
            genders = sorted(list(set(s.get("gender", "") for s in dataset)))
            selected_genders = st.multiselect("Gender", options=genders, default=genders)

        with fc3:
            att_range = st.slider("Attendance % Range", min_value=0.0, max_value=100.0, value=(40.0, 100.0))

        with fc4:
            back_col = f"{sem_pfx}_backlog_count"
            backlog_options = sorted(list(set(int(s.get(back_col, 0)) for s in dataset)))
            selected_backlogs = st.multiselect("Backlogs (0-4)", options=backlog_options, default=backlog_options)

        with fc5:
            color_risks = ["Safe", "Moderate", "High Risk"]
            selected_risk_tiers = st.multiselect("Risk Tier", options=color_risks, default=color_risks)

    # Apply COMBINED AND-LOGIC FILTERING
    filtered_dataset = []
    for s in dataset:
        cond_gender = s.get("gender") in selected_genders
        att_val = float(s.get(f"{sem_pfx}_attendance_pct", s.get("attendance_pct", 0)))
        cond_att = att_range[0] <= att_val <= att_range[1]
        back_val = int(s.get(back_col, s.get("backlog_count", 0)))
        cond_backlog = back_val in selected_backlogs
        c_risk = s.get("color_risk", "Moderate")
        cond_risk = c_risk in selected_risk_tiers

        if cond_gender and cond_att and cond_backlog and cond_risk:
            filtered_dataset.append(s)

    # 5 NAVIGATION TABS
    tabs = st.tabs([
        "📊 1. Home Overview",
        "📐 2. Subjects Used & Formulas",
        "💻 3. Programming Stack",
        "🤖 4. AI/ML Engine & Analytics",
        "⚡ 5. LIVE DEMO & Admin Panel"
    ])

    # --------------------------------------------------------------------------
    # TAB 1: HOME OVERVIEW
    # --------------------------------------------------------------------------
    with tabs[0]:
        st.subheader("Cohort Overview & Demographics")

        c1, c2, c3, c4, c5 = st.columns(5)
        total_st = len(filtered_dataset)
        avg_att_val = np.mean([float(s.get(f"{sem_pfx}_attendance_pct", 0)) for s in filtered_dataset]) if total_st > 0 else 0.0
        avg_score_val = np.mean([s["composite_score"] for s in filtered_dataset]) if total_st > 0 else 0.0
        total_backlogs_val = sum(int(s.get(f"{sem_pfx}_backlog_count", 0)) for s in filtered_dataset)
        alert_count = sum(1 for s in filtered_dataset if float(s.get(f"{sem_pfx}_attendance_pct", 0)) < ATTENDANCE_THRESHOLD)

        with c1:
            st.markdown(f'<div class="stat-card"><div class="stat-val">{total_st}</div><div class="stat-lbl">Filtered Students</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="stat-card"><div class="stat-val">{avg_att_val:.1f}%</div><div class="stat-lbl">Avg Attendance</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="stat-card"><div class="stat-val">{avg_score_val:.2f}</div><div class="stat-lbl">Avg Dot Product Score</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="stat-card"><div class="stat-val">{total_backlogs_val}</div><div class="stat-lbl">Total Backlogs</div></div>', unsafe_allow_html=True)
        with c5:
            st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#ef4444 !important">{alert_count}</div><div class="stat-lbl">< 75% Att Alerts</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if alert_count > 0:
            st.error(f"🚨 **Automated Attendance Threshold Alert:** {alert_count} student(s) currently fall below the mandatory 75.0% JNTUK R23 attendance threshold!")

        with st.expander("📌 JNTUK R23 Curriculum Academic Calendar & Subjects Mapping", expanded=True):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("""
                **Semester 1-1 (Aug 4, 2025 – Jan 21, 2026):**
                1. Linear Algebra & Calculus (LA&C)
                2. C Programming / Computer Programming
                3. Engineering Physics
                4. Engineering Graphics
                5. Basic Electrical & Electronics Engineering (BEEE)
                """)
            with col_b:
                st.markdown("""
                **Semester 1-2 (Jan 26, 2026 – Jul 9, 2026):**
                1. Differential Equations & Vector Calculus (DEVC)
                2. Communicative English
                3. Applied Chemistry
                4. Data Structures
                5. Basic Civil & Mechanical Engineering (BCME)
                """)

        # Visualizations Grid
        g1, g2, g3 = st.columns(3)
        with g1:
            fig_att = plot_attendance_vs_marks(filtered_dataset, semester_pfx=sem_pfx, save_png=False)
            st.pyplot(fig_att)
        with g2:
            fig_gen = plot_gender_backlog_distribution(filtered_dataset, semester_pfx=sem_pfx, save_png=False)
            st.pyplot(fig_gen)
        with g3:
            fig_growth = plot_growth_trajectory(filtered_dataset, save_png=False)
            st.pyplot(fig_growth)

    # --------------------------------------------------------------------------
    # TAB 2: SUBJECTS USED IN PROJECT & MATHEMATICAL TRANSPARENCY
    # --------------------------------------------------------------------------
    with tabs[1]:
        st.subheader("R23 Curriculum Mathematical & Algorithmic Integration")

        with st.expander("🧮 1. Linear Algebra — Feature Vector Formulations & Composite Scoring", expanded=True):
            st.markdown("""
            Each student is represented as a 5-dimensional feature vector:
            
            **Feature Vector S = [Attendance %, Mid-1 Marks, Mid-2 Marks, External Exam Score, Backlog Count]**
            
            **Weight Vector W = [0.25, 0.15, 0.15, 0.35, -0.10]**
            
            - **Composite Dot Product Score** = S · W = (Attendance % × 0.25) + (Mid-1 × 0.15) + (Mid-2 × 0.15) + (External × 0.35) - (Backlogs × 0.10)
            - **Credit-Weighted Score** = (Internal Marks × 0.4) + (Attendance % × 0.6)
            """)

            st.markdown("---")
            st.markdown("#### 🧮 Single-Student Step-by-Step Arithmetic Scaling Calculator")
            st.caption("Select any student from the 80-student cohort to inspect how their specific attendance and exam marks alter the composite dot product and credit-weighted scores.")

            student_options = [f"{s['roll_no']} - {s['name']}" for s in filtered_dataset]
            if student_options:
                calc_student_str = st.selectbox("Select Student to Calculate", options=student_options, key="calc_student_select")
                calc_roll = calc_student_str.split(" - ")[0]
                cs = next((s for s in filtered_dataset if s["roll_no"] == calc_roll), None)

                if cs:
                    att = float(cs.get(f"{sem_pfx}_attendance_pct", 0))
                    m1 = float(cs.get(f"{sem_pfx}_mid1", 0))
                    m2 = float(cs.get(f"{sem_pfx}_mid2", 0))
                    ext = float(cs.get(f"{sem_pfx}_external", 0))
                    back = int(cs.get(f"{sem_pfx}_backlog_count", 0))

                    t_att = att * 0.25
                    t_m1 = m1 * 0.15
                    t_m2 = m2 * 0.15
                    t_ext = ext * 0.35
                    t_back = back * -0.10
                    comp_val = t_att + t_m1 + t_m2 + t_ext + t_back

                    internal_avg = (m1 + m2) / 2.0
                    cred_val = internal_avg * 0.4 + att * 0.6

                    st.markdown(f"""
                    <div class="math-callout">
                        <h4 style="color:#0284c7; margin-top:0;">Numerical Step-by-Step Arithmetic: {cs['name']} ({cs['roll_no']})</h4>
                        <p>• <strong>Feature Vector:</strong> <code>S = [{att}%, {m1}, {m2}, {ext}, {back}]</code></p>
                        <p>• <strong>Weight Vector:</strong> <code>W = [0.25, 0.15, 0.15, 0.35, -0.10]</code></p>
                        <br>
                        <strong>Term Multiplication Details:</strong><br>
                        1. Attendance Term = {att} × 0.25 = <strong>{t_att:.3f}</strong><br>
                        2. Mid-1 Term = {m1} × 0.15 = <strong>{t_m1:.3f}</strong><br>
                        3. Mid-2 Term = {m2} × 0.15 = <strong>{t_m2:.3f}</strong><br>
                        4. External Exam Term = {ext} × 0.35 = <strong>{t_ext:.3f}</strong><br>
                        5. Backlog Penalty Term = {back} × -0.10 = <strong>{t_back:.3f}</strong><br><br>
                        <p style="font-size:1.1rem; color:#0284c7;"><strong>Composite Score (Dot Product) = {t_att:.3f} + {t_m1:.3f} + {t_m2:.3f} + {t_ext:.3f} + ({t_back:.3f}) = {comp_val:.2f}</strong></p>
                        <p style="font-size:1.1rem; color:#16a34a;"><strong>Credit-Weighted Score = ({internal_avg:.1f} × 0.4) + ({att} × 0.6) = {internal_avg*0.4:.2f} + {att*0.6:.2f} = {cred_val:.2f}</strong></p>
                    </div>
                    """, unsafe_allow_html=True)

            att_vals = [float(s.get(f"{sem_pfx}_attendance_pct", 0)) for s in filtered_dataset]
            ext_vals = [float(s.get(f"{sem_pfx}_external", 0)) for s in filtered_dataset]
            r_val = compute_pearson_correlation(att_vals, ext_vals)
            st.info(f"💡 **Matrix Covariance Insight:** Pearson Correlation Coefficient between Attendance and External Marks across cohort: **r = {r_val:.4f}**")

        with st.expander("⚡ 2. Data Structures — Custom QuickSort Algorithm & Complexity Analysis", expanded=True):
            st.markdown("""
            Instead of relying on Python's built-in `sorted()`, we implement **QuickSort from scratch** with Median-of-Three pivot selection:

            - **Pivot Selection**: median(low, mid, high) element chosen as pivot to prevent worst-case partitions.
            - **Best / Average Time Complexity**: O(n log n) when partitions divide balanced subarrays.
            - **Worst Time Complexity**: O(n^2) (mitigated via median pivot selection).
            - **Auxiliary Space Complexity**: O(log n) recursive stack depth.
            """)

        with st.expander("📁 3. File I/O Mechanics — Low-Memory Stream vs. Pandas DataFrames", expanded=True):
            st.markdown("""
            Dual File I/O persistence using native Python `csv.DictReader` (buffered low-memory stream) and Pandas DataFrames (`read_csv`, `to_csv`).
            """)

    # --------------------------------------------------------------------------
    # TAB 3: PROGRAMMING STACK
    # --------------------------------------------------------------------------
    with tabs[2]:
        st.subheader("Technology Stack & Engineering Rationale")

        p1, p2, p3 = st.columns(3)
        with p1:
            st.markdown('<div class="content-box"><h3>🐍 Python 3.11</h3><p>Core programming runtime providing dynamic typing and numerical modules.</p></div>', unsafe_allow_html=True)
            st.markdown('<div class="content-box"><h3>📊 Pandas & NumPy</h3><p>Matrix dot products, vector operations, and tabular data transformation.</p></div>', unsafe_allow_html=True)
        with p2:
            st.markdown('<div class="content-box"><h3>🍃 PyMongo & MongoDB</h3><p>Document database persistence for student profiles, daily attendance logs, and ML results.</p></div>', unsafe_allow_html=True)
            st.markdown('<div class="content-box"><h3>🤖 Scikit-Learn</h3><p>StandardScaler normalization, K-Means (k=3), Silhouette metrics, Linear Regression & Random Forest.</p></div>', unsafe_allow_html=True)
        with p3:
            st.markdown('<div class="content-box"><h3>🎨 Streamlit 1.35</h3><p>Interactive web application framework with reactive controls and custom Light theme CSS.</p></div>', unsafe_allow_html=True)
            st.markdown('<div class="content-box"><h3>📈 Matplotlib & Seaborn</h3><p>High-contrast analytics plots and PNG graph exporter.</p></div>', unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # TAB 4: AI/ML LAYER & INDIVIDUAL DRILL-DOWN INSPECTOR
    # --------------------------------------------------------------------------
    with tabs[3]:
        st.subheader("Unsupervised K-Means Clustering & Ensemble Trajectory Models")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Optimal Clusters (k)", "3 Clusters")
        m2.metric("Silhouette Score", f"{ml_results['silhouette_score']}")
        m3.metric("Random Forest R²", f"{regression_results['r2_rf']}")
        m4.metric("Linear Reg. R²", f"{regression_results['r2_linear']}")

        col_ml1, col_ml2 = st.columns(2)
        with col_ml1:
            fig_cluster = plot_kmeans_clusters(filtered_dataset, save_png=False)
            st.pyplot(fig_cluster)
        with col_ml2:
            fig_elbow = plot_elbow_curve(ml_results["elbow_data"], save_png=False)
            st.pyplot(fig_elbow)

        st.markdown("---")

        # Dedicated Individual Student Profile Panel
        st.subheader("🔍 Dedicated Individual Student Academic Profile Panel")
        st.caption("Select any student from the 80-student cohort to inspect specific Mid-1, Mid-2, Internal, External, Semester Marks, Backlogs, Projected GPA, and drill-down comparison graph.")

        student_list = [f"{s['roll_no']} - {s['name']}" for s in filtered_dataset]
        if student_list:
            selected_student_str = st.selectbox("Select Student Profile to Inspect", options=student_list, key="inspect_student_select")
            sel_roll = selected_student_str.split(" - ")[0]
            selected_student = next((s for s in filtered_dataset if s["roll_no"] == sel_roll), None)

            if selected_student:
                sd1, sd2 = st.columns([1, 1.2])

                risk_badge_class = "badge-safe" if selected_student.get("color_risk") == "Safe" else "badge-moderate" if selected_student.get("color_risk") == "Moderate" else "badge-high-risk"

                with sd1:
                    st.markdown(f"""
                    <div class="content-box">
                        <h3 style="color:#0284c7; margin-top:0;">👤 Student Profile: {selected_student['name']}</h3>
                        <p><strong>Roll Number:</strong> <code>{selected_student['roll_no']}</code> | <strong>Gender:</strong> {selected_student['gender']}</p>
                        <p><strong>Academic Status:</strong> <span class="{risk_badge_class}">{selected_student.get('color_risk', 'Moderate')} Tier</span></p>
                        <table style="width:100%; border-collapse:collapse; margin-top:10px; font-size:0.9rem;">
                            <tr style="border-bottom:1px solid #cbd5e1;"><td style="padding:6px; font-weight:bold;">Sem 1-1 Attendance %</td><td style="padding:6px;">{selected_student.get('sem1_1_attendance_pct', 0)}%</td></tr>
                            <tr style="border-bottom:1px solid #cbd5e1;"><td style="padding:6px; font-weight:bold;">Sem 1-1 Mid-1 Marks (/30)</td><td style="padding:6px;">{selected_student.get('sem1_1_mid1', 0)}</td></tr>
                            <tr style="border-bottom:1px solid #cbd5e1;"><td style="padding:6px; font-weight:bold;">Sem 1-1 Mid-2 Marks (/30)</td><td style="padding:6px;">{selected_student.get('sem1_1_mid2', 0)}</td></tr>
                            <tr style="border-bottom:1px solid #cbd5e1;"><td style="padding:6px; font-weight:bold;">Sem 1-1 External Exam (/70)</td><td style="padding:6px;">{selected_student.get('sem1_1_external', 0)}</td></tr>
                            <tr style="border-bottom:1px solid #cbd5e1;"><td style="padding:6px; font-weight:bold;">Sem 1-1 Backlog Count</td><td style="padding:6px;">{selected_student.get('sem1_1_backlog_count', 0)}</td></tr>
                            <tr style="border-bottom:1px solid #cbd5e1;"><td style="padding:6px; font-weight:bold;">Projected Sem 1-2 External Marks</td><td style="padding:6px; font-weight:bold; color:#0284c7;">{selected_student.get('predicted_sem1_2_external', 0)} / 70</td></tr>
                            <tr><td style="padding:6px; font-weight:bold;">Predicted Sem 1-2 GPA</td><td style="padding:6px; font-weight:bold; color:#16a34a; font-size:1.1rem;">{selected_student.get('predicted_sem1_2_gpa', 0.0)} / 10.0</td></tr>
                        </table>
                        <p style="margin-top:12px;"><strong>Faculty Remarks:</strong> <em>"{selected_student.get('sem1_1_remarks', 'Regular student.')}"</em></p>
                    </div>
                    """, unsafe_allow_html=True)

                with sd2:
                    fig_drill = plot_student_drilldown(selected_student)
                    st.pyplot(fig_drill)

        st.markdown("---")
        st.subheader("🔮 Interactive Single-Student Trajectory Predictor Form")

        with st.form("risk_predictor_form"):
            fc1, fc2, fc3, fc4 = st.columns(4)
            with fc1:
                in_att = st.number_input("Attendance %", min_value=0.0, max_value=100.0, value=76.0, step=1.0)
            with fc2:
                in_mid1 = st.number_input("Mid-1 Score (out of 30)", min_value=0.0, max_value=30.0, value=21.0, step=0.5)
            with fc3:
                in_mid2 = st.number_input("Mid-2 Score (out of 30)", min_value=0.0, max_value=30.0, value=22.0, step=0.5)
            with fc4:
                in_backlog = st.number_input("Backlog Count", min_value=0, max_value=4, value=0, step=1)

            submit_btn = st.form_submit_button("Run AI Trajectory Prediction 🚀")

        if submit_btn:
            pred_res = ml_engine.predict_individual_student(in_att, in_mid1, in_mid2, in_backlog)
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.success(f"**Predicted Sem 1-2 External Score**: {pred_res['predicted_external_score']} / 70")
                st.info(f"**Predicted Sem 1-2 GPA**: {pred_res['predicted_gpa']} / 10.0")
                st.info(f"**Predicted Risk Tier**: {pred_res['predicted_cluster']}")
            with res_col2:
                st.warning(f"**Actionable Recommendation**: {pred_res['recommendation']}")

    # --------------------------------------------------------------------------
    # TAB 5: LIVE DEMO & SMART ADMIN PANEL
    # --------------------------------------------------------------------------
    with tabs[4]:
        st.subheader("Smart Admin Control Panel & Daily Attendance System")

        with st.expander("📝 Mark Today's Class Session Attendance", expanded=True):
            with st.form("mark_attendance_form"):
                d_col1, d_col2, d_col3, d_col4 = st.columns(4)
                with d_col1:
                    att_date = st.date_input("Session Date", value=date.today())
                with d_col2:
                    att_sem_choice = st.selectbox("Semester", ["Sem 1-1", "Sem 1-2"])
                with d_col3:
                    active_subjects = SEM_1_1_SUBJECTS if att_sem_choice == "Sem 1-1" else SEM_1_2_SUBJECTS
                    att_subject = st.selectbox("Subject", active_subjects)
                with d_col4:
                    session_status_type = st.selectbox("Session Type", ["Present / Working Day", "Absent", "Public Holiday", "Second Saturday"])

                all_rolls = [f"{s['roll_no']} - {s['name']}" for s in dataset]
                absent_selected = st.multiselect("Select Absent Students", options=all_rolls)
                faculty_remark_text = st.text_input("Faculty Remarks / Notes", value="Theory lecture & practical lab completed.")

                submit_att = st.form_submit_button("Submit Attendance Log to DB & Trigger Alerts 📤")

                if submit_att:
                    absent_rolls = [x.split(" - ")[0] for x in absent_selected]
                    present_rolls = [s["roll_no"] for s in dataset if s["roll_no"] not in absent_rolls]

                    res_log = db_manager.insert_attendance_log(
                        date_str=str(att_date),
                        subject=att_subject,
                        semester=att_sem_choice,
                        present_rolls=present_rolls,
                        absent_rolls=absent_rolls,
                        faculty_remarks=f"[{session_status_type}] {faculty_remark_text}"
                    )
                    st.success(f"Attendance logged! {len(present_rolls)} Present, {len(absent_rolls)} Absent. Session Type: {session_status_type}")

                    if res_log.get("triggered_alerts"):
                        for alt in res_log["triggered_alerts"]:
                            st.error(f"🚨 **ALERT:** Student {alt['roll_no']} ({alt['name']}) dropped below 75% attendance! New attendance: {alt['new_att']}%")

        # Historical Range Selection Filter for Admin Attendance Logs
        st.markdown("#### 📅 Historical Attendance Range Inspector")
        range_col1, range_col2 = st.columns(2)
        with range_col1:
            time_range = st.selectbox("Historical Range Filter", ["Last 1 Week", "Last 1 Month", "Whole Academic Semester"])
        with range_col2:
            st.info(f"Showing session roster logs for: **{time_range}** ({selected_sem})")

        # Daily Present & Absent Lists View
        st.subheader("📊 Session Roster Status (Present & Absent Lists)")
        roster_col1, roster_col2 = st.columns(2)
        with roster_col1:
            st.markdown("#### ✔️ Daily Present List")
            present_data = [{"roll_no": s["roll_no"], "name": s["name"], "status": "✔️ Present"} for s in filtered_dataset if float(s.get(f"{sem_pfx}_attendance_pct", 0)) >= ATTENDANCE_THRESHOLD]
            st.dataframe(pd.DataFrame(present_data))
        with roster_col2:
            st.markdown("#### ❌ Daily Absent / At-Risk List (<75%)")
            absent_data = [{"roll_no": s["roll_no"], "name": s["name"], "attendance_%": s.get(f"{sem_pfx}_attendance_pct"), "status": "❌ At-Risk", "faculty_remark": s.get(f"{sem_pfx}_remarks", "Needs counseling.")} for s in filtered_dataset if float(s.get(f"{sem_pfx}_attendance_pct", 0)) < ATTENDANCE_THRESHOLD]
            st.dataframe(pd.DataFrame(absent_data))

        st.subheader("📋 Cohort Academic Roster & Color-Coded Risk Analysis")

        sort_by_quicksort = st.checkbox("Enable Custom QuickSort (Rank by Composite Score Descending)", value=True)

        display_data = list(filtered_dataset)
        if sort_by_quicksort:
            display_data = custom_quicksort(display_data, key="composite_score", descending=True)

        df_display = pd.DataFrame(display_data)

        cols_to_show = ["roll_no", "name", "gender", f"{sem_pfx}_attendance_pct", f"{sem_pfx}_mid1", f"{sem_pfx}_mid2", f"{sem_pfx}_external", f"{sem_pfx}_backlog_count", "composite_score", "credit_weighted_score", "predicted_sem1_2_gpa", "color_risk", "trajectory_status"]
        available_cols = [c for c in cols_to_show if c in df_display.columns]

        st.dataframe(df_display[available_cols])

        st.subheader("📥 Export Dataset & Reports")
        down_col1, down_col2 = st.columns(2)
        with down_col1:
            csv_data = df_display.to_csv(index=False).encode('utf-8')
            st.download_button("Download Clustered Students CSV 📄", data=csv_data, file_name="clustered_students.csv", mime="text/csv")
        with down_col2:
            st.download_button("Download Risk Predictions CSV 📊", data=csv_data, file_name="risk_predictions.csv", mime="text/csv")


if __name__ == "__main__":
    main()
