# Environment Notes

This document separates application requirements from limitations specific to the local development machine and workflow.

## Application requirements

- A running PostgreSQL instance with the `smart_civic` database.
- A backend `DATABASE_URL` that points to the local PostgreSQL instance.
- A non-placeholder `SECRET_KEY` supplied through the backend environment.
- Python dependencies from `backend/requirements.txt`.
- Node.js and npm dependencies from `frontend/package.json` and `frontend/package-lock.json`.
- A backend process running at the URL configured by the frontend API client, currently `http://127.0.0.1:8000`.
- Network access to OpenStreetMap tile URLs when map tiles are displayed.

## Local machine limitations

### OneDrive path behavior

The original project is located under a OneDrive-managed Windows path. Earlier verification work observed Node/Windows `EPERM` behavior in the original path. An isolated working copy was used successfully for frontend lint and production-build verification. This is an environment and filesystem-permission limitation, not an application feature limitation.

### Local PostgreSQL dependency

The application is verified against a local PostgreSQL database. A database server and the `smart_civic` database must be available before the backend can provide database-backed functionality. No cloud database is configured or claimed.

### Python environment

The verified backend work used the project’s repaired/local Python environment when required. The environment is machine-local and is not part of the committed source tree. Recreate or activate an equivalent environment from `backend/requirements.txt` on another machine.

### Local backend/frontend processes

The frontend API client points to the local FastAPI address `http://127.0.0.1:8000`. The frontend and backend must be started separately for a local demonstration. The `/health` route is available when the backend process is running.

### Runtime uploads

Uploaded issue files are runtime data under `backend/uploads/issues/`. They are intentionally excluded from source control and should be treated as local application data.

## Not claimed

- No production deployment was performed.
- No public URL is provided.
- No CI/CD workflow execution is claimed.
- No external government-system integration is configured.
