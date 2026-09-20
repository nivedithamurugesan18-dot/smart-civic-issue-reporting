# Requirements Specification

## 1. Document Purpose

This document defines the functional and non-functional requirements for the implemented Smart Public Infrastructure Issue Reporting System. It establishes a requirements baseline suitable for the project’s college SDLC/capstone submission and maps each requirement to implementation evidence and recorded verification evidence where that evidence exists.

The repository implementation is the source of truth for current requirements. The verification column uses the test IDs and status recorded in `docs/TESTING.md`; it does not invent tests or convert source-only evidence into a successful runtime result.

The system is documented as a local client-server application. The current baseline does not claim public deployment, cloud hosting, live PostgreSQL integration in GitHub Actions, AI implementation, or government-system integration.

## 2. System Scope

The system is a browser-based civic issue reporting and tracking application. Citizens can register, authenticate, submit public infrastructure issues, provide structured details, optionally select map coordinates, attach evidence images, and follow the resulting status and progress information. Authorized administrative and field roles can review, assign, update, track, and manage those issues through role-specific workflows.

The implemented scope includes:

- Citizen registration and login.
- Bearer JWT authentication.
- Role-based access control for citizens, admins, authority users, and Field Staff.
- Citizen issue reporting with title, description, category, priority, severity, and optional textual location.
- The implemented issue categories: Road, Street Light, Waste, Water, Traffic, and Other.
- Optional Leaflet/OpenStreetMap map selection.
- Nullable latitude and longitude persistence on the issue record.
- JPEG, PNG, and WEBP evidence-image upload, validation, retrieval, display, and authorized deletion.
- Administrative issue review and all-issue listing.
- Admin assignment of issues to Field Staff through `issues.assigned_to`.
- Field Staff retrieval of issues assigned to the authenticated Field Staff user.
- Controlled issue statuses: `reported`, `assigned`, `in_progress`, `resolved`, and `closed`.
- Status changes and progress updates stored in `issue_updates`.
- Database-backed in-app notifications for implemented issue lifecycle events.
- Citizen, Admin, Authority, Field Staff, Issue Details, and Notifications interfaces.
- PostgreSQL persistence through SQLAlchemy.

The following are outside the current implemented scope and are not treated as current requirements:

- AI or computer-vision issue classification.
- Automated severity estimation or priority recommendation by AI.
- Public or cloud deployment.
- Automated government-system integration.
- Email, SMS, or push notifications.
- A live PostgreSQL integration test in GitHub Actions.

## 3. Stakeholders and User Roles

### 3.1 Citizen

A citizen is the public reporter and owner of submitted issue records. The implemented citizen workflow allows a citizen to:

- Register with a name, email, and password.
- Log in and receive an authenticated session token.
- Create an issue report with the implemented issue fields.
- Select an issue category and provide priority and severity values.
- Enter optional textual location information.
- Select optional latitude and longitude using the map.
- Select and upload evidence images after issue creation.
- Retrieve the citizen’s own issue list.
- Open Issue Details and view status, assignment information, evidence, location, and the progress timeline.
- View notifications, unread count information, and mark owned notifications as read.
- Perform issue or evidence operations only within the ownership rules implemented by the backend.

### 3.2 Admin

An admin is the primary issue-management role. The implemented admin workflow allows an admin to:

- Authenticate through the protected login flow.
- View the all-issue listing.
- Review issue details, category, priority, severity, status, location, and evidence.
- Assign an issue to a user whose role is `field_staff`.
- Change issue status and add progress updates.
- Use the Admin Dashboard’s issue summaries and assignment controls.
- Create managed user accounts through the protected `/users/` route. The role supplied to that route is validated against the implemented role enum.
- Operate on issue evidence under the admin authorization rules.

The current implementation does not provide a separate verified workflow for an admin to approve/reject reports, manage department assignment on an issue, or use AI-generated prioritization. Those items remain outside the current requirements baseline.

### 3.3 Authority

An authority user is an authorized monitoring and review role. The implemented authority workflow allows an authority user to:

- Authenticate through the protected application.
- Access the all-issue listing permitted by the backend role check.
- Use the Authority Dashboard to view issue summaries and filter displayed issues by status and priority.
- Open issue details through the dashboard.

The source and existing documentation support this issue-listing/dashboard workflow. A separate authority-specific negative authorization test is not recorded in `docs/TESTING.md` under `RBAC-004`.

### 3.4 Field Staff

Field Staff handle issues assigned to them. The implemented Field Staff workflow allows a Field Staff user to:

- Authenticate through the protected application.
- Retrieve only issues whose `issues.assigned_to` value matches the authenticated user.
- Use the Field Staff Dashboard to view assigned-issue totals and filter assigned issues by status.
- Open assigned issue details.
- Change status and add progress updates only for issues assigned to that user.
- Operate on evidence images for assigned issues under the implemented image authorization checks.

The legacy `assignments` model/table and legacy assignment router are not the active workflow. The active assignment source of truth is the `issues.assigned_to` column.

## 4. Functional Requirements

The following requirements describe implemented or source-supported current functionality. A requirement with no dedicated recorded runtime test is explicitly marked as source evidence only in the traceability matrix.

### 4.1 Authentication Requirements

| ID | Requirement | Implementation evidence |
|---|---|---|
| FR-AUTH-001 | The system shall allow a public user to register with a name, email, and password. A newly registered account shall receive the `citizen` role. | `backend/app/routes/auth.py` `POST /auth/register`; `User` model default and explicit registration role. |
| FR-AUTH-002 | The system shall reject registration when the submitted email is already registered. | Duplicate-email lookup in `backend/app/routes/auth.py`; returns a client error. |
| FR-AUTH-003 | The system shall authenticate a user through JSON email/password login and return a Bearer access token with user identity information. | `POST /auth/login` in `backend/app/routes/auth.py`; frontend login stores token and user data. |
| FR-AUTH-004 | The system shall hash passwords before persistence and verify submitted passwords against the stored hash. | PassLib/bcrypt functions in `backend/app/security.py`; registration and login use `hash_password` and `verify_password`. |
| FR-AUTH-005 | The system shall create JWT access tokens containing the authenticated user identity and role, with an expiration period. | `create_access_token` and login handlers in `backend/app/security.py` and `backend/app/routes/auth.py`. |
| FR-AUTH-006 | Protected API operations shall require a valid HTTP Bearer JWT and a corresponding user record. | `get_current_user` in `backend/app/dependencies.py`; frontend Axios interceptor adds the Bearer header. |
| FR-AUTH-007 | The system shall expose an OAuth2 password-flow token endpoint for the FastAPI Swagger interface. | `POST /auth/token` in `backend/app/routes/auth.py`. |
| FR-AUTH-008 | Only an authenticated admin shall create managed user accounts through the user-management route. | `POST /users/` depends on `require_role("admin")` in `backend/app/routes/user.py`; `UserRole` validates allowed roles. |

