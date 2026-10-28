from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from contextlib import asynccontextmanager
from pathlib import Path
import asyncio
import logging
import os

from app.config import get_settings
from app.database import Base, engine
import app.models  # ensure models are registered
from app.routers import (
    auth, organizations, water, electricity, waste, incidents, carbon,
    recommendations, dashboard, analytics, locations, challenges,
    notifications, reports, admin, iot
)

logger = logging.getLogger("ecotrack")
settings = get_settings()

FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables exist silently
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.warning(f"Database initialization warning: {e}")
    try:
        yield
    except (asyncio.CancelledError, KeyboardInterrupt):
        pass


app = FastAPI(
    title="EcoTrack AI API",
    description="AI-powered environmental intelligence platform. Detect waste. Predict problems. Take action. Measure impact.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# CORS configuration allowing frontend dev server and direct backend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include all API routers under /api
for router_module in [
    auth, organizations, water, electricity, waste, incidents, carbon,
    recommendations, dashboard, analytics, locations, challenges,
    notifications, reports, admin, iot
]:
    app.include_router(router_module.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "EcoTrack AI", "version": "1.0.0"}


# Serve Frontend SPA from backend if built
if FRONTEND_DIST.exists():
    assets_dir = FRONTEND_DIST / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="frontend-assets")

    @app.get("/{full_path:path}")
    async def serve_frontend_spa(full_path: str):
        # Do not catch /api endpoints
        if full_path.startswith("api/") or full_path == "api":
            raise HTTPException(status_code=404, detail="Not Found")
        
        target_file = FRONTEND_DIST / full_path
        if full_path and target_file.is_file():
            return FileResponse(target_file)
        
        # Fallback to SPA index.html
        return FileResponse(FRONTEND_DIST / "index.html")
else:
    @app.get("/")
    def root_redirect():
        return RedirectResponse(url="/api/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["app"],
        reload_excludes=["venv", "uploads", ".git", "__pycache__", "*.pyc"]
    )
