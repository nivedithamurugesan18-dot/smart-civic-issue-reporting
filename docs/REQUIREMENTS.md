# System Requirements

## 1. Project Overview

### Project Title

Smart Public Infrastructure Issue Reporting and Prioritization System

### Purpose

The system will provide a centralized web-based platform for
reporting, managing, prioritizing, assigning, tracking, and resolving
public infrastructure issues.

Citizens can report issues with descriptions, photographs, and
location information. Administrators can verify reports, assign
priority, and assign issues to responsible departments or field staff.
Field staff can update the progress of assigned issues and provide
resolution evidence.

The system will also provide map-based monitoring and administrative
analytics.

A future enhancement will introduce AI-based image analysis to assist
with infrastructure issue detection and severity or priority
recommendation.


## 2. Target Users

### 2.1 Citizen

The citizen is the person who identifies and reports a public
infrastructure issue.

The citizen should be able to:

- Register an account.
- Log in securely.
- Create an infrastructure issue report.
- Select an issue category.
- Enter an issue description.
- Upload photographic evidence.
- Provide the issue location.
- View submitted reports.
- Track issue status.
- View resolution information.


### 2.2 Administrator / Municipal Officer

The administrator manages the reported infrastructure issues.

The administrator should be able to:

- Log in securely.
- View all reported issues.
- Review issue information and evidence.
- Verify or reject reports.
- Assign issue priority.
- Assign issues to departments.
- Assign issues to field staff.
- Monitor issue status.
- View issue statistics.
- Manage relevant users and departments.
- Monitor issues using the map interface.


### 2.3 Field Staff

Field staff handle assigned infrastructure issues.

The field staff should be able to:

- Log in securely.
- View assigned issues.
- View issue descriptions and photographs.
- View issue locations.
- Update issue status.
- Add maintenance remarks.
- Upload resolution evidence.
- Mark an issue as resolved.


## 3. Functional Requirements

Functional requirements define what the system must do.

### FR-01: User Registration

The system shall allow citizens to create an account using the
required registration information.

The system shall validate the submitted information before creating
the account.


### FR-02: User Authentication

The system shall allow registered users to securely log in.

The system shall authenticate users before providing access to
protected features.


### FR-03: Role-Based Access

The system shall support different user roles.

Initial roles:

- Citizen
- Administrator
- Field Staff

Users shall only be allowed to access operations permitted for their
role.


### FR-04: Create Infrastructure Issue

A citizen shall be able to create an infrastructure issue report.

The report shall contain:

- Issue category
- Description
- Location
- Photograph
- Submission timestamp


### FR-05: Issue Categories

The initial system shall support the following issue categories:

- Pothole
- Road Damage
- Broken Streetlight
- Damaged Traffic Sign

The system architecture should allow additional categories to be
added later.


### FR-06: Image Upload

The system shall allow citizens to upload photographs as evidence
for an infrastructure issue.

The system shall associate uploaded images with the corresponding
issue.


### FR-07: Location Capture

The system shall store geographical information for reported issues.

The issue location shall include geographical coordinates such as:

- Latitude
- Longitude

Where available, an address or location description may also be
stored.


### FR-08: View Submitted Issues

Citizens shall be able to view the infrastructure issues they have
submitted.

The citizen shall be able to view:

- Issue category
- Description
- Image
- Location
- Priority
- Current status
- Submission date
- Resolution information


### FR-09: Issue Verification

Administrators shall be able to review submitted infrastructure
issues.

The administrator shall be able to:

- Verify a valid report.
- Reject an invalid or inappropriate report.
- Add remarks where necessary.


### FR-10: Issue Prioritization

Administrators shall be able to assign a priority to a verified
issue.

Initial priority levels:

- Low
- Medium
- High
- Critical

Priority may consider factors such as:

- Reported severity
- Safety impact
- Issue category
- Location
- Available operational information

AI-based priority recommendation will be considered during the
enhancement phase.


### FR-11: Department Assignment

Administrators shall be able to assign verified issues to the
appropriate department.


### FR-12: Field Staff Assignment

Administrators shall be able to assign an issue to a field staff
member.

The assignment shall be associated with the relevant issue and
department.


### FR-13: Issue Status Management

The system shall maintain a controlled issue status workflow.

Initial statuses:

1. Reported
2. Under Review
3. Verified
4. Assigned
5. In Progress
6. Resolved
7. Closed

Only authorized users shall be allowed to perform relevant status
changes.


### FR-14: Status History

The system shall maintain a history of important issue status
changes.

Each status history record should contain:

- Issue
- Previous/current status information
- User who performed the action
- Remarks
- Timestamp


### FR-15: Field Staff Progress Update

Field staff shall be able to update the progress of their assigned
issues.

They shall be able to add remarks describing the maintenance work.


### FR-16: Resolution Evidence

Field staff shall be able to upload photographs or other permitted
evidence showing the completed maintenance work.

The evidence shall be associated with the corresponding issue.


### FR-17: Issue Tracking

Citizens shall be able to track the status of their submitted
issues.