### 4.2 Issue Management Requirements

| ID | Requirement | Implementation evidence |
|---|---|---|
| FR-ISSUE-001 | An authenticated citizen shall be able to create an issue containing a title, description, category, priority, severity, and optional textual location. | `IssueCreate` schema and `POST /issues/`; `ReportIssue.jsx` form. |
| FR-ISSUE-002 | The issue-reporting interface shall provide the implemented category choices: Road, Street Light, Waste, Water, Traffic, and Other. | Category options in `frontend/src/pages/ReportIssue.jsx`; submitted category is stored on `Issue.category`. |
| FR-ISSUE-003 | The system shall associate each newly created issue with the authenticated citizen who reported it. | `reported_by=current_user.id` in `backend/app/routes/issue.py`. |
| FR-ISSUE-004 | The system shall preserve the submitted priority and severity values on the issue record and display them in issue-management and details views. | `Issue.priority`, `Issue.severity`, `IssueCreate`, `IssueResponse`, and dashboard/detail rendering. |
| FR-ISSUE-005 | An authenticated citizen shall be able to retrieve only the issues reported by that citizen through the personal issue workflow. | `GET /issues/my` filters on `Issue.reported_by`; `MyIssues.jsx` uses the endpoint. |
| FR-ISSUE-006 | Admin and authority users shall be able to retrieve the all-issue listing permitted by their role. | `GET /issues/` uses `require_role("admin", "authority")`; Admin and Authority dashboards call the endpoint. |
| FR-ISSUE-007 | An authenticated user shall be able to open a single issue by ID and view its stored issue details. | `GET /issues/{issue_id}` and `IssueDetails.jsx`. |
| FR-ISSUE-008 | The system shall expose the current issue status and active assignment value in issue responses and details views. | `IssueResponse` includes `status` and `assigned_to`; Issue Details displays both. |
| FR-ISSUE-009 | The issue API shall allow an issue owner or admin to delete an issue, and shall allow an owner, admin, or assigned Field Staff user to update issue details according to the implemented route checks. | `PUT /issues/{issue_id}` and `DELETE /issues/{issue_id}` authorization logic in `backend/app/routes/issue.py`. |

### 4.3 Location and Map Requirements

| ID | Requirement | Implementation evidence |
|---|---|---|
| FR-MAP-001 | The issue report shall support optional latitude and longitude values; a citizen shall be able to submit an issue without map coordinates. | Nullable coordinate fields in `IssueCreate` and `Issue`; optional `LocationPicker` integration. |
| FR-MAP-002 | The report interface shall render a Leaflet map with OpenStreetMap tiles and allow the user to select a point. | `LocationPicker.jsx` uses React Leaflet, Leaflet, and the OpenStreetMap tile URL. |
| FR-MAP-003 | A selected map point shall capture latitude and longitude rounded to six decimal places. | `MapClickHandler` in `LocationPicker.jsx`. |
| FR-MAP-004 | The system shall validate coordinate ranges and require latitude and longitude to be supplied together when coordinates are provided. | `IssueCreate` uses latitude/longitude bounds and a coordinate-pair model validator. |
| FR-MAP-005 | The system shall persist submitted coordinates on the issue and display a read-only marker map in Issue Details when both coordinates exist. | `Issue.latitude`/`Issue.longitude`; `IssueLocationMap.jsx`; Issue Details coordinate handling. |
| FR-MAP-006 | When coordinates are unavailable, Issue Details shall retain a textual location/fallback presentation instead of rendering an invalid marker map. | Conditional map rendering and fallback text in `IssueDetails.jsx`. |

### 4.4 Evidence Image Requirements

| ID | Requirement | Implementation evidence |
|---|---|---|
| FR-IMG-001 | The report workflow shall support selecting multiple evidence images and uploading them to the created issue using multipart form data. | `ReportIssue.jsx` creates `FormData` for selected files and calls `/issues/{issue_id}/images`. |
| FR-IMG-002 | Evidence uploads shall accept JPEG, PNG, and WEBP images only. | `ALLOWED_CONTENT_TYPES` in `backend/app/routes/issue_image.py`; frontend file input accept list. |
| FR-IMG-003 | An evidence image shall not exceed five megabytes. | `MAX_IMAGE_SIZE = 5 * 1024 * 1024` and bounded file read in `issue_image.py`. |
| FR-IMG-004 | Evidence validation shall check content type, filename extension compatibility, and the file signature for the declared image format. | `_validate_image` in `backend/app/routes/issue_image.py`. |
| FR-IMG-005 | Accepted evidence files shall be stored under the runtime issue-upload directory and represented by an `issue_images` database record. | Generated filename, `backend/uploads/issues/`, `IssueImage`, and image service/repository. |
| FR-IMG-006 | Authenticated users shall be able to retrieve issue-scoped image metadata, and Issue Details shall display the returned evidence images. | `GET /issues/{issue_id}/images`; `IssueDetails.jsx` gallery. |
| FR-IMG-007 | Authorized users shall be able to delete an issue-scoped image, removing its database record and stored file. | `DELETE /issues/{issue_id}/images/{image_id}` and `_remove_stored_file`. |
| FR-IMG-008 | Image upload and deletion shall be limited to an admin, the reporting citizen, or the Field Staff user assigned through `issues.assigned_to`; authority users shall not receive image mutation permission from the implemented helper. | `_is_authorized_for_issue` in `backend/app/routes/issue_image.py`; frontend delete visibility checks. |

### 4.5 Assignment Requirements

| ID | Requirement | Implementation evidence |
|---|---|---|
| FR-ASSIGN-001 | Only an admin shall assign an issue through the active assignment endpoint. | `PATCH /issues/{issue_id}/assign` depends on `require_role("admin")`. |
| FR-ASSIGN-002 | The active assignment operation shall accept only an existing user whose role is `field_staff`, write that user ID to `issues.assigned_to`, and change `reported` to `assigned` when applicable. | `assign_issue` in `backend/app/routes/issue.py`; `Issue.assigned_to`. |
| FR-ASSIGN-003 | A Field Staff user shall retrieve only issues assigned to that user. | `GET /issues/assigned` filters directly on `Issue.assigned_to`; Field Staff Dashboard calls it. |
| FR-ASSIGN-004 | A changed assignment shall generate an `issue_assigned` notification for the assigned Field Staff user. | Assignment route calls `create_notification_safe` with `issue_assigned`. |

