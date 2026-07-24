import os
import sys

# Compute project root and code directory paths
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE_DIR = os.path.join(ROOT_DIR, 'code')

# Add project root and code dir to Python module search path
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

# Import the FastAPI application instance from app.py
from app import app

# Export handler for Vercel Serverless Function builder (@vercel/python)
handler = app
