import os
import sys
import subprocess
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

# Ensure 'code' directory is accessible on Python module search path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.join(BASE_DIR, 'code')
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

# Initialize FastAPI Application instance
app = FastAPI(
    title="Smart Attendance & Performance Analyzer API",
    description="JNTUK R23 B.Tech AI & Data Science Academic Performance Engine",
    version="1.0.0"
)

# Enable Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def landing_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Smart Attendance & Performance Analyzer</title>
        <style>
            :root {
                --bg-primary: #0F172A;
                --bg-card: #1E293B;
                --accent-blue: #6366F1;
                --text-main: #F8FAFC;
                --text-muted: #94A3B8;
                --success-green: #22C55E;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: var(--bg-primary);
                color: var(--text-main);
                margin: 0;
                padding: 40px 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 80vh;
            }
            .container {
                background-color: var(--bg-card);
                border-radius: 12px;
                padding: 32px;
                max-width: 650px;
                width: 100%;
                box-shadow: 0 10px 25px rgba(0,0,0,0.5);
                border: 1px solid #334155;
            }
            .badge {
                display: inline-block;
                background-color: rgba(34, 197, 94, 0.15);
                color: var(--success-green);
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
                margin-bottom: 12px;
            }
            h1 { color: var(--text-main); margin-top: 0; font-size: 1.8rem; }
            p { color: var(--text-muted); line-height: 1.6; }
            .endpoint-list {
                list-style: none;
                padding: 0;
                margin: 20px 0;
            }
            .endpoint-list li {
                background: #0F172A;
                padding: 12px 16px;
                border-radius: 8px;
                margin-bottom: 10px;
                border: 1px solid #334155;
            }
            .method { font-weight: bold; color: var(--accent-blue); margin-right: 10px; }
            a { color: #38BDF8; text-decoration: none; font-weight: 500; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <span class="badge">● HTTP Web Service Active</span>
            <h1>🎓 Smart Attendance & Performance Analyzer</h1>
            <p>JNTUK R23 B.Tech AI & Data Science Academic Performance Analytics Engine.</p>
            <hr style="border-color: #334155; margin: 20px 0;">
            <h3>Available Endpoints</h3>
            <ul class="endpoint-list">
                <li><span class="method">GET</span> <a href="/health">/health</a> — Service Health & Version Status</li>
                <li><span class="method">GET</span> <a href="/api/v1/rules">/api/v1/rules</a> — JNTUK R23 Attendance Cutoffs & Grading Rules</li>
                <li><span class="method">GET</span> <a href="/docs">/docs</a> — Interactive OpenAPI Documentation</li>
            </ul>
        </div>
    </body>
    </html>
    """

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Smart Attendance & Performance Analyzer",
        "version": "1.0.0",
        "regulation": "JNTUK R23 B.Tech AI & DS"
    }

@app.get("/api/v1/rules")
def get_jntuk_rules():
    return {
        "regulation": "JNTUK R23",
        "branch": "AI & Data Science",
        "attendance_thresholds": {
            "eligible": ">= 75%",
            "condonation": "65% to 74.9%",
            "detained": "< 65%"
        },
        "grading_scale": {
            "S": {"grade_points": 10, "marks_range": ">= 90%"},
            "A": {"grade_points": 9, "marks_range": "80% - 89%"},
            "B": {"grade_points": 8, "marks_range": "70% - 79%"},
            "C": {"grade_points": 7, "marks_range": "60% - 69%"},
            "D": {"grade_points": 6, "marks_range": "50% - 59%"},
            "E": {"grade_points": 5, "marks_range": "40% - 49%"},
            "F": {"grade_points": 0, "marks_range": "< 40% (Fail)"}
        }
    }

# Local/Container Execution Runner
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8501))
    main_script = os.path.join(CODE_DIR, "main.py")
    print(f"Starting Streamlit app runner on port {port}...")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", main_script,
        f"--server.port={port}",
        "--server.address=0.0.0.0",
        "--server.headless=true"
    ])
