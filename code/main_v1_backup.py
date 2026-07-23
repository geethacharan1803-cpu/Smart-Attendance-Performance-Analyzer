"""
================================================================================
JNTUK R23 CURRICULUM - B.TECH ARTIFICIAL INTELLIGENCE & DATA SCIENCE (YEAR 1)
PROJECT 17: SMART ATTENDANCE & PERFORMANCE ANALYZER (MASTER PROMPT VERSION)
================================================================================
Integrated Curriculum Framework:
  1. Dataset Expansion: 80 Students (30 Females, 50 Males) for 2025 Batch across 
     Semester 1-1 (Aug 4, 2025 - Jan 21, 2026) & Semester 1-2 (Jan 26, 2026 - Jul 9, 2026).
  2. R23 Coursework: Linear Algebra & Calculus, C Programming, Python Programming,
     Data Structures, Engineering Physics, BEEE, IT Workshop & Labs.
  3. Timetable Engine: Working day calculation, 2nd Saturday holidays, public holidays.
  4. Linear Algebra & Data Structures: Feature Matrices M(80x7), Dot Product S = M.W,
     and custom O(n log n) QuickSort algorithm.
  5. Machine Learning Layer: Scikit-Learn K-Means Clustering (3 Cohorts), Pearson r, 
     OLS Linear Regression, Growth Trajectory Predictor, and LLM Advisory Engineering.
  6. New Advanced Features: Automated Parent Alert System (<75% attendance), 
     Semester-over-Semester Growth Trajectory Predictor, Exportable Audit Reports.
  7. Streamlit Web Dashboard: Multi-tab navigation, custom CSS, metric cards, 
     interactive filters, and Matplotlib visual analytics graphs.
================================================================================
"""

