# Master Prompt: JNTUK R23 B.Tech AI & Data Science — Interdisciplinary Project 17
## Project Title: "Smart Attendance & Performance Analyzer"

---

### ROLE DEFINITION
Act as an expert **AI/ML Architect, Full-Stack Python Developer, Database Engineer, UI/UX Designer, and Academic Technical Writer**. Your task is to build a complete, end-to-end, production-quality, deployable interdisciplinary project for **JNTUK R23 B.Tech AI & Data Science, Project 17: "Smart Attendance & Performance Analyzer"**.

---

### 1. PROJECT SCOPE & COHORT SPECIFICATIONS
- **Target Cohort**: Exactly 80 students total (30 Female students, 50 Male students) from the 2025 admitted B.Tech AI & Data Science batch.
- **Roll Number Scheme**:
  - Female students: `25331A0501` to `25331A0530` (30 total)
  - Male students: `25331A0531` to `25331A0580` (50 total)
- **Academic Status**: Realistic spread containing regular performers, high achievers, and students carrying 0 to 4 backlogs.

---

### 2. ACADEMIC CALENDAR & CURRICULUM SUBJECT MAPPING

#### Semester 1-1 Timeline: August 4, 2025 – January 21, 2026
- **Subjects**:
  1. Linear Algebra & Calculus (LA&C)
  2. C Programming / Basic Coding
  3. Engineering Physics
  4. Engineering Graphics
  5. Basic Electrical & Electronics Engineering (BEEE)

#### Semester 1-2 Timeline: January 26, 2026 – July 9, 2026
- **Subjects**:
  1. Differential Equations & Vector Calculus
  2. Python Programming
  3. Applied Chemistry
  4. Data Structures
  5. IT Workshop

---

### 3. MATHEMATICAL & ALGORITHMIC FORMULATIONS

#### 3.1 Linear Algebra — Feature Vectors, Matrix Scoring & Covariance
- Represent each student $i$ as a 5-dimensional feature vector:
  $$S_i = [\text{Attendance}\_\%, \text{Mid1}, \text{Mid2}, \text{External}, \text{Backlog\_Count}]$$
- Build class cohort matrix $X \in \mathbb{R}^{80 \times 5}$.
- Define a weight vector $W = [0.25, 0.15, 0.15, 0.35, -0.10]$ balancing academic contributions:
  - Attendance (25%), Mid-1 (15%), Mid-2 (15%), External Marks (35%), Backlog Penalty (-10%).
- Calculate Composite Score via vector dot product:
  $$\text{Score}_i = S_i \cdot W = \sum_{j=0}^{4} (S_i[j] \times W[j])$$
- Incorporate specific credit weight formula for internal evaluation:
  $$\text{Weighted Score} = (\text{Internal Marks} \times 0.4) + (\text{Attendance Percentage} \times 0.6)$$
- Compute matrix covariance & live **Pearson correlation coefficient** ($r$) between attendance percentage and external exam scores.

#### 3.2 Data Structures — Custom QuickSort Algorithm
- Implement **QuickSort from scratch** in Python (without using built-in `sorted()` or `.sort()`) to rank student performance vectors in descending order.
- Use **Median-of-Three Pivot Selection** ($\text{median}(\text{low}, \text{mid}, \text{high})$) to avoid $\mathcal{O}(n^2)$ worst-case behavior on pre-sorted data.
- Provide time and space complexity derivations:
  - Best/Average Case: $\mathcal{O}(n \log n)$
  - Worst Case: $\mathcal{O}(n^2)$ (mitigated by pivot strategy)
  - Space Complexity: $\mathcal{O}(\log n)$ auxiliary stack depth.

#### 3.3 File I/O Mechanics
- Implement dual file handling:
  1. Native Python `csv` module with `with open(...)` for low-memory buffered stream reading.
  2. Pandas DataFrames (`pd.read_csv`, `df.to_csv`) for vector calculations and ML transformations.

---

### 4. SMART ADMIN & DAILY ATTENDANCE SYSTEM
- **Interactive Admin Control Panel**:
  - Daily session attendance logger allowing faculty to select date, subject, present roll numbers, and absent roll numbers.
  - Faculty qualitative remarks text entry logged per session.
  - Automated threshold alerts highlighting students falling below 65% or 75% attendance.
  - Real-time Daily Present and Daily Absent list generation with instant database sync.