The system shall provide sufficient status information to show the
progress from reporting to resolution.


### FR-18: Notifications

The system should provide notifications for important issue events,
such as:

- Issue verification
- Issue assignment
- Status update
- Issue resolution

The exact notification mechanism will be finalized during
development.


### FR-19: Map-Based Monitoring

The administrator shall be able to view reported infrastructure
issues on an interactive map.

The map shall use the stored geographical coordinates of issues.


### FR-20: Administrative Dashboard

The administrator shall have access to a dashboard showing useful
infrastructure issue statistics.

Possible statistics include:

- Total reported issues
- Verified issues
- Assigned issues
- In-progress issues
- Resolved issues
- High-priority issues
- Issues by category
- Issues by location


### FR-21: Issue Search and Filtering

The administrator should be able to search and filter issues based
on available information such as:

- Issue category
- Status
- Priority
- Location
- Date
- Assigned department


### FR-22: AI Enhancement

During the later enhancement phase, the system may include an
AI-based image analysis module.

The AI enhancement may:

- Analyze uploaded infrastructure images.
- Detect infrastructure-related damage.
- Classify the detected issue.
- Estimate severity.
- Recommend a priority level.

The AI output shall be treated as decision support and shall not
replace administrator verification.


## 4. Non-Functional Requirements

### NFR-01: Security

The application shall protect user authentication information.

Passwords shall not be stored as plain text.

Protected API endpoints shall require appropriate authentication.


### NFR-02: Authorization

The application shall enforce role-based authorization.

A user shall not be able to access administrative or field staff
operations without the required role.


### NFR-03: Data Integrity

The system shall maintain relationships between users, issues,
images, assignments, departments, status history, and notifications.

Invalid references and inconsistent records should be prevented
through appropriate database constraints and backend validation.


### NFR-04: Reliability

The application should handle invalid user input without crashing.

API errors should return clear and meaningful responses.


### NFR-05: Usability

The user interface should be simple enough for citizens to report an
issue without extensive technical knowledge.

Important information such as status, priority, and issue location
should be clearly presented.


### NFR-06: Responsiveness

The frontend should provide a usable experience on both desktop and
mobile screen sizes.


### NFR-07: Maintainability

The application shall use a modular architecture so that frontend,
backend, database, authentication, and other modules can be
developed and maintained separately.


### NFR-08: Testability

Important backend business logic shall be covered by automated unit
tests using the selected testing framework.

The Python track requires Pytest for basic unit testing.


### NFR-09: API Consistency

The backend shall expose functionality through REST APIs.

API responses should follow one consistent JSON response structure
throughout the application.

Planned response structure:

{
    "success": true,
    "data": {},
    "message": "Operation completed successfully"
}


### NFR-10: API Documentation

Backend APIs shall be documented using Swagger / OpenAPI.

The documentation should make it possible to understand and test the
available API endpoints.


### NFR-11: Performance

The system should provide reasonable response times for normal
operations such as:

- Login
- Issue creation
- Issue retrieval
- Status updates
- Dashboard data retrieval

Performance optimization will be considered after the core
functionality is implemented.


### NFR-12: Scalability

The application should be designed so that additional issue
categories, users, departments, and infrastructure records can be
supported without major architectural changes.


### NFR-13: Deployment

The final application shall be deployable to cloud hosting.

The college capstone requires the full product to be publicly
accessible by the Review-II stage.


### NFR-14: Version Control

All meaningful project changes shall be tracked using Git and stored
in the GitHub repository.

Commit messages shall follow the required Conventional Commits
format.


## 5. Core Business Rules

### BR-01

A citizen can create an infrastructure report only after successful
authentication.


### BR-02

Every issue must belong to the citizen who created it.


### BR-03

An issue should contain sufficient information before submission,
including category, description, and location.


### BR-04

An issue must be reviewed by an authorized administrator before it
is treated as a verified infrastructure problem.


### BR-05

Only authorized administrators can assign priority to an issue.


### BR-06

Only authorized administrators can assign an issue to a department
or field staff member.


### BR-07

Field staff can update only issues assigned to them.


### BR-08

Citizens can view and track their own submitted issues.


### BR-09

Important issue status changes should be recorded in status history.


### BR-10

An issue should not be marked as closed without completing the
required resolution workflow.


### BR-11

AI recommendations must not automatically override administrator
decisions.


## 6. Issue Lifecycle

The planned issue lifecycle is:

Citizen Reports Issue
        ↓
Reported
        ↓
Administrator Reviews
        ↓
Verified / Rejected
        ↓
Priority Assigned
        ↓
Department / Field Staff Assigned
        ↓
In Progress
        ↓
Resolution Evidence Added
        ↓
Resolved
        ↓
Closed


## 7. MVP Scope

The Minimum Viable Product for Review-I will focus on the core
reporting and management workflow.

### MVP Features

- User registration and login
- Role-based access
- Citizen issue reporting
- Issue category selection
- Issue description
- Image upload
- Location information
- Administrator issue review
- Issue verification
- Priority management
- Department/field staff assignment
- Field staff status updates
- Citizen issue tracking
- Issue status history
- Basic administrator dashboard
- Basic map-based issue display