import os
import sys
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Ensure UTF-8 output encoding for Windows terminals
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Configure Streamlit Page Layout
st.set_page_config(
    page_title="Smart Attendance & Performance Analyzer | JNTUK R23",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure Matplotlib styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica', 'sans-serif']
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

# Base directory path resolution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Custom CSS styling for glassmorphic cards and badges
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .subject-card {
        background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%);
        border-left: 5px solid #2563EB;
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    .example-box {
        background-color: #F1F5F9;
        border-left: 4px solid #10B981;
        padding: 10px 14px;
        border-radius: 6px;
        font-size: 0.92rem;
        color: #334155;
        margin-top: 8px;
        margin-bottom: 12px;
    }
    .alert-card {
        background-color: #FFF5F5;
        border: 1px solid #FEB2B2;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# MODULE 1: ACADEMIC CALENDAR & TIMETABLE TRACKING ENGINE
# JNTUK R23 Subject: Operational Calendar & Academic Planning
# ==============================================================================

class JNTUKAcademicCalendar:
    """
    [R23 Topic: Operational Analytics & Calendar Math]
    Calculates total instructional working days and lab sessions factoring in:
      - Sem 1-1 Duration: Aug 4, 2025 to Jan 21, 2026
      - Sem 1-2 Duration: Jan 26, 2026 to Jul 9, 2026
      - 2nd Saturday Holidays rule
      - Official Public Holidays
    """
    SEM_1_1_START = datetime.date(2025, 8, 4)
    SEM_1_1_END = datetime.date(2026, 1, 21)
    
    SEM_1_2_START = datetime.date(2026, 1, 26)
    SEM_1_2_END = datetime.date(2026, 7, 9)
    
    PUBLIC_HOLIDAYS = {
        datetime.date(2025, 8, 15): "Independence Day",
        datetime.date(2025, 10, 2): "Gandhi Jayanti",
        datetime.date(2025, 10, 20): "Vijaya Dasami / Dussehra",
        datetime.date(2025, 11, 1): "Diwali",
        datetime.date(2026, 1, 14): "Sankranti / Bhogi",
        datetime.date(2026, 1, 15): "Makara Sankranti",
        datetime.date(2026, 1, 26): "Republic Day",
        datetime.date(2026, 3, 4): "Maha Shivaratri",
        datetime.date(2026, 3, 25): "Holi",
        datetime.date(2026, 4, 14): "Dr. B.R. Ambedkar Jayanti",
        datetime.date(2026, 5, 1): "May Day"
    }

    @classmethod
    def get_working_days(cls, start_date: datetime.date, end_date: datetime.date) -> tuple[int, int]:
        current = start_date
        working_days = 0
        lab_slots = 0
        
        while current <= end_date:
            weekday = current.weekday()  # Mon=0, Sun=6
            if weekday != 6:  # Sunday is holiday
                is_second_saturday = (weekday == 5 and 8 <= current.day <= 14)
                is_public_holiday = current in cls.PUBLIC_HOLIDAYS
                
                if not is_second_saturday and not is_public_holiday:
                    working_days += 1
                    if weekday in [0, 2, 4]:  # Labs Mon, Wed, Fri
                        lab_slots += 1
                        
            current += datetime.timedelta(days=1)
            
        return working_days, lab_slots


# ==============================================================================
# MODULE 2: FILE I/O & DATA INGESTION (PANDAS)
# JNTUK R23 Subject: Programming & Problem Solving (File Handling Unit)
# ==============================================================================

@st.cache_data
def load_student_dataset(filepath: str) -> pd.DataFrame:
    """
    [R23 Topic: File I/O & Data Cleaning]
    Loads student academic records from CSV storage with schema validation.
    Imputes missing values with column medians.
    """
    if not os.path.exists(filepath):
        st.error(f"❌ Error: Dataset file '{filepath}' not found!")
        st.stop()
        
    df = pd.read_csv(filepath)
    
    required_cols = [
        'Roll_No', 'Student_Name', 'Gender', 'Sem1_1_Attendance_Pct', 
        'Sem1_2_Attendance_Pct', 'Overall_Attendance_Pct', 'LA_Calculus_Marks', 
        'C_Programming_Marks', 'Python_Programming_Marks', 'Data_Structures_Marks', 
        'Eng_Physics_Marks', 'BEEE_Marks', 'IT_Workshop_Marks', 'Lab_Attendance_Pct', 'Backlogs'
    ]
    for col in required_cols:
        if col not in df.columns:
            st.error(f"❌ Missing required CSV column: {col}")
            st.stop()
            
    numeric_cols = [c for c in required_cols if c not in ['Roll_No', 'Student_Name', 'Gender']]
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    
    return df


# ==============================================================================
# MODULE 3: LINEAR ALGEBRA - MATRIX TRANSFORMATION & WEIGHTED SCORING
# JNTUK R23 Subject: Linear Algebra & Calculus (Matrices & Vector Spaces)
# ==============================================================================

def compute_linear_algebra_matrix_scores(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """
    [R23 Topic: Linear Algebra - Feature Matrix & Linear Combinations]
    Feature Matrix M (80 x 7) dot product with Credit Weight Vector W (7 x 1):
    LA&Calculus: 18% | C Prog: 16% | Python: 16% | DS: 16% | Physics: 12% | BEEE: 12% | IT Workshop: 10%
    """
    subject_cols = [
        'LA_Calculus_Marks', 'C_Programming_Marks', 'Python_Programming_Marks',
        'Data_Structures_Marks', 'Eng_Physics_Marks', 'BEEE_Marks', 'IT_Workshop_Marks'
    ]
    M = df[subject_cols].to_numpy()
    W = np.array([0.18, 0.16, 0.16, 0.16, 0.12, 0.12, 0.10])
    S = np.dot(M, W)
    return M, S


# ==============================================================================
# MODULE 4: DATA STRUCTURES - QUICKSORT ALGORITHM
# JNTUK R23 Subject: Data Structures (Sorting Algorithms)
# ==============================================================================

def quicksort_student_records(records: list[dict], low: int, high: int) -> None:
    """
    [R23 Topic: Data Structures - QuickSort (Divide and Conquer)]
    Custom QuickSort algorithm sorting student records by 'Composite_Score' in DESCENDING order.
    """
    if low < high:
        pi = _partition(records, low, high)
        quicksort_student_records(records, low, pi - 1)
        quicksort_student_records(records, pi + 1, high)

def _partition(arr: list[dict], low: int, high: int) -> int:
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
# JNTUK R23 Subject: AI & Machine Learning Foundations
# ==============================================================================

def perform_kmeans_clustering(df: pd.DataFrame) -> tuple[pd.DataFrame, KMeans]:
    """
    [R23 Topic: Machine Learning - Unsupervised K-Means Clustering]
    Segments 80 students into 3 Risk Cohorts:
      - Cohort 0: High Achievers 🟢
      - Cohort 1: Moderate Learners 🟡
      - Cohort 2: At-Risk & Backlog Vulnerable 🔴
    """
    features = ['Overall_Attendance_Pct', 'Composite_Score', 'Backlogs']
    X = df[features].to_numpy()
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_scaled)
    
    temp_df = df.copy()
    temp_df['Cluster'] = cluster_labels
    cluster_means = temp_df.groupby('Cluster')['Composite_Score'].mean().sort_values(ascending=False)
    
    rank_to_cohort = {
        cluster_means.index[0]: "High Achievers 🟢",
        cluster_means.index[1]: "Moderate Learners 🟡",
        cluster_means.index[2]: "At-Risk & Backlog Vulnerable 🔴"
    }
    
    df['Cohort'] = [rank_to_cohort[c] for c in cluster_labels]
    return df, kmeans

def compute_growth_trajectory(row: pd.Series) -> str:
    """
    [NEW FEATURE]: Semester-over-Semester Growth Trajectory Predictor (1-1 vs 1-2)
    """
    delta = row['Sem1_2_Attendance_Pct'] - row['Sem1_1_Attendance_Pct']
    if delta > 3.0:
        return "Upward Trajectory 📈"
    elif delta < -3.0:
        return "Declining Trajectory 📉"
    else:
        return "Stable Progression ➖"

def generate_parent_alerts(df: pd.DataFrame) -> list[dict]:
    """
    [NEW FEATURE]: Automated SMS/WhatsApp Parent Alert Simulator for Attendance < 75%
    """
    alerts = []
    at_risk_df = df[df['Overall_Attendance_Pct'] < 75.0]
    for _, row in at_risk_df.iterrows():
        alerts.append({
            'Roll_No': row['Roll_No'],
            'Student_Name': row['Student_Name'],
            'Attendance_Pct': row['Overall_Attendance_Pct'],
            'Backlogs': row['Backlogs'],
            'Payload': f"ALERT: Parent of {row['Student_Name']} ({row['Roll_No']}): Attendance is {row['Overall_Attendance_Pct']}%, BELOW 75% JNTUK cutoff. Backlogs: {row['Backlogs']}. Mandatory counseling required."
        })
    return alerts

def compute_statistical_trends(df: pd.DataFrame) -> dict:
    """
    [R23 Topic: AI/ML Foundations - Pearson Correlation & OLS Linear Regression]
    """
    x = df['Overall_Attendance_Pct'].to_numpy()
    y = df['Composite_Score'].to_numpy()
    
    r = np.corrcoef(x, y)[0, 1]
    m, c = np.polyfit(x, y, 1)
    
    return {'pearson_r': r, 'slope': m, 'intercept': c}

def generate_llm_advisory_note(row: pd.Series) -> str:
    """
    [R23 Topic: LLM Advisory Prompt Engineering]
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
        return f"CRITICAL: Mandatory faculty counseling for {name} ({att}% att, {backlogs} backlogs). Schedule remedial classes."


# ==============================================================================
# SIDEBAR NAVIGATION MENU (5 EXACT TABS)
# ==============================================================================
st.sidebar.image("https://img.icons8.com/color/96/graduation-cap.png", width=70)
st.sidebar.title("Navigation Menu")
st.sidebar.caption("JNTUK R23 B.Tech AI & DS (2025 Batch)")

selected_tab = st.sidebar.radio(
    "Select Section:",
    [
        "Home",
        "Subjects used in project",
        "Programming used",
        "AI/ML layer",
        "LIVE DEMO"
    ]
)

st.sidebar.divider()
st.sidebar.info("💡 **Project 17**: Smart Attendance & Performance Analyzer\n\nBatch: 2025-2029 (80 Students)")


# ==============================================================================
# TAB 1: HOME
# ==============================================================================
if selected_tab == "Home":
    st.markdown('<p class="main-header">🎓 Smart Attendance & Performance Analyzer</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">JNTUK R23 Curriculum — B.Tech Artificial Intelligence & Data Science (2025 Batch)</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📌 Project Overview & Master Blueprint")
        st.write("""
        Welcome to **Project 17: Smart Attendance & Performance Analyzer**! 
        This application tracks **80 students (30 Females, 50 Males)** from the 2025 AI & DS batch across Semester 1-1 and Semester 1-2.
        
        The platform correlates attendance percentage with examination marks, lab performance, and backlog counts using **Linear Algebra Matrix Multiplication**, **Custom QuickSort**, and **Unsupervised K-Means Clustering**.
        """)
        
        # Calendar working days stats
        w_days_1_1, labs_1_1 = JNTUKAcademicCalendar.get_working_days(JNTUKAcademicCalendar.SEM_1_1_START, JNTUKAcademicCalendar.SEM_1_1_END)
        w_days_1_2, labs_1_2 = JNTUKAcademicCalendar.get_working_days(JNTUKAcademicCalendar.SEM_1_2_START, JNTUKAcademicCalendar.SEM_1_2_END)
        
        st.markdown("### 📅 Academic Calendar & Timetable Stats")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Sem 1-1 Working Days", f"{w_days_1_1} Days")
        k2.metric("Sem 1-1 Lab Slots", f"{labs_1_1} Labs")
        k3.metric("Sem 1-2 Working Days", f"{w_days_1_2} Days")
        k4.metric("Sem 1-2 Lab Slots", f"{labs_1_2} Labs")
        
    with col2:
        st.subheader("📋 Batch Information")
        st.info("""
        **Institution**: JNTUK Curriculum R23
        
        **Branch**: AI & DS (2025 Batch)
        
        **Total Strength**: 80 Students
        
        **Gender Ratio**: 30 Girls | 50 Boys
        
        **Semesters**: 1-1 & 1-2
        """)


# ==============================================================================
# TAB 2: SUBJECTS USED IN PROJECT
# ==============================================================================
elif selected_tab == "Subjects used in project":
    st.markdown('<p class="main-header">📚 Integrated JNTUK R23 Subjects & Practical Applications</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Detailed Explanations & Concrete Examples on 80 Student Records</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="subject-card">
        <h4>1. Programming & Problem Solving (File I/O & CSV Ingestion)</h4>
        <p><strong>R23 Syllabus Topic:</strong> File Handling, Pandas CSV Ingestion, Exception Handling, Data Imputation.</p>
        <p><strong>Application on 80 Students:</strong> Ingests <code>sample_data/student_records.csv</code> containing 80 rows and 15 academic columns (roll numbers <code>25A91A4201</code> to <code>25A91A4280</code>). Validates schema integrity and performs median imputation for any missing marks.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="example-box">
        <strong>💡 Beginner Example (File I/O in Action):</strong><br>
        <code>import pandas as pd</code><br>
        <code>df = pd.read_csv('sample_data/student_records.csv')  # Ingests 80 student records</code><br>
        <code>df['LA_Calculus_Marks'].fillna(df['LA_Calculus_Marks'].median(), inplace=True)  # Clean missing data</code>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("""
    <div class="subject-card">
        <h4>2. Linear Algebra & Calculus (Feature Matrix & Vector Dot Product)</h4>
        <p><strong>R23 Syllabus Topic:</strong> Vectors, 2D Feature Matrices, Credit Weight Vectors, Matrix Transformations.</p>
        <p><strong>Application on 80 Students:</strong> Represents all 80 students as an 80 &times; 7 Feature Matrix M, where each row contains 7 normalized subject marks. Computes composite performance scores in a single linear algebra step: <em>S = M &middot; W</em>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.latex(r"M_{80 \times 7} = \begin{bmatrix} m_{1,1} & m_{1,2} & \dots & m_{1,7} \\ m_{2,1} & m_{2,2} & \dots & m_{2,7} \\ \vdots & \vdots & \ddots & \vdots \\ m_{80,1} & m_{80,2} & \dots & m_{80,7} \end{bmatrix}, \quad W_{7 \times 1} = \begin{bmatrix} 0.18 \\ 0.16 \\ 0.16 \\ 0.16 \\ 0.12 \\ 0.12 \\ 0.10 \end{bmatrix}")
    st.latex(r"S_{80 \times 1} = M_{80 \times 7} \cdot W_{7 \times 1}")
    
    st.markdown("""
    <div class="example-box">
        <strong>💡 Concrete Numerical Example (Student 25A91A4201 - Ananya Verma):</strong><br>
        • Marks Vector: <code>[LA=56.2, C=59.6, Python=52.9, DS=50.2, Physics=46.7, BEEE=42.6, IT=45.0]</code><br>
        • Weight Vector W: <code>[0.18, 0.16, 0.16, 0.16, 0.12, 0.12, 0.10]</code><br>
        • Composite Score S = (56.2&times;0.18) + (59.6&times;0.16) + (52.9&times;0.16) + (50.2&times;0.16) + (46.7&times;0.12) + (42.6&times;0.12) + (45.0&times;0.10) = <strong>51.35%</strong>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("""
    <div class="subject-card">
        <h4>3. Data Structures (QuickSort Algorithm)</h4>
        <p><strong>R23 Syllabus Topic:</strong> Array Data Structures, Divide-and-Conquer Sorting, Partitioning Logic.</p>
        <p><strong>Application on 80 Students:</strong> Custom QuickSort algorithm sorts the array of 80 student dictionary records by composite score in descending order in average <em>O(n log n)</em> time complexity.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.latex(r"\text{Average Time Complexity: } \mathcal{O}(n \log_2 n) = 80 \times \log_2(80) \approx 506 \text{ comparisons}")
    
    st.markdown("""
    <div class="example-box">
        <strong>💡 QuickSort Partitioning Example:</strong><br>
        1. Select last student's composite score as Pivot (e.g. 72.5%).<br>
        2. Partition array: Students with score &ge; 72.5% move to the left; students &lt; 72.5% move to the right.<br>
        3. Recursively repeat on left and right partitions until all 80 students are sorted into Leaderboard Ranks #1 to #80.
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# TAB 3: PROGRAMMING USED
# ==============================================================================
elif selected_tab == "Programming used":
    st.markdown('<p class="main-header">💻 Programming & Data Structures Logic</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Step-by-Step Explanation of Code Algorithms & Matrix Math</p>', unsafe_allow_html=True)
    
    st.subheader("1. Linear Algebra Matrix Multiplication (NumPy)")
    st.code("""
# Feature Matrix M (80 x 7) multiplied by Weight Vector W (7 x 1)
def compute_linear_algebra_matrix_scores(df: pd.DataFrame):
    subject_cols = [
        'LA_Calculus_Marks', 'C_Programming_Marks', 'Python_Programming_Marks',
        'Data_Structures_Marks', 'Eng_Physics_Marks', 'BEEE_Marks', 'IT_Workshop_Marks'
    ]
    M = df[subject_cols].to_numpy()
    W = np.array([0.18, 0.16, 0.16, 0.16, 0.12, 0.12, 0.10]) # Weight vector summing to 1.0
    S = np.dot(M, W) # Matrix Dot Product S = M . W
    return M, S
    """, language="python")
    
    st.subheader("2. Custom QuickSort Algorithm (Data Structures)")
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
        if arr[j]['Composite_Score'] >= pivot: # Descending order
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
    """, language="python")


# ==============================================================================
# TAB 4: AI/ML LAYER
# ==============================================================================
elif selected_tab == "AI/ML layer":
    st.markdown('<p class="main-header">🤖 Unsupervised Machine Learning & Clustering</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Scikit-Learn K-Means Clustering & OLS Linear Regression</p>', unsafe_allow_html=True)
    
    st.latex(r"\text{K-Means Objective: } J = \sum_{i=1}^{k} \sum_{x \in S_i} \|x - \mu_i\|^2")
    st.latex(r"\text{Pearson Correlation: } r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}")
    st.latex(r"\text{OLS Linear Regression: } y = m \cdot x + c")
    
    st.subheader("🎯 K-Means Risk Cohort Definitions")
    st.table(pd.DataFrame({
        "Risk Cohort": ["High Achievers 🟢", "Moderate Learners 🟡", "At-Risk & Backlog Vulnerable 🔴"],
        "Attendance Range": ["≥ 82%", "70% - 82%", "< 70%"],
        "Backlog Expectation": ["0 Backlogs", "0 - 1 Backlog", "1 - 4 Backlogs"],
        "Targeted Action": [
            "Advanced research projects & peer mentoring",
            "Attendance tracking & assignment guidance",
            "Mandatory faculty counseling & remedial classes"
        ]
    }))


# ==============================================================================
# TAB 5: LIVE DEMO (INTERACTIVE APPLICATION)
# ==============================================================================
elif selected_tab == "LIVE DEMO":
    st.markdown('<p class="main-header">⚡ Live Student Performance Analytics Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-Time Ingestion, K-Means Clustering & Interactive Visualizations</p>', unsafe_allow_html=True)
    
    default_csv = os.path.join(BASE_DIR, "sample_data", "student_records.csv")
    
    st.sidebar.subheader("⚙️ Dataset Controls")
    uploaded_file = st.sidebar.file_uploader("Upload Custom CSV", type=["csv"])
    
    if uploaded_file is not None:
        df_raw = pd.read_csv(uploaded_file)
        st.sidebar.success("Custom CSV Loaded!")
    else:
        df_raw = load_student_dataset(default_csv)
        
    df = df_raw.copy()
    
    # Step 1: Matrix Operations
    _, S = compute_linear_algebra_matrix_scores(df)
    df['Composite_Score'] = S
    
    # Step 2: Machine Learning - K-Means Clustering & Trajectory
    df, kmeans_model = perform_kmeans_clustering(df)
    df['Trajectory'] = df.apply(compute_growth_trajectory, axis=1)
    
    # Step 3: Statistical Trends & Prompts
    stats = compute_statistical_trends(df)
    df['LLM_Advisory_Note'] = df.apply(generate_llm_advisory_note, axis=1)
    
    # Step 4: QuickSort Ranking
    records = df.to_dict('records')
    quicksort_student_records(records, 0, len(records) - 1)
    sorted_df = pd.DataFrame(records)
    sorted_df['Rank'] = range(1, len(sorted_df) + 1)
    
    # -------------------------------------------------------------------------
    # Top KPI Metrics Cards
    # -------------------------------------------------------------------------
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("Total Students", f"{len(sorted_df)}")
    with m2:
        st.metric("Class Avg Att. %", f"{sorted_df['Overall_Attendance_Pct'].mean():.1f}%")
    with m3:
        st.metric("Class Avg Score", f"{sorted_df['Composite_Score'].mean():.1f}%")
    with m4:
        total_backlogs = int(sorted_df['Backlogs'].sum())
        st.metric("Total Backlogs", f"{total_backlogs}", delta=f"-{total_backlogs}" if total_backlogs > 0 else "0", delta_color="inverse")
    with m5:
        at_risk_cnt = len(sorted_df[sorted_df['Cohort'].str.contains('At-Risk')])
        st.metric("At-Risk Students", f"{at_risk_cnt}", delta=f"-{at_risk_cnt}" if at_risk_cnt > 0 else "0", delta_color="inverse")
        
    st.divider()
    
    # -------------------------------------------------------------------------
    # NEW FEATURE: Automated Parent Alert Simulator & Growth Trajectories
    # -------------------------------------------------------------------------
    st.subheader("🔔 Automated Parent Alert Simulator (< 75% Attendance)")
    parent_alerts = generate_parent_alerts(sorted_df)
    
    with st.expander(f"⚠️ View Simulated Parent SMS/WhatsApp Alerts ({len(parent_alerts)} Triggered Alerts)"):
        for alert in parent_alerts[:6]:  # Display top 6
            st.markdown(f"""
            <div class="alert-card">
                <strong>📲 Notification to Parent of {alert['Student_Name']} ({alert['Roll_No']})</strong><br>
                <small>{alert['Payload']}</small>
            </div>
            """, unsafe_allow_html=True)
            
    st.divider()
    
    # -------------------------------------------------------------------------
    # Leaderboard Table & Filtering
    # -------------------------------------------------------------------------
    st.subheader("🏆 Student Roster Leaderboard")
    
    f1, f2, f3 = st.columns([1, 1, 1])
    with f1:
        gender_sel = st.multiselect("Filter by Gender:", options=['Female', 'Male'], default=['Female', 'Male'])
    with f2:
        cohort_sel = st.multiselect("Filter by K-Means Cohort:", options=sorted_df['Cohort'].unique(), default=sorted_df['Cohort'].unique())
    with f3:
        backlog_sel = st.selectbox("Filter by Backlogs:", options=["All", "0 Backlogs", "Has Backlogs (>0)"])
        
    filtered = sorted_df[
        (sorted_df['Gender'].isin(gender_sel)) & 
        (sorted_df['Cohort'].isin(cohort_sel))
    ]
    if backlog_sel == "0 Backlogs":
        filtered = filtered[filtered['Backlogs'] == 0]
    elif backlog_sel == "Has Backlogs (>0)":
        filtered = filtered[filtered['Backlogs'] > 0]
        
    disp_cols = [
        'Rank', 'Roll_No', 'Student_Name', 'Gender', 'Overall_Attendance_Pct', 
        'Composite_Score', 'Backlogs', 'Trajectory', 'Cohort'
    ]
    st.dataframe(
        filtered[disp_cols].style.format({'Overall_Attendance_Pct': '{:.1f}%', 'Composite_Score': '{:.2f}%'}),
        use_container_width=True,
        height=320
    )
    
    # NEW FEATURE: Export Institutional Audit Report CSV
    csv_bytes = filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Institutional Audit CSV Report",
        data=csv_bytes,
        file_name="institutional_audit_report.csv",
        mime="text/csv"
    )
    
    st.divider()
    
    # -------------------------------------------------------------------------
    # Visual Analytics Dashboard Graphs
    # -------------------------------------------------------------------------
    st.subheader("📊 Visual Analytics Graphs")
    
    g1, g2 = st.columns(2)
    
    with g1:
        fig1, ax1 = plt.subplots(figsize=(8, 5.5))
        sns.scatterplot(data=filtered, x='Overall_Attendance_Pct', y='Composite_Score', hue='Cohort', s=80, ax=ax1)
        
        x_line = np.linspace(filtered['Overall_Attendance_Pct'].min() - 2, filtered['Overall_Attendance_Pct'].max() + 2, 100)
        y_line = stats['slope'] * x_line + stats['intercept']
        ax1.plot(x_line, y_line, color='#dc2626', linestyle='--', linewidth=2, label=f"OLS Trendline (r={stats['pearson_r']:.2f})")
        ax1.axvline(75, color='#f59e0b', linestyle=':', label='JNTUK 75% Cutoff')
        
        ax1.set_title("Attendance % vs Composite Performance Score", fontweight='bold')
        ax1.set_xlabel("Overall Attendance Percentage (%)")
        ax1.set_ylabel("Composite Performance Score (%)")
        ax1.legend(fontsize=8)
        st.pyplot(fig1)
        
    with g2:
        fig2, ax2 = plt.subplots(figsize=(8, 5.5))
        sns.countplot(data=filtered, x='Backlogs', hue='Gender', palette='Set2', ax=ax2)
        ax2.set_title("Gender-Wise Backlog Distribution", fontweight='bold')
        ax2.set_xlabel("Number of Backlogs")
        ax2.set_ylabel("Student Count")
        for p in ax2.patches:
            height = p.get_height()
            if height > 0:
                ax2.annotate(f'{int(height)}', (p.get_x() + p.get_width() / 2., height),
                             ha='center', va='bottom', fontweight='bold', fontsize=9)
        st.pyplot(fig2)
        
    g3, g4 = st.columns(2)
    
    with g3:
        fig3, ax3 = plt.subplots(figsize=(8, 5.5))
        sns.scatterplot(data=filtered, x='Overall_Attendance_Pct', y='Backlogs', hue='Cohort', palette='bright', s=100, ax=ax3)
        ax3.set_title("K-Means Clustering: Attendance vs Backlogs", fontweight='bold')
        ax3.set_xlabel("Overall Attendance Percentage (%)")
        ax3.set_ylabel("Backlog Count")
        st.pyplot(fig3)
        
    with g4:
        fig4, ax4 = plt.subplots(figsize=(8, 5.5))
        subj_cols = ['LA_Calculus_Marks', 'C_Programming_Marks', 'Python_Programming_Marks', 'Data_Structures_Marks', 'Eng_Physics_Marks', 'BEEE_Marks', 'IT_Workshop_Marks']
        subj_labels = ['LA & Calc', 'C Prog', 'Python', 'Data Struct', 'Physics', 'BEEE', 'IT Workshop']
        means = filtered[subj_cols].mean()
        
        sns.barplot(x=subj_labels, y=means.values, hue=subj_labels, palette='crest', legend=False, ax=ax4)
        ax4.set_title("Class Average Subject Performance (out of 100)", fontweight='bold')
        ax4.set_ylabel("Average Marks")
        ax4.set_ylim(0, 100)
        plt.xticks(rotation=20)
        for i, v in enumerate(means.values):
            ax4.text(i, v + 1.5, f"{v:.1f}", ha='center', fontweight='bold', fontsize=9)
        st.pyplot(fig4)

    st.divider()
    
    # -------------------------------------------------------------------------
    # Individual Student Deep-Dive Advisor Card
    # -------------------------------------------------------------------------
    st.subheader("👤 Student Deep-Dive & AI Advisory Note")
    
    sel_student = st.selectbox("Select Student:", options=sorted_df['Student_Name'].tolist())
    s_row = sorted_df[sorted_df['Student_Name'] == sel_student].iloc[0]
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.info(f"**Roll No**: {s_row['Roll_No']}\n\n**Gender**: {s_row['Gender']}\n\n**Rank**: #{s_row['Rank']}\n\n**Attendance**: {s_row['Overall_Attendance_Pct']}%\n\n**Composite Score**: {s_row['Composite_Score']:.2f}%\n\n**Growth Trajectory**: {s_row['Trajectory']}\n\n**Backlogs**: {s_row['Backlogs']}")
    with c2:
        st.warning(f"**K-Means Cohort**: {s_row['Cohort']}")
        st.success(f"🤖 **LLM Advisory Recommendation Note**:\n\n\"{s_row['LLM_Advisory_Note']}\"")
