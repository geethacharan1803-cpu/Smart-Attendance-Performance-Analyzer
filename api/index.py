"""
=============================================================================
API/INDEX.PY — Vercel Serverless Entry Point
=============================================================================
This module adapts the FastAPI ASGI application into a serverless-compatible
handler using Mangum. Vercel's @vercel/python runtime invokes the `handler`
callable for every incoming HTTP request.
=============================================================================
"""

import os
import sys

# ---------------------------------------------------------------------------
# Path Resolution — ensure project root & code/ are importable
# ---------------------------------------------------------------------------
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE_DIR = os.path.join(ROOT_DIR, 'code')

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

# ---------------------------------------------------------------------------
# Import FastAPI app & wrap with Mangum for serverless execution
# ---------------------------------------------------------------------------
from mangum import Mangum  # noqa: E402
from app import app        # noqa: E402

# Mangum adapts ASGI (FastAPI) → AWS Lambda / Vercel serverless handler
# lifespan="off" disables ASGI lifespan events (unsupported in serverless)
handler = Mangum(app, lifespan="off")
