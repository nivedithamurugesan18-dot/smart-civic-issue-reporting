# System Workflow

## Overview

The Smart Public Infrastructure Issue Reporting System connects citizens, administrators, authority users, and Field Staff through a FastAPI REST API and PostgreSQL database. The React frontend communicates with the backend through Axios and sends the JWT Bearer token for protected requests.

## Main application workflow

```text
Citizen
  → Register/Login
  → Report Issue
  → Select optional map location
  → Select optional evidence images
  → Submit issue
  → Admin reviews the issue
  → Admin assigns Field Staff
  → Field Staff retrieves assigned issue
  → Field Staff updates status/progress
  → Citizen receives notifications
  → Citizen views Issue Details and timeline
```

### 1. Citizen registration and login

1. A citizen opens the registration page and submits name, email, and password.
2. The backend creates the user with the `citizen` role and stores a bcrypt password hash.
3. The citizen logs in through `/auth/login`.
4. The backend verifies the password and returns a Bearer JWT containing the user identity and role.
5. The frontend stores the access token and user information locally and attaches the token to later Axios requests.

### 2. Citizen issue reporting

1. The citizen opens `ReportIssue`.
2. The form collects title, description, category, priority, severity, and optional location text.
3. The citizen may select an optional map location.
4. The citizen may select one or more evidence images.
5. The frontend submits the issue to `POST /issues/`.
6. The backend associates the issue with the authenticated citizen and stores the issue fields in PostgreSQL.
7. The backend creates an `issue_created` notification for admin users.
8. The frontend uploads selected images to the newly created issue and opens Issue Details when the workflow succeeds.

### 3. Admin review and assignment

1. An admin opens the Admin Dashboard.
2. The dashboard loads the all-issue view from `GET /issues/`.
3. The admin reviews issue details, category, priority, severity, status, and location.
4. The admin enters a Field Staff user ID and calls `PATCH /issues/{issue_id}/assign`.
5. The active assignment source of truth is `issues.assigned_to`.
6. If the issue is still `reported`, the assignment operation changes it to `assigned`.
7. The assigned Field Staff receives an `issue_assigned` notification.

The legacy `assignments` table/router is not used as the active assignment path. The application’s mounted assignment workflow writes `Issue.assigned_to` directly.

### 4. Field Staff workflow

1. Field Staff logs in with an authorized account.
2. The Field Staff Dashboard calls `GET /issues/assigned`.
3. The backend returns issues whose `assigned_to` value matches the authenticated Field Staff user.
4. Field Staff opens an issue and can update the status or add progress through Issue Details.
5. The backend records issue updates in `issue_updates` and updates the main issue status when a status is supplied.
6. The reporting citizen receives status or progress notifications.

### 5. Citizen follow-up

1. The citizen opens the notification page or receives the updated information through the application workflow.
2. The citizen opens Issue Details.
3. Issue Details loads the issue, progress updates, and evidence images.
4. The citizen can see the current status, assigned Field Staff identifier when present, saved location, evidence gallery, and timeline.

## Map and location path

```text
Map click
  → latitude/longitude captured in LocationPicker
  → issue JSON submitted to FastAPI
  → latitude/longitude stored on issues
  → Issue Details reads the saved values
  → read-only IssueLocationMap renders the marker
```

The report map uses Leaflet and OpenStreetMap tiles. A map click captures latitude and longitude to six decimal places. Selecting a map point is optional. If an issue has no coordinates, Issue Details remains available and omits the map section instead of rendering an invalid marker.

## Evidence image path

```text
File selection
  → multipart upload
  → content type, extension, size, and file-signature validation
  → filesystem storage under backend/uploads/issues/
  → issue image database record
  → authenticated retrieval/display
  → authorized issue-scoped deletion
```

The implemented upload path accepts JPEG, PNG, and WEBP images up to five megabytes. The database record stores the issue relationship, generated filename, and image URL. The backend exposes the runtime upload directory at `/uploads/issues`. Image mutations are authorized for an admin, the reporting citizen, or the assigned Field Staff user according to the issue authorization checks.

## Notification path

```text
Issue/assignment/status/progress event
  → notification record created
  → authenticated user loads notifications
  → unread count is queried
  → user marks a notification as read
```

The notification routes are:

- `GET /notifications/`
- `GET /notifications/unread-count`
- `PATCH /notifications/{notification_id}/read`

## Role boundaries

- **Citizen:** register, log in, create issues, upload evidence for owned issues, view own reports, and follow status/progress information.
- **Admin:** view all issues, assign Field Staff, manage issue status/progress, and access administrative issue management.
- **Authority:** access the implemented authority issue-listing workflow and its dashboard restrictions.
- **Field Staff:** retrieve issues assigned through `issues.assigned_to`, update assigned issue status/progress, and operate on authorized assigned issue evidence.

## Related documentation

- [Testing](./TESTING.md)
- [Validation summary](./VALIDATION_SUMMARY.md)
- [Demo checklist](./DEMO_CHECKLIST.md)
- [Feature summary](./FEATURES.md)
- [ER diagram](./diagrams/ER_DIAGRAM.svg)