## 8. Enhancement Scope

The following features are planned for the later enhancement phase
and will not block the initial MVP:

### AI-Based Image Analysis

- Infrastructure damage detection
- Issue classification
- Severity estimation
- Priority recommendation

### Advanced Analytics

- Location-based issue trends
- Resolution-time analysis
- Frequently affected areas
- Category trends
- Department performance indicators


## 9. Out-of-Scope Requirements

The following are not part of the initial capstone implementation:

- Direct integration with official government systems.
- Automated physical repair of infrastructure.
- Emergency service dispatch.
- Nationwide infrastructure monitoring.
- Physical IoT sensor deployment.
- Payment processing.
- Satellite-based infrastructure monitoring.
- Fully autonomous AI decision-making.
- Supporting every possible infrastructure category in the first
  version.


## 10. Third-Party Integrations

### Mapping Integration

The application will use:

- Leaflet
- OpenStreetMap

Purpose:

- Display infrastructure issue locations.
- Support map-based monitoring.
- Help administrators understand issue distribution.


## 11. Core Data Requirements

The planned database entities are:

1. Users
2. Issues
3. Issue Images
4. Departments
5. Assignments
6. Status History
7. Notifications

These entities will be refined and represented in the ER diagram
during the design phase.


## 12. Planned API Areas

The backend REST API will be organized under `/api/`.

Planned API areas include:

### Authentication

- Registration
- Login
- Current user information

### Users

- User information
- Role management where authorized

### Issues

- Create issue
- View issue
- List issues
- Update issue
- Verify issue
- Prioritize issue

### Assignments

- Assign department
- Assign field staff
- View assignments

### Status

- Update status
- View status history

### Images

- Upload issue image
- Upload resolution evidence

### Notifications

- View notifications
- Mark notification as read

### Dashboard

- Issue statistics
- Category statistics
- Status statistics
- Priority statistics


## 13. Acceptance Criteria for the Core Application

The core application will be considered functionally successful
when:

1. A citizen can register and log in.
2. A citizen can submit an infrastructure issue.
3. The issue can include a category, description, photograph, and
   location.
4. The issue is stored correctly in the database.
5. An administrator can review and verify the issue.
6. An administrator can assign priority.
7. An administrator can assign the issue to a department or field
   staff member.
8. Assigned field staff can view their assigned issue.
9. Field staff can update issue progress.
10. Field staff can upload resolution evidence.
11. Citizens can track their submitted issue.
12. Issue status history is maintained.
13. Administrators can view basic issue statistics.
14. Reported issues can be displayed on a map.
15. Protected operations enforce appropriate user roles.


## 14. Quality and Development Constraints

The project will follow the selected Python/FastAPI technology
track.

The application will use:

- React.js for frontend development.
- FastAPI for backend REST APIs.
- PostgreSQL for the database.
- SQLAlchemy for database access.
- JWT-based authentication.
- Leaflet and OpenStreetMap for mapping.
- Pytest for backend unit tests.
- Swagger/OpenAPI for API documentation.
- Git and GitHub for version control.
- GitHub Actions for CI/CD during the development phase.


## 15. Requirement Traceability

The major requirements will be connected to later design and
implementation artifacts.

| Requirement Area | Planned Design / Implementation |
|------------------|---------------------------------|
| Authentication | Auth module + JWT |
| User roles | Role-based authorization |
| Issue reporting | Issue API + Issue form |
| Images | Issue Images entity + upload API |
| Location | Latitude/longitude + map |
| Verification | Issue workflow |
| Priority | Priority business logic |
| Assignment | Assignment entity + APIs |
| Status tracking | Status History entity |
| Notifications | Notifications entity |
| Dashboard | Analytics/dashboard module |
| AI enhancement | Computer vision module |
| Testing | Pytest |
| API documentation | Swagger/OpenAPI |
| CI/CD | GitHub Actions |


## 16. Requirement Status

At this planning stage:

- Problem definition: Completed
- Domain study: Completed
- Technology stack decision: Completed
- Functional requirements: Defined
- Non-functional requirements: Defined
- MVP scope: Defined
- Enhancement scope: Defined
- Database entities: Initial definition completed
- Architecture: To be designed
- ER diagram: To be designed
- Class/module diagram: To be designed
- Database schema: To be designed
- REST APIs: To be implemented
- Frontend: To be implemented
- Testing: To be implemented
- CI/CD: To be implemented
- Cloud deployment: To be implemented
- AI enhancement: Planned for later phase


## 17. Conclusion

The requirements define a practical scope for the Smart Public
Infrastructure Issue Reporting and Prioritization System.

The core MVP focuses on the complete reporting-to-resolution
workflow, while AI and advanced analytics are intentionally
separated into the later enhancement phase.

This approach keeps the project achievable within the capstone
timeline while providing sufficient scope for full-stack development,
database design, testing, deployment, and an AI/Data Science
enhancement.