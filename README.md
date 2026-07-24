# JNTUK R23 B.Tech AI & Data Science — Interdisciplinary Project 17
## Smart Attendance & Performance Analyzer

A production-quality, deployable interdisciplinary academic project developed for the **JNTUK R23 B.Tech AI & Data Science Curriculum (Project 17)** for the **2025 admitted cohort (80 Students: 30 Female, 50 Male)**.

---

## 📂 Folder Structure Explanation (R23 Rubric Requirement)

Per JNTUK R23 engineering evaluation standards, projects are assessed on structured software engineering practices. Below is the full directory tree and technical justification for each folder:

```
smart-attendance-performance-analyzer/
│
├── problem_statement.md          # Comprehensive problem definition, objectives, and system comparison
├── requirements.txt              # Fully pinned Python dependency versions for deployment reproducibility
├── runtime.txt                   # Explicit Python version pin (python-3.11)
├── .python-version               # Backup Python runtime configuration file
├── .env.example                  # Environment variable configuration template (MONGODB_URI)
├── vercel.json                   # Vercel serverless functions configuration file
├── .gitignore                    # Version control exclusion rules for cache and credentials
├── README.md                     # Full documentation, folder guide, and deployment checklist
│
├── code/                         # Modular Python backend, ML, data structures, and UI code
│   ├── __init__.py               # Package initialization marker
│   ├── main.py                   # Streamlit web application entry point (5 interactive tabs)
│   ├── db.py                     # PyMongo MongoDB CRUD manager + Automatic Offline CSV Fallback & 75% Alerts
│   ├── data_utils.py             # Feature matrices, dot product S_i · W, credit weights, custom QuickSort, File I/O
│   ├── ml_engine.py              # StandardScaler, K-Means (k=3), Elbow plot, Silhouette, Trajectory Regression
│   ├── visualizations.py         # Matplotlib dark glassmorphic chart builders & PNG exporter
│   └── styles.py                 # Injected custom CSS theme styling for Streamlit
│
├── sample_data/
│   ├── student_records.csv       # Synthetic dataset of 80 students (30 Female, 50 Male) across Sem 1-1 & 1-2
│   └── generate_dataset.py       # Reproducible script used to generate synthetic student records
│
├── output/
│   ├── clustered_students.csv    # Exported K-Means cluster assignments & risk labels
│   ├── risk_predictions.csv     # Exported Linear Regression trajectory projections
│   └── charts/                   # Saved high-resolution PNG image exports of visual graphs
│
├── ai_prompts/
│   ├── prompts_used.md           # Responsible AI prompt log diary (required for R23 Viva evaluation)
│   └── master_prompt.md          # Master prompt reference specification
│
└── report/
    ├── Project17_Report.docx     # Full submission-ready academic report document
    ├── generate_report.py        # Automated python-docx script generating the academic report
    └── screenshots/              # Reserved folder for UI application screenshots
```

---

## 🧮 Academic Subject Integrations (R23 Alignment)

1. **Linear Algebra & Calculus**:
   - **Feature Vector**: $S_i = [\text{Attendance}\_\%, \text{Mid1}, \text{Mid2}, \text{External}, \text{Backlogs}]$
   - **Weight Vector**: $W = [0.25, 0.15, 0.15, 0.35, -0.10]$
   - **Composite Score**: $\text{Score}_i = S_i \cdot W = \sum_{j=0}^{4} (S_i[j] \times W[j])$
   - **Credit-Weighted Score**: $\text{Score} = (\text{Internal Marks} \times 0.4) + (\text{Attendance Percentage} \times 0.6)$
   - **Matrix Covariance**: Live Pearson correlation coefficient ($r$) computed between attendance percentage and external exam marks.

2. **Data Structures (Arrays & Sorting)**:
   - **Custom QuickSort Implementation**: Sorts student objects by composite score descending without `sorted()`.
   - **Pivot Strategy**: Median-of-three selection ($\text{median}(\text{low}, \text{mid}, \text{high})$) to prevent $\mathcal{O}(n^2)$ worst-case behavior.
   - **Complexity**: Best/Average $\mathcal{O}(n \log n)$, Worst $\mathcal{O}(n^2)$ (mitigated), Auxiliary Space $\mathcal{O}(\log n)$.

3. **Database & Resilient Fallback Engine**:
   - PyMongo engine connecting to MongoDB (`MONGODB_URI`).
   - **Offline Fallback**: If MongoDB connection times out or fails (e.g. offline viva exam), the system seamlessly operates on `sample_data/student_records.csv` without throwing unhandled exceptions.
   - **Automated Alerts**: Triggers notification when a student's attendance drops below 75%.

4. **AI/ML Layer (Scikit-Learn)**:
   - Unsupervised K-Means ($k=3$) with `StandardScaler` feature normalization.
   - Deterministic centroid sorting mapping clusters to color-coded risk tiers: **Safe (Green)**, **Moderate (Yellow)**, and **High Risk (Red)**.
   - Elbow curve inertia analysis ($k=1..8$) and Silhouette score calculation.
   - Linear Regression model for projecting Semester 1-2 external exam performance and growth trajectory.

---

## ⚡ Quick Start & Local Execution Guide

### 1. Prerequisites & Virtual Environment Setup
Make sure Python 3.11 is installed on your system.

```bash
# Clone or navigate to project directory
cd smart-attendance-performance-analyzer

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate
```

### 2. Install Pinned Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Dashboard
```bash
streamlit run code/main.py
```
Open your browser to `http://localhost:8501`.

---

## 🚀 Deployment Guide & Version-Mismatch Prevention

### Recommended Hosting Options for Streamlit
1. **Streamlit Community Cloud** (Recommended — Zero Config, Free):
   - Connect your GitHub repository.
   - Main file path: `code/main.py`.
   - Add environment variable `MONGODB_URI` in Streamlit secrets dashboard.
2. **Render / Railway / Hugging Face Spaces**:
   - Supports persistent Python web services out of the box.

### Deploying API Endpoints on Vercel
Vercel serverless functions support Python request/response APIs via `@vercel/python`. The repository includes `vercel.json` and explicit version pins (`runtime.txt`, `.python-version`) to prevent build failures.

---

## ✅ Pre-Deployment Checklist

- [x] `requirements.txt` fully pinned (`streamlit==1.35.0`, `pandas==2.2.2`, `numpy==1.26.4`, `scikit-learn==1.5.0`, `pymongo==4.7.3`, `python-docx==1.1.2`)
- [x] `runtime.txt` (`python-3.11`) and `.python-version` (`3.11`) present and matching local Python environment.
- [x] `MONGODB_URI` environment variable template created in `.env.example`.
- [x] MongoDB offline CSV fallback tested and verified (works with zero internet/database connection).
- [x] Automated 75% attendance alert notifications tested.
- [x] App tested locally via `streamlit run code/main.py`.
- [x] Academic report `report/Project17_Report.docx` and AI prompt logs generated for viva evaluation.
