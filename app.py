import sys
import os

# Add 'code' directory to Python path for smooth importing across cloud platforms
code_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'code')
if code_dir not in sys.path:
    sys.path.insert(0, code_dir)

# Run main application orchestrator
if __name__ == "__main__":
    import runpy
    main_path = os.path.join(code_dir, 'main.py')
    runpy.run_path(main_path, run_name="__main__")