---

### 5. PREDICTIVE ANALYTICS & MACHINE LEARNING LAYER

#### 5.1 Unsupervised Student Risk Clustering (K-Means)
- Features: $[\text{attendance}\_\%, \text{avg}\_\text{marks}, \text{backlog}\_\text{count}]$ where $\text{avg}\_\text{marks} = (\text{Mid1} + \text{Mid2} + \text{External})/3$.
- Feature Normalization: Mandatory `StandardScaler` to handle magnitude scale differences (Euclidean distance sensitivity).
- Deterministic Label Mapping: Sort cluster centroids by mean composite score to assign:
  - Highest centroid $\rightarrow$ **High Achievers** (Green)
  - Middle centroid $\rightarrow$ **Moderate Learners** (Yellow)
  - Lowest centroid $\rightarrow$ **At-Risk** (Red)
- Evaluation: **Elbow Method Curve** ($k=1..8$) and **Silhouette Score** calculation.

#### 5.2 Performance Trajectory Prediction (Sem 1-1 to Sem 1-2)
- Train a `LinearRegression` model taking Semester 1-1 metrics ($\text{Attendance}, \text{Mid1}, \text{Mid2}, \text{Backlog Count}$) to project Semester 1-2 external exam performance.
- Interactive Single-Student Risk Calculator Form: Accepts custom student inputs and computes immediate predicted external score, risk cluster, and actionable faculty recommendation.

---

### 6. DATABASE INTEGRATION & OFFLINE FALLBACK (PyMongo)
- PyMongo client connecting via environment variable `MONGODB_URI` (`mongodb://localhost:27017` or Atlas).
- Collections: `students`, `attendance_logs`, `academic_records`, `ml_results`.
- **Automatic Offline Fallback**: Wrap all Mongo operations in `try/except`. If MongoDB connection fails, gracefully route all reads and writes to `sample_data/student_records.csv` so offline viva demonstrations never crash.

---

### 7. UI/UX DESIGN & STREAMLIT DASHBOARD
- Custom dark glassmorphic CSS theme (`code/styles.py`) with metric cards, risk badges, rounded containers, and math callouts.
- **Sidebar Controls (AND-logic multi-filters)**:
  - Gender multi-select (Female, Male)
  - Semester multi-select (Sem 1-1, Sem 1-2)
  - Attendance % range slider
  - Backlog count filter (0 to 4)
  - Risk cluster filter (High Achievers, Moderate Learners, At-Risk)
- **5 Multi-Tab Navigation**:
  1. **📊 1. Home Overview**: Cohort overview, summary statistics, timeline details, attendance & backlog charts.
  2. **📐 2. Subjects Used**: Linear Algebra LaTeX math formulas, worked arithmetic examples, QuickSort derivations, File I/O mechanics.
  3. **💻 3. Programming Stack**: Tech stack breakdown (Python, Pandas, NumPy, PyMongo, Scikit-Learn, Matplotlib, Streamlit) with justifications.
  4. **🤖 4. AI/ML Engine**: K-Means cluster scatter plot, Elbow curve plot, Silhouette metric, Regression model metrics, and interactive student risk calculator.
  5. **⚡ 5. LIVE DEMO & Admin**: Daily attendance marking portal, QuickSort re-ranking student records table, ML re-clustering, and CSV downloads.

---

### 8. PRODUCTION DEPLOYMENT & VERSION PINNING
- `requirements.txt`: Pin exact dependency versions (`streamlit==1.35.0`, `pandas==2.2.2`, `numpy==1.26.4`, `scikit-learn==1.5.0`, `matplotlib==3.9.0`, `pymongo==4.7.3`, `python-docx==1.1.2`).
- `runtime.txt`: `python-3.11`
- `.python-version`: `3.11`
- `vercel.json`: Vercel serverless function configuration.
- `.env.example`: Environment variable template.

---

### 9. ACADEMIC DELIVERABLES
- `problem_statement.md`: Problem formulation, objectives, curriculum mapping, existing vs. proposed comparison.
- `ai_prompts/prompts_used.md`: AI prompt log diary for R23 compliance.
- `report/Project17_Report.docx`: Complete submission-ready academic report DOCX file with worked math, architecture diagrams, results, and 8 Examiner Viva Q&A items.
- `README.md`: Documented project guide with folder structure rationale and pre-deployment checklist.
