from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine

# ============================================================
# IMPORT ALL MODELS
# ============================================================

from app.models.user import User
from app.models.issue import Issue
from app.models.issue_update import IssueUpdate
from app.models.issue_image import IssueImage
from app.models.department import Department
from app.models.assignment import Assignment
from app.models.notification import Notification

# ============================================================
# IMPORT ROUTERS
# ============================================================

from app.routes.user import router as user_router
from app.routes.issue import router as issue_router
# Assignment is handled by /issues/{issue_id}/assign and Issue.assigned_to.
# The legacy /assignments router is retained but intentionally not mounted.
from app.routes.auth import router as auth_router
from app.routes.department import router as department_router
from app.routes.issue_image import router as issue_image_router
from app.routes.notification import router as notification_router

# ============================================================
# CREATE DATABASE TABLES
# ============================================================

Base.metadata.create_all(bind=engine)

# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Smart Public Infrastructure Issue Reporting System",
    description=(
        "Backend API for reporting, assigning, tracking, "
        "and managing public infrastructure issues."
    ),
    version="1.0.0"
)

# Expose only the dedicated runtime upload directory.
ISSUE_UPLOAD_DIR = (
    Path(__file__).resolve().parents[1]
    / "uploads"
    / "issues"
)
ISSUE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount(
    "/uploads/issues",
    StaticFiles(directory=ISSUE_UPLOAD_DIR),
    name="issue-uploads"
)

# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# ROUTES
# ============================================================

app.include_router(user_router)
app.include_router(issue_router)
app.include_router(auth_router)
app.include_router(department_router)
app.include_router(issue_image_router)
app.include_router(notification_router)

# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Smart Public Infrastructure Issue Reporting System API",
        "status": "running",
        "version": "1.0.0"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
