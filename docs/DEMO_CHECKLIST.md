# Final Demonstration Checklist

## Before the demonstration

- Use a local machine with PostgreSQL available.
- Use the project’s configured Python environment and frontend dependencies.
- Prepare authorized demo accounts for the citizen, admin, and Field Staff roles without recording passwords in this document.
- Use a local database containing only demonstration data.

## Setup and startup

| Step | Action | Expected visible result |
|---:|---|---|
| 1 | Start PostgreSQL and confirm the `smart_civic` database is available. | PostgreSQL is running and the application database can accept connections. |
| 2 | Create `backend/.env` from `backend/.env.example` and replace only the local placeholders. | The backend has a local `DATABASE_URL` and `SECRET_KEY`; no secret is displayed during the demo. |
| 3 | Activate the backend Python environment and install dependencies from `backend/requirements.txt` if needed. | The backend environment contains FastAPI, SQLAlchemy, PostgreSQL, JWT, bcrypt, and multipart-upload dependencies. |
| 4 | Start FastAPI from the `backend` directory with `uvicorn app.main:app --reload`. | The terminal shows the local server is running. |
| 5 | Open `http://127.0.0.1:8000/health`. | The page returns the healthy API response. |
| 6 | Open the FastAPI documentation at `http://127.0.0.1:8000/docs` if endpoint inspection is needed. | Swagger/OpenAPI documentation is visible. |
| 7 | From the `frontend` directory, install dependencies if needed and run `npm run dev`. | Vite serves the React frontend and displays the local frontend URL. |

## Citizen demonstration

| Step | Action | Expected visible result |
|---:|---|---|
| 8 | Open the frontend login page. | The Smart Civic login screen is visible. |
| 9 | Register a new citizen if a fresh account is required, or log in with the prepared citizen account. | The citizen reaches the protected dashboard. |
| 10 | Open **Report Civic Issue**. | The issue-report form is visible with category, priority, severity, location, map, and evidence fields. |
| 11 | Enter a title, description, category, priority, severity, and location text. | The entered issue details remain visible in the form. |
| 12 | Click a point on the Leaflet map. | A marker appears and latitude/longitude values are shown. |
| 13 | Select a valid JPEG, PNG, or WEBP evidence image. | The selected filename appears in the evidence-photo list. |
| 14 | Submit the issue. | The issue is created and the application opens its Issue Details page when uploads succeed. |
| 15 | Inspect Issue Details. | The saved title, description, category, priority, severity, status, location, and evidence are visible. |
| 16 | Demonstrate the saved map marker and coordinate values. | The read-only map displays the marker at the persisted coordinates. |
| 17 | Demonstrate evidence retrieval/display. | The uploaded image appears in the Evidence Photos section. |
| 18 | Demonstrate the issue timeline after later updates. | Status/progress entries appear in chronological issue-update order. |

## Admin demonstration

| Step | Action | Expected visible result |
|---:|---|---|
| 19 | Log out and log in with the prepared admin account. | The admin reaches the protected admin workflow. |
| 20 | Open the Admin Dashboard. | The full issue list and status summary are visible. |
| 21 | Select an issue and enter the prepared Field Staff user ID. | The assignment action is ready to submit. |
| 22 | Assign the issue to Field Staff. | The issue shows the assigned Field Staff identifier and the Field Staff receives an assignment notification. |

## Field Staff demonstration

| Step | Action | Expected visible result |
|---:|---|---|
| 23 | Log out and log in with the prepared Field Staff account. | The Field Staff dashboard is visible. |
| 24 | Open the assigned-issue list. | Only issues assigned through the active `issues.assigned_to` field are listed. |
| 25 | Open the assigned issue. | Issue Details shows the issue information, map if coordinates exist, and evidence. |
| 26 | Change the issue status. | The status changes and a status-history entry is created. |
| 27 | Add a progress message. | The progress update appears in the issue timeline and a citizen notification is generated. |

## Citizen notification demonstration

| Step | Action | Expected visible result |
|---:|---|---|
| 28 | Log out and log in again as the reporting citizen. | The citizen dashboard is visible. |
| 29 | Open Notifications. | The citizen sees status/progress notifications and the unread count. |
| 30 | Mark a notification as read. | The notification changes to read and the unread count updates. |
| 31 | Reopen Issue Details. | The latest status, progress timeline, location marker, and evidence remain visible. |

## Demonstration boundaries

- Do not display passwords, JWT values, database URLs containing real credentials, or `.env` files.
- Do not use Issue 14 or other protected real records for destructive demonstrations.
- Do not create or delete records outside the approved demonstration scope.
- The application is locally runnable; this checklist does not claim cloud deployment.