### 4.6 Status and Progress Requirements

| ID | Requirement | Implementation evidence |
|---|---|---|
| FR-STATUS-001 | The system shall support the statuses `reported`, `assigned`, `in_progress`, `resolved`, and `closed`. | Allowed-status lists in issue routes and the status selector in Issue Details. |
| FR-STATUS-002 | Admin and Field Staff users shall be able to change an issue status, subject to the Field Staff assignment restriction. | `PATCH /issues/{issue_id}/status` with role and assignment checks. |
| FR-STATUS-003 | Each status change shall update the main issue and create an `issue_updates` history record containing the actor, message, status, and timestamp. | `update_issue_status` and `IssueUpdate` model. |
| FR-STATUS-004 | Admin and assigned Field Staff users shall be able to add a progress message, optionally with a supported status, and the optional status shall update the issue. | `POST /issues/{issue_id}/updates` and `IssueUpdateCreate`. |
| FR-STATUS-005 | Authenticated users shall be able to retrieve the issue update timeline, and citizens shall be able to view resulting status/progress information in Issue Details. | `GET /issues/{issue_id}/updates`; `IssueDetails.jsx`; recorded citizen visibility verification. |
| FR-STATUS-006 | A citizen shall not be permitted to change issue status or add a progress update through the protected status/progress endpoints. | Status and update routes require `admin` or `field_staff`; unauthorized citizen rejection is recorded as `STATUS-004`. |

### 4.7 Notification Requirements

| ID | Requirement | Implementation evidence |
|---|---|---|
| FR-NOTIF-001 | Creating an issue shall generate `issue_created` in-app notifications for admin users when notification persistence is available. | Issue creation route queries admin users and calls notification service with `issue_created`. |
| FR-NOTIF-002 | A changed admin assignment shall generate an `issue_assigned` notification for the assigned Field Staff user. | Assignment route and notification service. |
| FR-NOTIF-003 | An authorized status change shall generate a `status_changed` notification for the reporting citizen. | Status route and notification service. |
| FR-NOTIF-004 | An authorized progress update shall generate a `progress_update` notification for the reporting citizen. | Progress route and notification service. |
| FR-NOTIF-005 | An authenticated user shall be able to retrieve their notifications, query their unread count, and mark one of their own notifications as read. | `/notifications/`, `/notifications/unread-count`, and `PATCH /notifications/{notification_id}/read`; notification service/repository. |

Notifications are database-backed in-app records. Email, SMS, push, and external notification-provider delivery are not current functional requirements.

### 4.8 Role and Authorization Requirements

| ID | Requirement | Implementation evidence |
|---|---|---|
| FR-RBAC-001 | The system shall represent the roles `citizen`, `admin`, `authority`, and `field_staff`. | `UserRole` enum, `User.role`, and role-specific frontend pages. |
| FR-RBAC-002 | Citizen issue access and mutation operations shall enforce reporter ownership where the route implements ownership checks. | Issue route ownership checks; `GET /issues/my`; image authorization helper. |
| FR-RBAC-003 | Admin-only operations shall include managed-user creation and active issue assignment; admin may also use the implemented administrative issue-management operations. | `require_role("admin")` in user and assignment routes; Admin Dashboard. |
| FR-RBAC-004 | Authority users shall receive the implemented all-issue viewing access and Authority Dashboard workflow, without being treated as admins for admin-only mutations. | `GET /issues/` allows `admin` and `authority`; assignment route allows admin only; Authority Dashboard role guard. |
| FR-RBAC-005 | Field Staff issue operations shall be limited to issues assigned to the authenticated Field Staff user through `issues.assigned_to`. | Assignment checks in status, progress, detail-update, and image mutation routes. |
| FR-RBAC-006 | Missing, invalid, expired, or unusable Bearer credentials shall be rejected rather than treated as authenticated. | `get_current_user` returns HTTP 401 for missing/invalid credentials; the exact negative runtime case is `AUTH-005`, currently Not recorded. |

### 4.9 Dashboard and Interface Requirements

| ID | Requirement | Implementation evidence |
|---|---|---|
| FR-DASH-001 | The citizen dashboard shall provide navigation to issue reporting and the citizen’s own issue list. | `Dashboard.jsx`, `MyIssues.jsx`, and protected routes in `App.jsx`. |
| FR-DASH-002 | The Admin Dashboard shall display issue summary counts, list all issues, expose issue details, and provide Field Staff assignment controls. | `AdminDashboard.jsx`; `/issues/` and `/issues/{issue_id}/assign`. |
| FR-DASH-003 | The Authority Dashboard shall display issue summary counts and filter all-issue results by status and priority. | `AuthorityDashboard.jsx`; all-issue API access. |
| FR-DASH-004 | The Field Staff Dashboard shall display assigned-issue summary counts, provide status filtering, and link to assigned issue details. | `FieldStaffDashboard.jsx`; `/issues/assigned`. |
| FR-DASH-005 | The protected frontend shall redirect unauthenticated users to login and provide shared navigation for authenticated pages. | `ProtectedRoute.jsx`, `Navbar.jsx`, and protected routes in `App.jsx`. |
| FR-DASH-006 | The Issue Details interface shall present issue fields, status, assignment, optional map, evidence gallery, and progress timeline, with status/progress controls only for admin or Field Staff users. | `IssueDetails.jsx`; role checks and API calls. |

## 5. Non-Functional Requirements

The following non-functional requirements describe qualities and constraints supported by the implementation. No formal service-level agreement, response-time target, availability percentage, or production-scale capacity claim is made.

### 5.1 Security Requirements

