# Validation Summary

## Purpose

This summary explains how the current Smart Public Infrastructure Issue Reporting System satisfies its implemented functional areas. Claims combine the current repository source with the completed runtime and quality verification results supplied for the final submission phase.

The system is a local client-server application. No public deployment is claimed.

## 1. Authentication

The backend provides citizen registration and JSON login under `/auth/register` and `/auth/login`. Passwords are hashed with bcrypt through PassLib. Successful login returns a Bearer JWT containing the user identity and role. Protected endpoints validate the token before loading the current user.

Registration, login, password hashing/verification, and JWT-protected access were verified during the completed runtime verification.

## 2. Role-based access

The application uses the roles `citizen`, `admin`, `authority`, and `field_staff` in the implemented role checks and dashboards. Citizens can report issues and view their own reports. Admin users can list issues and assign Field Staff. Authority users can access the all-issue viewing workflow. Field Staff can retrieve and manage issues assigned through `issues.assigned_to`.

Role restrictions and the main citizen/admin/Field Staff flows passed the completed runtime verification. A separate authority-specific negative test was not recorded as a standalone result.

## 3. Issue reporting

An authenticated citizen can create an issue with title, description, category, priority, severity, location text, and optional latitude/longitude. The issue is associated with the authenticated reporter. Citizens can retrieve their own issues, while admin and authority roles can retrieve the all-issue view.

Issue creation without coordinates, issue creation with coordinates, citizen issue retrieval, admin listing, and Issue Details were verified.

## 4. Location/map

The frontend uses React Leaflet with OpenStreetMap tiles. The report form allows an optional map click. The selected coordinates are rounded to six decimal places, submitted through the issue API, stored on the issue, and displayed again on Issue Details through a read-only marker map.

Leaflet rendering, OpenStreetMap tiles, map click, coordinate capture, coordinate persistence, the Issue Details marker, and the no-coordinate fallback were verified.

## 5. Evidence images

The report form accepts multiple JPEG, PNG, or WEBP files. The backend validates content type, extension, file signature, and a five-megabyte maximum before storing files in `backend/uploads/issues/` and creating database image records. Images can be retrieved for an issue and displayed on Issue Details. Authorized users can delete issue-scoped image records and their stored files.

Valid upload, retrieval, display, deletion, and authorization restrictions were verified.

## 6. Assignment

The active assignment workflow is the issue route `PATCH /issues/{issue_id}/assign`, which writes the Field Staff user ID to `issues.assigned_to`. The admin dashboard performs this operation, and the assigned Field Staff receives a notification. Field Staff retrieval filters on `Issue.assigned_to`.

The legacy `assignments` model/table remains present in the repository but is not the active source of truth; the legacy assignment router is intentionally not mounted by the application.

Admin assignment, Field Staff assignment, and assigned-issue retrieval were verified.

## 7. Status/progress tracking

Admin and Field Staff users can update an issue status from the supported status set. Field Staff may update only issues assigned to them. Status changes create issue-update history. Authorized admin or Field Staff users can also add progress messages, optionally changing the issue status. Citizens can view the resulting issue details and timeline.

Status updates, progress updates, citizen visibility, and rejection of unauthorized citizen status mutation were verified.

## 8. Notifications

Notifications are created for new issue reports, assignments, status changes, and progress updates. Authenticated users can retrieve their notifications, query the unread count, and mark their own notifications as read.

New issue, assignment, status, progress, unread count, and mark-as-read behavior were verified.

## 9. Database

PostgreSQL is the application database. SQLAlchemy models and sessions provide database access for users, issues, issue updates, issue images, departments, assignments, and notifications. The verified cleanup preserved the real Issue 14 and protected users 11, 17, and 18 while removing only the identified temporary audit records.

The database connection and controlled data verification passed. Alembic `1.16.4` is the explicit schema migration mechanism, with baseline revision `1b1e22234583`. The existing `smart_civic` database was compared read-only, backed up, and stamped at that baseline; the application schema and data remained unchanged except for the intended `alembic_version` marker. FastAPI startup no longer executes `Base.metadata.create_all()` and does not run migrations automatically.

The approved live `issues_reported_by_fkey` remains preserved even though the SQLAlchemy `Issue` model does not declare it. Accordingly, `alembic check` reports the known `remove_fk` discrepancy for that FK only; it must not be applied automatically.

## 10. Frontend

The React frontend uses React Router, Axios, React Leaflet, and role-specific pages for citizen, admin, authority, Field Staff, Issue Details, and notifications workflows. The frontend lint check and production build passed in the completed verification.

## 11. Backend

The FastAPI backend exposes authentication, user, issue, image, department, and notification routes. It also provides `/health` and FastAPI Swagger/OpenAPI documentation. The backend uses SQLAlchemy and Pydantic-based schemas.

Backend startup, API workflows, syntax/import validation, dependency verification, and database connectivity passed in the completed verification.

## 12. Security/configuration

The application requires `SECRET_KEY` to be provided through the environment and does not use an insecure JWT fallback. Database configuration is supplied through `DATABASE_URL`. Password hashing uses bcrypt, protected APIs use Bearer JWT authentication, and role/ownership checks protect restricted operations.

Security configuration cleanup and the absence of obvious real secrets in committed files were verified.

## Scope boundary

This summary does not claim CI/CD execution, cloud deployment, production hosting, or implementation of the planned AI enhancement. Those items are documented separately in `SDLC_STATUS.md` as incomplete or planned.
