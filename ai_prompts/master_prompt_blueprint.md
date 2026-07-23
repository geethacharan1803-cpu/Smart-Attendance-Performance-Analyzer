# Master Prompt Blueprint - Project 17: Smart Attendance & Performance Analyzer

> **Role & Persona**: Act as an Expert AI/ML Architect, Senior Python Developer, and Academic Mentor for First-Year B.Tech Artificial Intelligence and Data Science (AI & DS) students under the **JNTUK R23 Curriculum**.

---

## 🎯 Master Prompt Goal
Build, expand, and refine **"Project 17: Smart Attendance & Performance Analyzer"** in VS Code into an enterprise-grade, interactive Streamlit web application. The application bridges core 1st-year JNTUK R23 engineering subjects—*Programming in C/Python*, *Linear Algebra & Calculus*, *Data Structures*, and *AI/ML Foundations*—to analyze attendance-performance correlations and automate student risk intervention.

---

## 📋 1. Project Blueprint & Dataset Specifications

- **Target Audience & Batch**: B.Tech AI & DS 2025 Batch (Roll Numbers: `25A91A4201` to `25A91A4280`).
- **Student Strength**: Exactly **80 Students** (30 Females, 50 Males).
- **Academic Timeline & Semesters**:
  - **Semester 1-1**: August 4, 2025 – January 21, 2026 (Working days calculation excluding Sundays, 2nd Saturdays, and JNTUK Public Holidays).
  - **Semester 1-2**: January 26, 2026 – July 9, 2026.
- **Academic Parameters Tracked**:
  - `Roll_No`, `Student_Name`, `Gender` (`Female`/`Male`).
  - `Sem1_1_Attendance_Pct`, `Sem1_2_Attendance_Pct`, `Overall_Attendance_Pct`.
  - 7 Core R23 Subject Marks (scaled 0-100): `LA_Calculus_Marks`, `C_Programming_Marks`, `Python_Programming_Marks`, `Data_Structures_Marks`, `Eng_Physics_Marks`, `BEEE_Marks`, `IT_Workshop_Marks`.
  - `Lab_Attendance_Pct` and `Backlogs` count (0 to 4 backlogs).

---

## 📐 2. Subject & Mathematical Integration Engine

### A. Programming & Problem Solving (File I/O)
- **Concept**: CSV Ingestion, Schema Validation, Median Imputation, Data Persistence.
- **Python Function**: `load_student_dataset(filepath)` using `pd.read_csv()`. Missing numerical values are imputed via $x_{\text{missing}} \leftarrow \text{median}(X_{\text{col}})$.

### B. Linear Algebra & Calculus (Matrices & Dot Products)
- **Concept**: 2D Feature Matrix $M_{80 \times 7}$, Credit Weight Vector $W_{7 \times 1}$, Dot Product $S = M \cdot W$.
- **Formulas**:
  $$M_{80 \times 7} = \begin{bmatrix} m_{1,1} & \dots & m_{1,7} \\ \vdots & \ddots & \vdots \\ m_{80,1} & \dots & m_{80,7} \end{bmatrix}, \quad W_{7 \times 1} = \begin{bmatrix} 0.18 \\ 0.16 \\ 0.16 \\ 0.16 \\ 0.12 \\ 0.12 \\ 0.10 \end{bmatrix}$$
  $$S_{80 \times 1} = M \cdot W$$
- **Concrete Example (Student 25A91A4201 - Ananya Verma)**:
  $$S_1 = (56.2 \times 0.18) + (59.6 \times 0.16) + (52.9 \times 0.16) + (50.2 \times 0.16) + (46.7 \times 0.12) + (42.6 \times 0.12) + (45.0 \times 0.10) = 51.35\%$$

### C. Data Structures (QuickSort Algorithm)
- **Concept**: Array Structures, Divide-and-Conquer Partitioning, QuickSort Algorithm.
- **Complexity**: Average time complexity $\mathcal{O}(n \log_2 n) \approx 80 \times \log_2(80) \approx 506$ comparisons.
- **Implementation**: Custom `quicksort_student_records()` function sorting student dictionary objects by composite score in descending order.

---

## 🤖 3. Advanced AI/ML Layer & Risk Analytics

### A. Unsupervised K-Means Clustering (`sklearn.cluster.KMeans`)
- **Normalized Feature Space**: `[Overall_Attendance_Pct, Composite_Score, Backlogs]` standardized via `StandardScaler()`.
- **Clustering Objective**: $J = \sum_{i=1}^{k} \sum_{x \in S_i} \|x - \mu_i\|^2$ with $k=3$.
- **Risk Cohorts**:
  1. 🟢 **High Achievers**: Attendance $\ge 82\%$, 0 Backlogs.
  2. 🟡 **Moderate Learners**: Attendance $70\% - 82\%$, 0-1 Backlog.
  3. 🔴 **At-Risk & Backlog Vulnerable**: Attendance $< 70\%$, 1-4 Backlogs.

### B. Statistical Correlation & OLS Linear Regression
- **Pearson $r$**: $r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}$
- **OLS Regression Line**: $y = m \cdot x + c$ mapping overall attendance % to predicted exam score.

---

## ⚡ 4. Interactive Dashboard (Streamlit Architecture)

### 5 Required Sidebar Navigation Tabs:
1. 🏠 **Home**: Executive overview, JNTUK R23 curriculum context, working day metrics, and batch stats.
2. 📚 **Subjects used in project**: Educational breakdown of 4 core subjects with LaTeX formulas and 80-student numerical examples.
3. 💻 **Programming used**: Code walkthrough snippets explaining Pandas File I/O, Matrix Multiplication, and pure Python QuickSort algorithms.
4. 🤖 **AI/ML layer**: Mathematical theory of K-Means clustering, Pearson correlation, OLS regression, and decision matrices.
5. ⚡ **LIVE DEMO**: Real-time student performance dashboard with KPI metric cards, leaderboard dataframe with filters, scatter correlation plot, gender-wise backlog distribution bar chart, K-Means cohort scatter plot, subject average performance bars, and student deep-dive selector.

---

## 🚀 5. Advanced Feature Roadmap & Extension Specifications

### Feature A: Automated Parent Alert Simulation (SMS / WhatsApp)
- **Logic**: Iterates through all students with `Overall_Attendance_Pct < 75.0%`.
- **Notification Payload**:
  ```text
  [JNTUK R23 ATTENDANCE ALERT]
  To: Parent of {Student_Name} ({Roll_No})
  Notice: Your ward's attendance is {Attendance_Pct}%, which is BELOW the mandatory 75% JNTUK cutoff. 
  Current Backlogs: {Backlogs}. Mandatory faculty counseling scheduled.
  ```

### Feature B: Semester Growth Trajectory Predictor (1-1 vs 1-2)
- **Delta Metric**: $\Delta_{\text{Att}} = \text{Sem1\_2\_Attendance\_Pct} - \text{Sem1\_1\_Attendance\_Pct}$.
- **Trajectory Classification**:
  - `Upward Trajectory 📈`: $\Delta_{\text{Att}} > +3.0\%$
  - `Stable Progression ➖`: $-3.0\% \le \Delta_{\text{Att}} \le +3.0\%$
  - `Declining Trajectory 📉`: $\Delta_{\text{Att}} < -3.0\%$

### Feature C: Institutional Audit Report Generator (PDF / CSV)
- **Output Formats**: Exportable CSV report (`processed_student_performance.csv`) and PDF institutional report for HOD / Faculty review.
- **Report Content**: Class average metrics, gender-wise backlog summary, at-risk student list, and intervention recommendations.