| ID | Requirement | Implementation evidence |
|---|---|---|
| NFR-SEC-001 | Passwords shall not be stored as plaintext. | PassLib `CryptContext` with bcrypt in `backend/app/security.py`; registration stores `password_hash`. |
| NFR-SEC-002 | JWT signing shall require an environment-provided secret key and shall not silently use an insecure fallback. | `SECRET_KEY` is required in `security.py`; local environment configuration is documented. |
| NFR-SEC-003 | Protected API calls shall use HTTP Bearer JWT authentication. | FastAPI `HTTPBearer`, `get_current_user`, and Axios Authorization interceptor. |
| NFR-SEC-004 | Authorization shall combine role checks with ownership or assignment checks where the operation is issue-scoped. | `require_role`, issue reporter ownership checks, and `Issue.assigned_to` checks. |
| NFR-SEC-005 | Structured requests shall be validated before persistence, including email format and coordinate ranges/pair consistency. | Pydantic schemas, `EmailStr`, coordinate bounds, and the coordinate-pair validator. |
| NFR-SEC-006 | Evidence-image requests shall be validated by supported content type, extension, signature, size, and issue authorization. | `_validate_image`, `MAX_IMAGE_SIZE`, and `_is_authorized_for_issue`. |
| NFR-SEC-007 | Stored image deletion shall validate the image URL path before removing a local file. | `_stored_file_path` prevents unsafe path traversal before `_remove_stored_file`. |
| NFR-SEC-008 | Image deletion shall be constrained to the requested issue and image record. | The delete route matches both `IssueImage.id` and `IssueImage.issue_id` before authorization and removal. |

### 5.2 Performance and Operational Requirements

| ID | Requirement | Implementation evidence |
|---|---|---|
| NFR-PERF-001 | The system shall support the implemented local request/response workflows through FastAPI, SQLAlchemy, and the React client without asserting a numeric response-time target. | FastAPI route handlers, SQLAlchemy sessions, Axios client, and completed local runtime evidence. No SLA or benchmark target is claimed. |

The project does not define formal latency, throughput, concurrency, uptime, or capacity requirements. These remain outside the verified capstone baseline.

### 5.3 Usability Requirements

| ID | Requirement | Implementation evidence |
|---|---|---|
| NFR-USAB-001 | The system shall provide browser-based forms and role-specific pages for registration, login, reporting, issue review, dashboards, notifications, and Issue Details. | React pages and protected routes under `frontend/src/`. |
| NFR-USAB-002 | The issue-reporting interface shall provide interactive map feedback and a clear optional-location fallback. | `LocationPicker.jsx` displays a marker/coordinates or explains that map selection is optional. |
| NFR-USAB-003 | Dashboards shall present filtered issue lists and summary counts appropriate to the user’s implemented role workflow. | Admin, Authority, and Field Staff dashboard components. |

No separate responsive-design, accessibility-conformance, usability-study, or browser-compatibility test result is recorded in `docs/TESTING.md`.

### 5.4 Maintainability Requirements

| ID | Requirement | Implementation evidence |
|---|---|---|
| NFR-MAINT-001 | The application shall keep the React/Vite frontend and FastAPI backend in separate project areas. | `frontend/` and `backend/` repository structure. |
| NFR-MAINT-002 | Backend route groups shall be organized into modules, with supporting service/repository modules used for notifications and image operations where implemented. | `backend/app/routes/`, `services/`, and `repositories/`. |
| NFR-MAINT-003 | Runtime database and JWT configuration shall be supplied through environment variables rather than committed credentials. | `database.py` reads `DATABASE_URL`; `security.py` requires `SECRET_KEY`; `.env` is ignored. |

### 5.5 Data Integrity Requirements

| ID | Requirement | Implementation evidence |
|---|---|---|
| NFR-DATA-001 | Structured issue, user, update, image-reference, department, assignment-model, and notification data shall persist through SQLAlchemy models backed by PostgreSQL. | Models under `backend/app/models/`, shared database session, and PostgreSQL configuration. |
| NFR-DATA-002 | Issue data shall preserve reporter ownership, optional coordinates, controlled status values, and active assignment identity. | `Issue` model; issue schemas/routes; `issues.reported_by`, `latitude`, `longitude`, `status`, and `assigned_to`. |
| NFR-DATA-003 | Issue updates, images, and notifications shall remain associated with their relevant issue or user, and notification read operations shall be user-scoped. | Foreign keys/model fields, issue-scoped routes, and notification repository/service behavior. |

### 5.6 Compatibility and Runtime Requirements

| ID | Requirement | Implementation evidence |
|---|---|---|
| NFR-COMP-001 | The backend shall run in the documented local environment using Python-compatible FastAPI/Uvicorn dependencies and PostgreSQL. | `backend/requirements.txt`, FastAPI application, Uvicorn startup, PostgreSQL configuration, and local runtime evidence. |
| NFR-COMP-002 | The frontend shall run as a browser-based React/Vite application using the declared npm dependencies and scripts. | `frontend/package.json`, React/Vite source, `npm run lint`, and `npm run build`. |
| NFR-COMP-003 | Map functionality shall depend on network access to OpenStreetMap tile URLs when map tiles are displayed. | Leaflet `TileLayer` URLs in `LocationPicker.jsx` and `IssueLocationMap.jsx`. |

## 6. Data Requirements

### 6.1 User

The `users` table stores `id`, `name`, unique `email`, `password_hash`, and `role`. The implemented roles are `citizen`, `admin`, `authority`, and `field_staff`. Users report issues, receive notifications, and may be referenced by the active issue assignment value.

### 6.2 Issue

The `issues` table stores the primary civic report:

- `id`
- `title`
- `description`
- `category`
- `priority`
- `severity`
- `status`
- nullable textual `location`
- nullable `latitude`
- nullable `longitude`
- non-null `reported_by`
- nullable `assigned_to`

The active assignment relationship is represented by `issues.assigned_to = users.id`. Coordinates are optional, but the issue schema requires latitude and longitude to appear together when supplied.

### 6.3 IssueUpdate

The `issue_updates` table stores issue history and progress records with `issue_id`, `updated_by`, `message`, optional `status`, and `created_at`. Status changes and progress updates are returned to the Issue Details timeline.

### 6.4 IssueImage

The `issue_images` table stores evidence references with `id`, `issue_id`, `image_url`, and optional generated `file_name`. The image bytes are stored under the runtime `backend/uploads/issues/` directory, while the database stores the issue relationship and URL metadata.

### 6.5 Department

The `departments` table stores `id`, unique `name`, optional `description`, and `is_active`. The current `Issue` model does not contain an active department foreign-key field, so department records are documented as a persisted model rather than an active issue-assignment requirement.

### 6.6 Notification

The `notifications` table stores `user_id`, optional `issue_id`, `title`, `message`, `notification_type`, `is_read`, and `created_at`. Current notification types generated by the implemented lifecycle are `issue_created`, `issue_assigned`, `status_changed`, and `progress_update`.

### 6.7 Assignment / legacy assignment structure

The repository contains an `assignments` model with issue/user assignment fields, assignment status, and timestamps. It is retained for completeness and historical structure, but the legacy router is not mounted and it is not the active source of truth. Current assignment requirements and traceability use `issues.assigned_to` and the mounted issue assignment route.

