# Implemented Features

This document lists the features currently implemented and verified in the Smart Public Infrastructure Issue Reporting System. Planned AI functionality and unperformed deployment work are intentionally excluded.

## Citizen account

- Citizen registration with name, email, and password.
- Citizen login and protected-session handling.
- Citizen dashboard and personal issue list.
- Citizen access to issue details, status, progress, notifications, and authorized evidence operations for owned issues.

## Authentication

- Password hashing with bcrypt through PassLib.
- JWT access-token creation and verification.
- Bearer-token protection for authenticated API routes.
- Environment-required `SECRET_KEY` configuration.

## Role-based access

- Citizen, admin, authority, and Field Staff roles are represented in the application.
- Shared role checks restrict protected operations.
- Ownership and assignment checks protect issue mutations.
- Field Staff access is scoped to issues assigned through `issues.assigned_to`.

## Issue reporting

- Issue title and description.
- Issue category selection.
- Priority and severity fields.
- Location text.
- Citizen-associated issue creation.
- Citizen issue retrieval.
- Admin and authority all-issue listing.
- Issue Details view with status and assignment information.

## Issue categories, priority, and severity

The current report form exposes these category choices:

- Road
- Street Light
- Waste
- Water
- Traffic
- Other

Priority and severity values are captured and displayed as part of the issue workflow.

## Location coordinates

- Optional Leaflet map selection.
- OpenStreetMap tile layer.
- Latitude and longitude capture to six decimal places.
- Coordinate persistence on the issue record.
- Read-only Issue Details map marker.
- Graceful no-coordinate fallback.

## Evidence images

- Multiple image selection from the report form.
- JPEG, PNG, and WEBP validation.
- File-size and file-signature checks.
- Runtime storage under `backend/uploads/issues/`.
- Database image records associated with issues.
- Authenticated retrieval and display.
- Authorized issue-scoped deletion of the database record and stored file.

## Admin issue management

- Admin issue listing.
- Status summary cards.
- Issue review links to Issue Details.
- Assignment to a Field Staff user through the active issue route.

## Field Staff assignment and workflow

- Admin assignment through `PATCH /issues/{issue_id}/assign`.
- Active assignment source of truth: `issues.assigned_to`.
- Field Staff assigned-issue retrieval.
- Field Staff status and progress management for assigned issues.
- Assignment notification.

## Status tracking

Supported issue statuses in the implemented route include:

- `reported`
- `assigned`
- `in_progress`
- `resolved`
- `closed`

Status changes are reflected on the issue and recorded in `issue_updates`.

## Progress timeline

- Admin and Field Staff progress messages.
- Optional status value on a progress update.
- Issue Details timeline retrieval.
- Citizen visibility of updated issue information.

## Notifications

- New issue notification.
- Assignment notification.
- Status-change notification.
- Progress-update notification.
- User notification list.
- Unread count.
- Mark-as-read operation.

## Role-specific dashboards

- Citizen dashboard and personal issue views.
- Admin Dashboard for issue management and Field Staff assignment.
- Authority Dashboard for issue monitoring and filtering.
- Field Staff Dashboard for assigned issues and status filtering.
- Notifications page.

## Not implemented in the current feature set

- AI/computer-vision issue classification.
- Automated severity or priority recommendation by AI.
- Public cloud deployment.
- Automated government-system integration.
