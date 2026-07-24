# JNTUK R23 B.Tech AI & Data Science — Interdisciplinary Project 17
## Project Title: Smart Attendance & Performance Analyzer

---

## 1. Problem Definition
In traditional academic institutions, attendance recording and academic monitoring are typically handled as isolated, manual processes. Paper registers record attendance, while mid-term and end-semester exam marks are maintained in separate database silos.

This disconnected approach leads to critical drawbacks:
- **Delayed Intervention**: Faculty and academic mentors only identify at-risk students after semester exam results are published, when remediation is often too late.
- **Lack of Predictive Insight**: Traditional attendance systems track attendance percentages but fail to correlate attendance trends with internal assessment performance (Mid-1, Mid-2) or predict future academic failure risks.
- **Absence of Threshold Alerts**: Faculty lack automated alerts when students drop below the mandatory 75% attendance threshold.

---

## 2. Objectives
1. **Integrated Tracking**: Provide a centralized platform to record daily attendance, internal assessment scores (Mid-1, Mid-2), external exam scores, backlog counts (0-4), lab schedule adherence, and faculty qualitative remarks across both Semester 1-1 and Semester 1-2.
2. **Mathematical Integration (R23 Curriculum Alignment)**:
   - **Linear Algebra**: Formulate student feature vectors $S_i = [\text{Attendance}\_\%, \text{Mid1}, \text{Mid2}, \text{External}, \text{Backlogs}]$ and compute composite scores using dot products $S_i \cdot W$.
   - **Credit-Weighted Scoring**: Compute $\text{Score} = (\text{Internal Marks} \times 0.4) + (\text{Attendance Percentage} \times 0.6)$.
   - **Data Structures**: Implement a custom **QuickSort** algorithm from scratch with median-of-three pivot selection to rank students in $\mathcal{O}(n \log n)$ average time.
   - **File I/O**: Implement dual file reading/writing mechanics using native Python `csv` module (buffered stream) and `pandas` DataFrames.
3. **Machine Learning Risk Engine**:
   - Apply **K-Means Clustering** ($k=3$) with feature scaling (`StandardScaler`) to automatically group students into "High Achievers (Safe/Green)", "Moderate Learners (Yellow)", and "At-Risk (Red)" categories.
   - Validate cluster count selection via the **Elbow Method** and calculate silhouette scores.
   - Build a predictive regression trajectory model projecting Semester 1-2 external exam performance based on Semester 1-1 metrics.
4. **Database & Resilience Layer**:
   - Implement a PyMongo database interface for MongoDB with CRUD capabilities, session logs, and automated threshold alerts (<75%).
   - Incorporate an **automatic offline CSV fallback engine** ensuring zero downtime during offline vivas or when database connectivity is unavailable.
5. **Interactive Dashboard & Faculty Tools**:
   - Provide a 5-tab Streamlit dashboard for real-time attendance marking, threshold alerts, faculty remark logging, ML risk visualization, interactive risk prediction forms, and detailed academic reporting.

---

## 3. Cohort Scope & Academic Calendar

### Target Cohort
- **Total Enrolled**: 80 Students (2025 Admitted Batch, B.Tech AI & Data Science)
- **Gender Split**: 30 Female (`25331A0501` to `25331A0530`), 50 Male (`25331A0531` to `25331A0580`)
- **Backlog Distribution**: Realistic spread of regular students and students with 0 to 4 backlogs.

### Academic Calendar & Subject Mapping
- **Semester 1-1 (Aug 4, 2025 – Jan 21, 2026)**:
  1. Linear Algebra & Calculus (LA&C)
  2. C Programming / Computer Programming
  3. Engineering Physics
  4. Engineering Graphics
  5. Basic Electrical & Electronics Engineering (BEEE)

- **Semester 1-2 (Jan 26, 2026 – Jul 9, 2026)**:
  1. Differential Equations & Vector Calculus
  2. Python Programming
  3. Applied Chemistry
  4. Data Structures
  5. IT Workshop

---

## 4. Existing vs. Proposed System Comparison

| Feature | Existing Manual / Isolated Systems | Proposed Smart Attendance & Performance Analyzer |
| :--- | :--- | :--- |
| **Data Integration** | Disconnected paper registers & Excel sheets | Centralized MongoDB database + instant CSV fallback |
| **Performance Evaluation** | Unweighted average of exam scores | Dot product weighting ($S_i \cdot W$) + Credit-Weighted score |
| **Attendance Alerts** | Manual count check | Automated alert notification when dropping below 75% |
| **Student Ranking** | Built-in spreadsheet sort | Custom QuickSort with $\mathcal{O}(n \log n)$ algorithmic complexity |
| **Early Warning System** | None; reactive post-exam analysis | Unsupervised K-Means ($k=3$) color-coded risk tiers |
| **Future Trajectory** | Intuitive guessing by faculty | Linear Regression score trajectory model & growth graph |
| **Faculty Remarks** | Scribbled on paper margins | Searchable qualitative log per student session |
| **User Interface** | None / Static spreadsheets | Interactive 5-tab Streamlit Dashboard with custom CSS |