### 6.8 Data integrity boundaries

PostgreSQL is required for the database-backed application runtime. Image files are local runtime data rather than database blobs. The system does not claim a public data store, cloud backup, archival policy, or cross-system synchronization.

## 7. Interface Requirements

### 7.1 User Interface

The React/Vite frontend shall provide the implemented pages and workflows for:

- Login and registration.
- Citizen dashboard and personal issues.
- Issue reporting.
- Issue Details and timeline.
- Admin Dashboard.
- Authority Dashboard.
- Field Staff Dashboard.
- Notifications.

React Router defines protected routes, `ProtectedRoute` redirects users without an access token to login, and shared navigation is provided by `Navbar`.

### 7.2 API Interface

The frontend shall communicate with the FastAPI backend through Axios and JSON HTTP requests for registration, login, issue creation, issue retrieval, assignment, status changes, progress updates, and notifications. The backend exposes route groups under `/auth`, `/users`, `/issues`, `/notifications`, and related issue-image paths, plus `/health` and standard FastAPI documentation.

The frontend API client currently targets `http://127.0.0.1:8000` for the local runtime. Responses are used to update React page state and rendered views.

### 7.3 Authentication Interface

Protected frontend requests shall include `Authorization: Bearer <token>` when an access token is available. The backend shall validate that token, load the corresponding user, and apply role/ownership/assignment checks before protected operations.

### 7.4 Image Upload Interface

Evidence-image upload shall use `multipart/form-data` with a `file` field at `POST /issues/{issue_id}/images`. The Axios client removes the default JSON content type for `FormData` requests so the browser can supply the multipart boundary. Image metadata is returned as JSON, and stored files are referenced through `/uploads/issues/` URLs.

### 7.5 Map Interface

The report page shall use React Leaflet/Leaflet to render an OpenStreetMap tile layer and capture an optional map click. Issue Details shall render a read-only marker map only when both coordinate values exist. The frontend shall retain textual location/fallback behavior when coordinates are unavailable.

## 8. Security Requirements Matrix

| ID | Requirement | Implemented mechanism |
|---|---|---|
| NFR-SEC-001 | Passwords must not be stored as plaintext. | PassLib with bcrypt hashes passwords before the `password_hash` field is persisted. |
| NFR-SEC-002 | JWT signing must use configured secret material. | `SECRET_KEY` is read from the environment and startup raises an error when it is absent. |
| NFR-SEC-003 | Protected API operations require authentication. | FastAPI HTTP Bearer handling, JWT verification, subject parsing, and current-user lookup. |
| NFR-SEC-004 | Role-restricted actions must reject disallowed roles. | `require_role` returns HTTP 403 for roles outside the endpoint allow-list. |
| NFR-SEC-005 | Ownership and assignment rules must restrict issue operations. | Reporter ownership checks and direct `Issue.assigned_to` comparisons. |
| NFR-SEC-006 | Structured inputs must be validated. | Pydantic models, `EmailStr`, coordinate bounds, and coordinate-pair validation. |
| NFR-SEC-007 | Image uploads must be validated and bounded. | Content type, extension, signature, and five-megabyte checks. |
| NFR-SEC-008 | Image deletion must be constrained to safe issue-scoped files. | Issue/image ID matching, authorization checks, and resolved safe-path validation. |

`AUTH-005` and `RBAC-004` remain recorded as `Not recorded` in `docs/TESTING.md`; this requirements document does not reinterpret either as a successful negative test.

## 9. Business Rules

1. Public registration creates a `citizen` account; the registration route does not accept a caller-selected elevated role.
2. Duplicate registration emails are rejected by the authentication route.
3. Administrative user creation is protected by the admin role requirement on `/users/`.
4. A citizen-created issue is associated with the authenticated reporter through `reported_by`.
5. Issue categories displayed by the current report form are Road, Street Light, Waste, Water, Traffic, and Other.
6. Priority and severity are captured as issue fields; the report form currently offers low, medium, and high values.
7. Coordinates are optional. If supplied, latitude and longitude must be supplied together and must be within their valid ranges.
8. The active assignment workflow uses `issues.assigned_to`; it does not use the legacy `/assignments` router/table as the required current path.
9. Only an admin can assign an issue, and the target user must have the `field_staff` role.
10. Assigning a currently `reported` issue changes its status to `assigned`.
11. Field Staff retrieval and mutation checks compare the authenticated Field Staff user ID with `issues.assigned_to`.
12. Status changes are restricted to admin and Field Staff users; Field Staff status changes are limited to assigned issues.
13. Supported statuses are `reported`, `assigned`, `in_progress`, `resolved`, and `closed`.
14. Status changes create issue-update history records; progress updates may also include a supported status and update the main issue status.
15. Citizens can view issue details and progress information but cannot use the protected status/progress mutation endpoints.
16. New issue, assignment, status, and progress lifecycle events generate the corresponding database-backed in-app notification types when persistence succeeds.
17. Users can retrieve their own notifications, obtain their unread count, and mark their own notifications as read.
18. Evidence uploads are limited to JPEG, PNG, and WEBP files no larger than five megabytes, with content and signature validation.
19. Evidence retrieval is issue-scoped. Image mutation is authorized for an admin, the reporting citizen, or the assigned Field Staff user; authority image mutation is not granted by the implemented helper.
20. No current business rule delegates verification, prioritization, or resolution decisions to AI.

## 10. Requirements Traceability Matrix

The matrix below maps the current requirements baseline to implementation evidence and the recorded test IDs in `docs/TESTING.md`. `Not recorded` means implementation/source evidence exists but no corresponding successful runtime test was recorded for that specific requirement.

