"""
Streamlit Community Cloud Main Application Entry Point
Redirects execution to code/main.py with complete path resolution.
"""

import os
import sys

# Ensure code/ directory and project root are in sys.path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.join(ROOT_DIR, "code")

for d in [CODE_DIR, ROOT_DIR]:
    if d not in sys.path:
        sys.path.insert(0, d)

from main import main

if __name__ == "__main__":
    main()
