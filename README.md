# Smart Attendance & Performance Analyzer (Project 17)

**JNTUK R23 Curriculum — B.Tech Artificial Intelligence & Data Science (1st Year, 2025 Batch)**

## Overview
**Smart Attendance & Performance Analyzer** is an educational AI application designed for 1st-Year B.Tech Artificial Intelligence and Data Science students under the JNTUK R23 Curriculum. 

The system integrates foundational engineering concepts — Programming & Problem Solving (File I/O), Linear Algebra & Calculus (Matrix Operations), Data Structures (QuickSort Algorithm), AI/ML Foundations (K-Means Clustering, Pearson Correlation, OLS Linear Regression, Random Forest Regressor), and MongoDB integration.

## Key Features
- **Database Connection & Schema**: PyMongo / MongoDB Atlas integration for 80 students with nested mark structures and daily attendance logs.
- **Smart Admin & Daily Attendance**: Interactive tracking interface for daily present/absent marking, remarks logging, and mandatory 75% attendance threshold monitoring.
- **Predictive Performance Trajectory**: Random Forest ML model predicting Semester 1-2 performance, GPA expectations, and risk levels from Semester 1-1 features.
- **Modernized Dashboard & Visualizations**: Responsive Streamlit UI featuring glassmorphism cards, dark sidebar, multi-parameter filtering, and comprehensive matplotlib/seaborn analytical graphs.

## Tech Stack
- **Frontend / Dashboard**: Streamlit
- **Backend & Logic**: Python 3.10+, NumPy, Pandas, Scikit-Learn
- **Database**: MongoDB / PyMongo (with CSV fallback)
- **Data Visualization**: Matplotlib, Seaborn

## Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r code/requirements.txt
   ```

2. **Run the Streamlit Application**:
   ```bash
   cd code
   streamlit run main.py
   ```