| Requirement ID | Requirement Summary | Implementation Evidence | Verification/Test ID | Status |
|---|---|---|---|---|
| FR-AUTH-001 | Citizen registration creates a citizen account. | `POST /auth/register`; `User.role = citizen`. | AUTH-001 | Verified |
| FR-AUTH-002 | Duplicate registration email is rejected. | Existing-email check in `auth.py`. | Not recorded | Source evidence only |
| FR-AUTH-003 | JSON login returns a Bearer token and user data. | `POST /auth/login`; frontend token storage. | AUTH-002 | Verified |
| FR-AUTH-004 | Passwords are hashed and verified. | PassLib/bcrypt security functions. | AUTH-004 | Verified |
| FR-AUTH-005 | JWT contains identity/role and expires. | `create_access_token` and login handlers. | AUTH-002, AUTH-003 | Verified |
| FR-AUTH-006 | Protected calls require valid Bearer JWT authentication. | `get_current_user`, HTTP Bearer, Axios interceptor. | AUTH-003 | Verified |
| FR-AUTH-007 | Swagger OAuth2 token flow is available. | `POST /auth/token`. | Not recorded | Source evidence only |
| FR-AUTH-008 | Managed user creation is admin-protected. | `POST /users/` with `require_role("admin")`. | RBAC-003 | Verified for admin access; route-specific creation not separately recorded |
| FR-ISSUE-001 | Citizen can create a structured issue. | `IssueCreate`, `POST /issues/`, `ReportIssue.jsx`. | ISSUE-001, ISSUE-002 | Verified |
| FR-ISSUE-002 | Report form provides the six implemented categories. | Category select in `ReportIssue.jsx`. | Not recorded | Source evidence only |
| FR-ISSUE-003 | Issue stores its authenticated reporter. | `reported_by=current_user.id`. | ISSUE-001, ISSUE-002 | Verified through issue creation flows |
| FR-ISSUE-004 | Priority and severity are persisted/displayed. | Issue model, schema, dashboards, Issue Details. | ISSUE-005 | Verified through Issue Details; no field-specific test ID |
| FR-ISSUE-005 | Citizen retrieves personal issues. | `GET /issues/my`. | ISSUE-003 | Verified |
| FR-ISSUE-006 | Admin/authority can access all-issue listing. | `GET /issues/` role allow-list. | ISSUE-004; RBAC-004 | Admin verified; authority-specific negative result Not recorded |
| FR-ISSUE-007 | Authenticated user can open issue details. | `GET /issues/{issue_id}` and `IssueDetails.jsx`. | ISSUE-005 | Verified |
| FR-ISSUE-008 | Status and active assignment appear in issue details. | `IssueResponse`; Issue Details rendering. | ISSUE-005, ASSIGN-001 | Verified |
| FR-ISSUE-009 | Implemented owner/admin/assigned-staff issue mutations enforce checks. | `PUT`/`DELETE` issue route checks. | Not recorded | Source evidence only |
| FR-MAP-001 | Coordinates are optional. | Nullable schema/model fields; optional picker. | ISSUE-001, MAP-006 | Verified |
| FR-MAP-002 | Leaflet/OpenStreetMap map allows point selection. | `LocationPicker.jsx`. | MAP-001, MAP-002, MAP-003 | Verified |
| FR-MAP-003 | Map coordinates are rounded to six decimals. | Map click handler. | MAP-003 | Verified |
| FR-MAP-004 | Coordinate ranges and coordinate pairing are validated. | Pydantic bounds and model validator. | MAP-004 | Verified through coordinate submission; pair-negative case not separately recorded |
| FR-MAP-005 | Coordinates persist and render a marker. | Issue coordinate fields; `IssueLocationMap.jsx`. | MAP-004, MAP-005 | Verified |
| FR-MAP-006 | Missing coordinates use a textual fallback. | Conditional Issue Details map rendering. | MAP-006 | Verified |
| FR-IMG-001 | Multiple evidence files use multipart upload. | `FormData` in `ReportIssue.jsx`; image route. | IMG-001 | Verified |
| FR-IMG-002 | Only JPEG, PNG, and WEBP are accepted. | Allowed content types/extensions. | IMG-001 | Verified for valid upload; rejection case not separately recorded |
| FR-IMG-003 | Images are limited to five megabytes. | `MAX_IMAGE_SIZE`. | IMG-001 | Verified as part of upload validation; boundary-negative case not separately recorded |
| FR-IMG-004 | Type, extension, and signature are validated. | `_validate_image`. | IMG-001 | Verified for valid upload; each rejection branch not separately recorded |
| FR-IMG-005 | Accepted images use local storage plus image records. | Upload directory and `IssueImage`. | IMG-001 | Verified |
| FR-IMG-006 | Issue images can be retrieved and displayed. | Image GET route and Issue Details gallery. | IMG-002 | Verified |
| FR-IMG-007 | Authorized image deletion removes record/file. | Issue-scoped DELETE and safe file removal. | IMG-003 | Verified |
| FR-IMG-008 | Image mutation is restricted by role/ownership/assignment. | `_is_authorized_for_issue`. | IMG-004 | Verified |
| FR-ASSIGN-001 | Only admin can assign issues. | `PATCH /issues/{issue_id}/assign`; admin dependency. | ASSIGN-001 | Verified |
| FR-ASSIGN-002 | Assignment targets Field Staff and writes `issues.assigned_to`. | `assign_issue`; role check; status transition. | ASSIGN-001 | Verified |
| FR-ASSIGN-003 | Field Staff sees assigned issues only. | `GET /issues/assigned` filters `Issue.assigned_to`. | ASSIGN-002 | Verified |
| FR-ASSIGN-004 | Assignment creates an `issue_assigned` notification. | Assignment route notification call. | NOTIF-002 | Verified |
| FR-STATUS-001 | Supported statuses are reported, assigned, in_progress, resolved, closed. | Allowed-status lists and frontend selector. | STATUS-001 | Verified |
| FR-STATUS-002 | Admin/assigned Field Staff can change status. | Status route role and assignment checks. | STATUS-001 | Verified |
| FR-STATUS-003 | Status changes create history records. | `IssueUpdate` creation in status route. | STATUS-001 | Verified |
| FR-STATUS-004 | Admin/assigned Field Staff can add progress and optional status. | Progress route and schema. | STATUS-002 | Verified |
| FR-STATUS-005 | Users can view the update timeline and citizens see updates. | Update GET route and Issue Details. | STATUS-003 | Verified |
| FR-STATUS-006 | Citizens cannot mutate status/progress. | Role dependency on mutation routes. | STATUS-004 | Verified |
| FR-NOTIF-001 | New issue creates `issue_created` notifications. | Issue route and notification service. | NOTIF-001 | Verified |
| FR-NOTIF-002 | Assignment creates `issue_assigned`. | Assignment route. | NOTIF-002 | Verified |
| FR-NOTIF-003 | Status change creates `status_changed`. | Status route. | NOTIF-003 | Verified |
| FR-NOTIF-004 | Progress creates `progress_update`. | Progress route. | NOTIF-004 | Verified |
| FR-NOTIF-005 | User can list, count unread, and mark own notifications read. | Notification routes/service/repository. | NOTIF-005 | Verified |
| FR-RBAC-001 | Four implemented roles are represented. | `UserRole`, model, dashboards. | RBAC-001, RBAC-003 | Verified for main role workflows |
| FR-RBAC-002 | Citizen issue operations enforce ownership where implemented. | Issue/image ownership checks. | RBAC-001 | Verified |
| FR-RBAC-003 | Admin-only user and assignment actions are protected. | Role dependencies and Admin Dashboard. | RBAC-003, ASSIGN-001 | Verified |
| FR-RBAC-004 | Authority has all-issue viewing but not admin-only assignment. | Issue route allow-list; assignment admin dependency. | RBAC-004 | Not recorded for authority-specific negative test |
| FR-RBAC-005 | Field Staff operations are assignment-scoped. | `Issue.assigned_to` checks in routes. | RBAC-002 | Verified |
| FR-RBAC-006 | Invalid/missing credentials are rejected. | `get_current_user` HTTP 401 behavior. | AUTH-005 | Not recorded |
| FR-DASH-001 | Citizen dashboard links to reporting and personal issues. | `Dashboard.jsx`, `MyIssues.jsx`. | ISSUE-003 | Verified through citizen issue workflow |
| FR-DASH-002 | Admin dashboard summarizes, lists, and assigns issues. | `AdminDashboard.jsx`. | ISSUE-004, ASSIGN-001, RBAC-003 | Verified |
| FR-DASH-003 | Authority dashboard filters issue monitoring by status/priority. | `AuthorityDashboard.jsx`. | RBAC-004 | Not recorded for authority-specific negative test |
| FR-DASH-004 | Field Staff dashboard summarizes and filters assigned issues. | `FieldStaffDashboard.jsx`. | ASSIGN-002 | Verified |
| FR-DASH-005 | Protected routes redirect unauthenticated users and provide navigation. | `ProtectedRoute.jsx`, `App.jsx`, `Navbar.jsx`. | AUTH-003 | Protected access verified; redirect behavior not separately recorded |
| FR-DASH-006 | Issue Details presents details, map, evidence, and timeline with role controls. | `IssueDetails.jsx`. | ISSUE-005, MAP-005, IMG-002, STATUS-003 | Verified |
| NFR-SEC-001 | Passwords are not stored in plaintext. | PassLib/bcrypt. | AUTH-004 | Verified |
| NFR-SEC-002 | JWT secret is required from environment. | `security.py` required `SECRET_KEY`. | QUALITY-004 | Verified as configuration/dependency evidence |
| NFR-SEC-003 | Protected APIs use Bearer JWT. | HTTP Bearer dependency and Axios interceptor. | AUTH-003 | Verified |
| NFR-SEC-004 | Role, ownership, and assignment checks protect operations. | Dependencies and route checks. | RBAC-001, RBAC-002, RBAC-003 | Verified for recorded main workflows |
| NFR-SEC-005 | Structured inputs are validated. | Pydantic, email, coordinate validators. | QUALITY-003, MAP-004 | Syntax/import and coordinate flow verified; not every negative branch recorded |
| NFR-SEC-006 | Image inputs are validated and authorized. | Image validation and authorization helper. | IMG-001, IMG-004 | Verified |
| NFR-SEC-007 | Local image deletion uses safe paths. | `_stored_file_path`. | IMG-003 | Verified through authorized deletion workflow |
| NFR-SEC-008 | Image deletion is constrained to the requested issue and image record. | Issue/image ID matching in the delete route. | IMG-003 | Verified through authorized deletion workflow |
| NFR-PERF-001 | Local request/response workflows operate without a claimed SLA. | FastAPI/SQLAlchemy/Axios local architecture. | Not recorded | No performance target or benchmark is defined |
| NFR-USAB-001 | Browser forms and role-specific pages are provided. | React pages and routes. | QUALITY-002 | Production build verified; no separate usability test recorded |
| NFR-USAB-002 | Map selection provides feedback and optional fallback. | `LocationPicker.jsx`. | MAP-001, MAP-003, MAP-006 | Verified |
| NFR-USAB-003 | Role dashboards provide summaries and filters. | Dashboard components. | ISSUE-004, ASSIGN-002 | Main dashboard workflows verified; authority negative case Not recorded |
| NFR-MAINT-001 | Frontend and backend are separated. | `frontend/` and `backend/`. | QUALITY-004 | Manifest/dependency evidence recorded |
| NFR-MAINT-002 | Backend routes/services/repositories are modularized where implemented. | `backend/app/` structure. | QUALITY-003 | Syntax/import validation recorded |
| NFR-MAINT-003 | Runtime secrets and database configuration use environment variables. | `config.py`, `database.py`, `security.py`. | QUALITY-004 | Configuration/dependency evidence recorded |
| NFR-DATA-001 | Structured data persists through SQLAlchemy/PostgreSQL models. | Models, database session, PostgreSQL configuration. | QUALITY-005 | Verified |
| NFR-DATA-002 | Reporter, coordinates, status, and assignment data remain coherent. | `Issue` model and route validation. | ISSUE-002, MAP-004, ASSIGN-001, STATUS-001 | Verified |
| NFR-DATA-003 | Updates, images, and notifications remain issue/user scoped. | Foreign keys and scoped routes/services. | IMG-002, STATUS-003, NOTIF-005 | Verified |
| NFR-COMP-001 | Backend supports documented local Python/FastAPI/PostgreSQL runtime. | Requirements, FastAPI/Uvicorn, database configuration. | QUALITY-003, QUALITY-005, QUALITY-006 | Verified |
| NFR-COMP-002 | Frontend supports documented React/Vite/npm runtime. | Package scripts and frontend source. | QUALITY-001, QUALITY-002 | Verified |
| NFR-COMP-003 | Map tiles depend on OpenStreetMap network access. | Leaflet TileLayer configuration. | MAP-002 | Verified |

