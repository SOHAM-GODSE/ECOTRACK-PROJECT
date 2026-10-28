import uvicorn
import os
import sys

if __name__ == "__main__":
    # Ensure backend directory is in python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    print("🌱 Starting EcoTrack AI Backend on http://127.0.0.1:8000 ...")
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["app"],
        reload_excludes=["venv", "uploads", ".git", "__pycache__", "*.pyc"]
    )
