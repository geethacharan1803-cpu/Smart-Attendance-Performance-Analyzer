"""
Vercel Serverless Function Entry Point (api/index.py)
"""

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE_DIR = os.path.join(ROOT_DIR, "code")

for d in [CODE_DIR, ROOT_DIR]:
    if d not in sys.path:
        sys.path.insert(0, d)

from main import main

if __name__ == "__main__":
    main()