### Traceability interpretation

- `Verified` means the referenced test ID is recorded as passing in `docs/TESTING.md`.
- `Not recorded` means the implementation/source supports the requirement, but the corresponding specific runtime result was not recorded.
- `AUTH-005` is explicitly `Not recorded` in `docs/TESTING.md`; it is not presented as a successful negative test here.
- `RBAC-004` is explicitly `Not recorded` in `docs/TESTING.md`; it is not presented as a successful authority-specific negative test here.
- `QUALITY-001` and `QUALITY-002` represent the recorded frontend lint/build checks; the later successful GitHub Actions run for commit `699c80f` confirms the configured CI workflow completed both validation jobs, but it does not change the scope of the runtime test IDs.

## 11. Requirements Status Summary

| Area | Requirements Defined | Implementation Evidence | Verification Evidence |
|---|---|---|---|
| Authentication | FR-AUTH-001 through FR-AUTH-008 | Auth routes, security module, dependencies, user model, frontend login/register. | AUTH-001 through AUTH-004 verified; AUTH-005 remains Not recorded; source-only items are identified in the matrix. |
| Issue management | FR-ISSUE-001 through FR-ISSUE-009 | Issue model/schema/routes, report form, personal issue view, dashboards, Issue Details. | ISSUE-001 through ISSUE-005 verified; not every mutation/category branch has a separate test. |
| Location/map | FR-MAP-001 through FR-MAP-006 | Pydantic coordinate validation, LocationPicker, IssueLocationMap, issue fields. | MAP-001 through MAP-006 verified. |
| Evidence images | FR-IMG-001 through FR-IMG-008 | Multipart route, image validation, filesystem storage, IssueImage model/service, gallery. | IMG-001 through IMG-004 verified; individual rejection branches are not separately recorded. |
| Assignment | FR-ASSIGN-001 through FR-ASSIGN-004 | Mounted issue assignment route, `Issue.assigned_to`, Field Staff route, notification service. | ASSIGN-001 and ASSIGN-002 verified; assignment notification is covered by NOTIF-002. |
| Status/progress | FR-STATUS-001 through FR-STATUS-006 | Issue routes, IssueUpdate model/schema, Issue Details timeline. | STATUS-001 through STATUS-004 verified. |
| Notifications | FR-NOTIF-001 through FR-NOTIF-005 | Notification model/routes/service/repository and event calls. | NOTIF-001 through NOTIF-005 verified. |
| RBAC | FR-RBAC-001 through FR-RBAC-006 | Role enum, dependencies, ownership/assignment checks, protected dashboards. | RBAC-001 through RBAC-003 verified; RBAC-004 and AUTH-005 remain Not recorded for their specific negative cases. |
| Dashboards/UI | FR-DASH-001 through FR-DASH-006 | React Router, protected pages, role dashboards, Issue Details. | Main issue, dashboard, map, image, and timeline behavior is covered by recorded ISSUE/MAP/IMG/STATUS/RBAC IDs; no separate test exists for every UI control. |
| Security | NFR-SEC-001 through NFR-SEC-008 | Bcrypt, JWT, environment secrets, Pydantic, role checks, image validation/path checks. | AUTH, RBAC, IMG, MAP, and QUALITY evidence; some negative branches remain Not recorded. |
| Performance/operations | NFR-PERF-001 | Local FastAPI/SQLAlchemy/Axios request/response design. | No numeric performance test or SLA is defined. |
| Usability | NFR-USAB-001 through NFR-USAB-003 | React forms, dashboards, map feedback, fallback presentation. | Frontend build and feature verification; no separate usability study is claimed. |
| Maintainability | NFR-MAINT-001 through NFR-MAINT-003 | Repository separation, modular backend folders, environment configuration. | Source and dependency/configuration inspection; no dedicated maintainability test is claimed. |
| Data integrity | NFR-DATA-001 through NFR-DATA-003 | SQLAlchemy/PostgreSQL models, scoped routes, foreign keys, issue/update/image/notification records. | QUALITY-005, issue/map/assignment/status/image/notification verification. |
| Compatibility/runtime | NFR-COMP-001 through NFR-COMP-003 | Python/FastAPI/Uvicorn/PostgreSQL, React/Vite/npm, Leaflet/OpenStreetMap. | QUALITY-001 through QUALITY-006 and MAP-002. |

