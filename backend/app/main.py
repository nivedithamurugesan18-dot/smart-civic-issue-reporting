from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings

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

# Assignment is handled by /issues/{issue_id}/assign and
# Issue.assigned_to.
# The legacy /assignments router is retained but intentionally
# not mounted.
from app.routes.auth import router as auth_router
from app.routes.department import router as department_router
from app.routes.issue_image import router as issue_image_router
from app.routes.notification import router as notification_router

# ============================================================
# DATABASE SCHEMA OWNERSHIP
# ============================================================
# Schema creation and changes are managed explicitly through
# Alembic.
#
# Application startup must not create or alter database tables.
#
# Do not add Base.metadata.create_all() here.
# Do not automatically execute Alembic migrations here.

# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title=settings.app_name,
    description=(
        "Backend API for reporting, assigning, tracking, "
        "and managing public infrastructure issues."
    ),
    version=settings.app_version,
)

# ============================================================
# RUNTIME UPLOAD DIRECTORY
# ============================================================

# Expose only the dedicated runtime upload directory.
#
# NOTE:
# Local filesystem image storage is retained for the current
# application and will be replaced/extended with persistent
# cloud object storage in a later deployment phase.
ISSUE_UPLOAD_DIR = (
    Path(__file__).resolve().parents[1]
    / "uploads"
    / "issues"
)

ISSUE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app.mount(
    "/uploads/issues",
    StaticFiles(directory=ISSUE_UPLOAD_DIR),
    name="issue-uploads",
)

# ============================================================
# CORS
# ============================================================

# CORS origins are configured through the CORS_ORIGINS
# environment variable.
#
# Local default:
#   http://localhost:5173,http://127.0.0.1:5173
#
# Production deployment must set CORS_ORIGINS to the exact
# deployed frontend origin(s).
#
# The application uses JWT Bearer authentication through the
# Authorization header, so credentialed browser requests are
# not required.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "Accept",
    ],
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
        "version": settings.app_version,
    }


# ============================================================
# HEALTH CHECK
# ============================================================


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }