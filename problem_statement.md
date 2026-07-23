# Problem Statement - Project 17: Smart Attendance & Performance Analyzer

## Context
Under the **JNTUK R23 Curriculum for B.Tech Artificial Intelligence and Data Science (1st Year)**, students need to apply integrated knowledge across three foundational domains:
1. **Programming Fundamentals** (File I/O, Modular Code Structure, Exception Handling)
2. **Linear Algebra & Matrix Calculus** (Vector Spaces, Matrix Representation $M_{n \times m}$, Dot Products, Feature Weighting)
3. **Data Structures** (QuickSort Algorithm, Array Data Structures, Searching)

## Objective
Educational institutions often struggle to identify early warning indicators in student performance. Attendance percentage and mid-term exam marks are usually analyzed in isolation. 

**Smart Attendance & Performance Analyzer** bridges this gap by creating an automated analytics framework that:
- Ingests student academic records from standard CSV storage.
- Constructs feature matrices to calculate composite performance scores using weighted linear combination vector operations.
- Ranks students efficiently using custom Data Structure sorting algorithms (QuickSort).
- Applies basic Machine Learning correlation techniques (Pearson $r$) and Ordinary Least Squares (OLS) Linear Regression ($y = mx + c$) to model performance projections based on attendance.
- Generates rule-based AI performance classifications (*Consistent High-Achiever*, *High Potential Needs Attendance Boost*, *At-Risk*) along with LLM advisory prompt notes for faculty intervention.
- Produces a multi-panel visual analytics dashboard.

## Expected Deliverables
- **Data Ingestion**: Multi-column student CSV parser with automatic median imputation.
- **Linear Algebra Module**: Matrix dot product $S = M \cdot W$ for multi-factor weighted scoring.
- **Data Structure Module**: Custom O(n log n) QuickSort implementation for array sorting.
- **AI & Analytics Module**: Pearson correlation analysis and linear regression trend modeling.
- **Visualization & Reporting**: Matplotlib dashboard plots and processed result exports.