The separate GitHub Actions workflow evidence is recorded in `docs/TESTING.md`: commit `699c80f` completed both `backend-validation` and `frontend-validation`. This confirms the configured CI validation workflow, not a public deployment or live PostgreSQL integration test.

## 12. Current Scope and Limitations

- The application is verified for local runtime with a browser frontend, FastAPI/Uvicorn backend, and PostgreSQL database.
- The frontend currently targets the local backend address `http://127.0.0.1:8000`.
- No public deployment or cloud deployment is claimed.
- No deployment URL, production hosting, HTTPS termination, or cloud database is provided.
- The GitHub Actions workflow validates configured syntax/import, lint, and build steps; it does not run a live PostgreSQL integration test.
- OpenStreetMap tiles require network access when map features are displayed.
- Issue evidence files use local filesystem storage under `backend/uploads/issues/`.
- A separate formal negative result remains Not recorded for `AUTH-005` invalid authentication behavior.
- A separate authority-specific negative result remains Not recorded for `RBAC-004`.
- The legacy assignment model/table remains in the repository but is not the active source of truth.
- The implementation does not claim rate limiting, external identity providers, email/SMS/push notification delivery, cloud secret management, or production availability guarantees.

These limitations describe the verified boundary of the capstone implementation; they do not invalidate the implemented local workflows.

## 13. Future Requirements

The following are FUTURE / PLANNED requirements and are intentionally excluded from the current implemented traceability matrix:

- **FUTURE-AI-001:** Analyze uploaded infrastructure images using computer vision to identify issue types or visible damage.
- **FUTURE-AI-002:** Estimate issue severity from image and issue data.
- **FUTURE-AI-003:** Recommend an issue priority for administrator review.
- **FUTURE-DEP-001:** Deploy the application to a public or cloud environment with production runtime controls.
- **FUTURE-INT-001:** Integrate with external government or municipal systems.
- **FUTURE-NOTIF-001:** Add email, SMS, or push-notification delivery through an external provider.

These are planning items only. No AI implementation, public deployment, government integration, or external notification delivery is claimed in the current requirements baseline.

## 14. Conclusion

This specification establishes a formal requirements baseline for the implemented Smart Public Infrastructure Issue Reporting System. It covers authentication, role-based issue workflows, issue data, optional map coordinates, evidence images, active Field Staff assignment through `issues.assigned_to`, status/progress history, database-backed notifications, dashboards, interfaces, security, data integrity, local runtime constraints, and future boundaries.

The traceability matrix connects those requirements to actual repository implementation evidence and the recorded verification IDs in `docs/TESTING.md`. It explicitly preserves the distinction between verified behavior and source-supported behavior without claiming tests that were not recorded. In particular, `AUTH-005` and `RBAC-004` remain Not recorded, while the successful GitHub Actions run for commit `699c80f` is documented as CI validation evidence only.

The requirements baseline is therefore complete for the currently implemented local system and provides formal traceability without expanding the project’s actual functionality.
