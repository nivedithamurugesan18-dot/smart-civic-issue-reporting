# Smart Public Infrastructure Issue Reporting System

A web-based civic issue reporting platform that allows citizens to report public infrastructure problems and enables administrators, authority users, and Field Staff to review, assign, track, and update those issues.

## Project objective

The system centralizes reports for public infrastructure problems such as:

- Road damage
- Street light problems
- Waste management issues
- Water-related problems
- Traffic infrastructure issues
- Other public infrastructure problems

A report can contain structured issue information, optional latitude/longitude coordinates, and evidence images.

## Architecture

```text
React + Vite frontend
        ↓ Axios HTTP requests with Bearer JWT
FastAPI REST API
        ↓ SQLAlchemy
PostgreSQL database
```

The application also uses Leaflet and OpenStreetMap for optional location selection and read-only issue-location maps. Runtime evidence files are served from the backend upload directory.

## Current implemented features

- Citizen registration and login
- Bcrypt password hashing and JWT authentication
- Role-based access for citizens, admins, authority users, and Field Staff
- Citizen issue reporting with category, priority, severity, description, and optional location text
- Optional Leaflet/OpenStreetMap location selection
- Latitude/longitude persistence and Issue Details map markers
- No-coordinate fallback for issues without map data
- JPEG, PNG, and WEBP evidence-image upload, retrieval, display, and authorized deletion
- Admin issue listing and Field Staff assignment
- Active assignment source of truth: `issues.assigned_to`
- Field Staff assigned-issue retrieval and workflow
- Status changes and progress timeline updates
- New-issue, assignment, status, and progress notifications
- Unread notification count and mark-as-read behavior
- Citizen, Admin, Authority, Field Staff, Issue Details, and Notifications pages
- FastAPI Swagger/OpenAPI documentation

The planned AI/computer-vision enhancement is not part of the current implementation.

## Technology stack

- Frontend: React, Vite, React Router, Axios, React Leaflet, Leaflet
- Backend: Python, FastAPI, SQLAlchemy, Pydantic
- Database: PostgreSQL
- Authentication: JWT Bearer tokens
- Password security: bcrypt through PassLib
- Maps: Leaflet with OpenStreetMap tiles
- API documentation: FastAPI Swagger/OpenAPI
- Version control: Git and GitHub

## Prerequisites

- Python 3.11 or a compatible version supporting the project dependencies
- Node.js and npm
- PostgreSQL
- A local database named `smart_civic`
- Network access to OpenStreetMap tiles when using map features

## PostgreSQL setup

Create the local PostgreSQL database before starting the backend:

```sql
CREATE DATABASE smart_civic;
```

Use a local PostgreSQL role with permission to connect to this database. Do not place real credentials in source control.

## Backend setup

From the repository root:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell activation is unavailable, activate the equivalent environment using the shell conventions for your platform.

Create `backend/.env` from `backend/.env.example` and replace the placeholders locally:

```dotenv
DATABASE_URL=postgresql://postgres:change_me@localhost:5432/smart_civic
SECRET_KEY=replace-with-a-long-random-secret
```

Never commit a real password or secret key.

Start the backend from the `backend` directory:

```powershell
uvicorn app.main:app --reload
```

The local API is expected at `http://127.0.0.1:8000`.

Health check:

```text
http://127.0.0.1:8000/health
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Frontend setup

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

The Vite development server prints the local frontend URL. The frontend API client currently targets `http://127.0.0.1:8000`.

Useful frontend commands:

```powershell
npm run lint
npm run build
npm run preview
```

## Project structure

```text
smart-civic-issue-reporting/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── main.py
│   │   └── security.py
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   ├── eslint.config.js
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
├── docs/
│   ├── diagrams/
│   │   ├── ER_DIAGRAM.drawio
│   │   ├── ER_DIAGRAM.svg
│   │   └── SYSTEM_ARCHITECTURE.md
│   ├── DEMO_CHECKLIST.md
│   ├── DOMAIN_STUDY.md
│   ├── ENVIRONMENT_NOTES.md
│   ├── FEATURES.md
│   ├── SDLC_STATUS.md
│   ├── SYSTEM_WORKFLOW.md
│   ├── TECH_STACK.md
│   ├── TESTING.md
│   └── VALIDATION_SUMMARY.md
├── Problem_Statement.md
├── requirements.txt
├── README.md
└── .gitignore
```

## Database and assignment note

The repository includes an `assignments` model from the project history, but the active mounted application workflow assigns Field Staff through `issues.assigned_to`. The active route is `PATCH /issues/{issue_id}/assign`; the legacy assignment router is intentionally not mounted.

## Verification status

The completed verification work reported passing results for PostgreSQL connectivity, FastAPI backend workflows, frontend workflows, authentication, JWT, RBAC, issue reporting, map selection, coordinate persistence, Issue Details, image handling, assignment, Field Staff workflow, status/progress updates, notifications, frontend ESLint, frontend production build, dependency checks, and security configuration cleanup.

The project is verified for local execution. No public cloud deployment or CI/CD execution is claimed.

See the final documentation set:

- [Testing](docs/TESTING.md)
- [Validation summary](docs/VALIDATION_SUMMARY.md)
- [System workflow](docs/SYSTEM_WORKFLOW.md)
- [Demo checklist](docs/DEMO_CHECKLIST.md)
- [Features](docs/FEATURES.md)
- [SDLC status](docs/SDLC_STATUS.md)
- [Environment notes](docs/ENVIRONMENT_NOTES.md)
