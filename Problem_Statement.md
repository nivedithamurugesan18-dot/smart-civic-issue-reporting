# Problem Statement

## 1. Title

Smart Public Infrastructure Issue Reporting and Prioritization System

## 2. Domain

Civic Technology / Smart City / Artificial Intelligence and Data Science

## 3. Who is the user? (2-3 user types, with roles)

### 1. Citizen

Citizens are the primary users who can report public infrastructure
issues such as potholes, damaged roads, broken streetlights, and
damaged traffic signs.

Key responsibilities:
- Register and log in to the system.
- Report public infrastructure issues.
- Select the appropriate issue category.
- Upload photographic evidence.
- Provide the issue location.
- Track the status of submitted reports.
- View the resolution details of their reports.

### 2. Administrator / Municipal Officer

Administrators manage and monitor reported infrastructure issues.

Key responsibilities:
- View and verify submitted issue reports.
- Review issue details and evidence.
- Assign priority to reported issues.
- Assign issues to appropriate departments or field staff.
- Monitor issue resolution progress.
- Manage departments and users.
- View dashboard-based infrastructure statistics.

### 3. Field Staff

Field staff are responsible for handling and resolving assigned
infrastructure issues.

Key responsibilities:
- View issues assigned to them.
- Access the reported issue location and details.
- Update the progress of an assigned issue.
- Add remarks about the maintenance work.
- Upload resolution evidence.
- Mark the issue as resolved after completing the work.


## 4. What problem are we solving? (3-5 sentences, real-life example)

Public infrastructure problems such as potholes, damaged roads,
broken streetlights, and damaged traffic signs are often reported
through unstructured or disconnected channels. Citizens may not have
a centralized platform where they can submit an issue along with
photographic evidence and precise location information. Authorities
may also face difficulties in organizing, prioritizing, assigning,
and tracking reported issues efficiently, which can result in delayed
maintenance and poor visibility of unresolved problems.

For example, if a citizen notices a dangerous pothole on a frequently
used road, they may report it through an informal channel or may not
know which department should handle it. Even after reporting, the
citizen may have no way to track whether the issue has been verified,
assigned, or resolved. The proposed system aims to provide a
centralized digital workflow from issue reporting to resolution
tracking.


## 5. Proposed Solution (what the application will do, feature-wise)

The proposed system is a web-based platform that provides a
centralized mechanism for citizens to report and track public
infrastructure issues while helping authorities manage and prioritize
those reports.

### Citizen Features

- User registration and secure login.
- Create a new infrastructure issue report.
- Select an issue category such as:
  - Pothole
  - Road damage
  - Broken streetlight
  - Damaged traffic sign
- Enter a description of the issue.
- Upload one or more photographs as evidence.
- Capture or enter the geographical location of the issue.
- View submitted reports.
- Track the current status of each report.
- View resolution details after the issue is completed.

### Administrator Features

- Secure administrator login.
- View all submitted infrastructure reports.
- Verify and review reported issues.
- Review photographs and location information.
- Assign priority based on issue severity and other relevant factors.
- Assign issues to appropriate departments or field staff.
- Monitor pending, assigned, in-progress, and resolved issues.
- Manage departments and field staff.
- View statistics and analytics through an administrative dashboard.
- Monitor infrastructure issues through a map-based interface.

### Field Staff Features

- Secure field staff login.
- View assigned infrastructure issues.
- View issue description, images, and location.
- Update issue status.
- Add maintenance remarks.
- Upload resolution evidence.
- Mark an issue as resolved after completing the required work.

### Map-Based Features

- Display reported issues on an interactive map.
- Show issue locations using geographical coordinates.
- Allow administrators to identify areas with multiple reported
  infrastructure problems.
- Support location-based issue monitoring using a mapping service.

### Issue Status Workflow

Each reported issue will follow a controlled workflow:

Reported
→ Under Review
→ Verified
→ Assigned
→ In Progress
→ Resolved
→ Closed

This workflow provides a clear history of the issue from the initial
citizen report to final resolution.

### Future AI Enhancement

During the enhancement phase of the project, an AI-based computer
vision module will be integrated into the system.

The AI module will analyze uploaded infrastructure images and assist
in identifying the type of issue, such as a pothole or road damage,
and estimate its severity or priority.

The planned AI workflow is:

Image Upload
→ Image Processing
→ AI-Based Issue Detection
→ Issue Classification
→ Severity Estimation
→ Priority Recommendation

The AI output will assist administrators in making faster and more
consistent prioritization decisions.


## 6. Core Entities / Database Tables (list all, minimum 5)

### 1. Users

Stores information about all registered users.

Important fields:
- user_id
- name
- email
- password_hash
- role
- created_at

### 2. Issues

Stores the main information about infrastructure issue reports.

Important fields:
- issue_id
- user_id
- issue_type
- description
- latitude
- longitude
- address
- priority
- status
- created_at
- updated_at

### 3. Issue Images

Stores photographs associated with infrastructure reports.

Important fields:
- image_id
- issue_id
- image_url
- uploaded_at

### 4. Departments

Stores information about departments responsible for handling
different infrastructure issues.

Important fields:
- department_id
- department_name
- description

### 5. Assignments

Stores assignments of reported issues to field staff.

Important fields:
- assignment_id
- issue_id
- staff_id
- department_id
- assigned_at
- completed_at

### 6. Status History

Stores the history of status changes for each reported issue.

Important fields:
- history_id
- issue_id
- status
- changed_by
- remarks
- changed_at

### 7. Notifications

Stores notifications related to issue updates and assignments.

Important fields:
- notification_id
- user_id
- issue_id
- message
- is_read
- created_at

The planned relationships between these entities will be represented
in the Entity-Relationship diagram during the design phase.


## 7. User Roles & Permissions (minimum 2 distinct roles)

| Role | Permissions |
|------|-------------|
| Citizen | Register, login, create issues, upload images, provide location, view own reports, track issue status |
| Administrator | Login, view all issues, verify reports, set priority, assign issues, manage departments and staff, monitor analytics |
| Field Staff | Login, view assigned issues, update status, add remarks, upload resolution evidence, mark issues as resolved |

The system will implement role-based access control so that users can
access only the functions appropriate to their assigned role.


## 8. Success Criteria

The project will be considered successful when the following
functional and technical objectives are achieved:

1. A citizen should be able to register and securely log in to the
   application.

2. A citizen should be able to create an infrastructure issue report
   containing an issue category, description, photograph, and
   geographical location.

3. A submitted issue should be stored correctly in the database and
   associated with the reporting citizen.

4. An administrator should be able to view, verify, prioritize, and
   assign reported issues.

5. A field staff member should be able to view assigned issues and
   update their progress.

6. Citizens should be able to track the status of their submitted
   issues from reporting through resolution.

7. The system should maintain a history of important issue status
   changes.

8. The application should provide a dashboard for administrators to
   monitor issue statistics and resolution progress.

9. Reported issues should be displayed using an interactive map based
   on their geographical locations.

10. The application should have a clear and modular architecture
    separating frontend, backend, business logic, and database
    responsibilities.

11. The system should be testable and deployable as a publicly
    accessible web application.

12. The later AI enhancement should be capable of assisting with
    infrastructure issue detection and severity or priority
    estimation from uploaded images.


## 9. Out of Scope (clearly list what you will NOT build, to avoid over-commitment)

The following features are outside the scope of the initial
60-day project:

- Direct integration with official government or municipal
  department systems.
- Automated dispatch of emergency services such as police,
  ambulance, or fire services.
- Real-world financial or payment processing.
- Automated physical repair of infrastructure.
- Deployment and maintenance of physical IoT sensor networks.
- Nationwide infrastructure monitoring.
- Satellite-based infrastructure monitoring.
- Real-time integration with every existing traffic management
  system.
- Support for every possible type of public infrastructure in the
  initial version.
- Fully autonomous decision-making by the AI system without human
  verification.

The AI component will be designed as a decision-support feature for
administrators rather than a replacement for human decision-making.


## 10. Chosen Track: Python (FastAPI)

### Frontend

- React.js
- Tailwind CSS
- JavaScript
- Axios
- React Router

### Backend

- Python
- FastAPI
- SQLAlchemy

### Database

- PostgreSQL

### Authentication and Security

- JWT-based authentication
- Password hashing
- Role-based access control
- Environment variables for sensitive configuration

### Maps and Location

- Leaflet
- OpenStreetMap

### Testing

- Pytest

### API Documentation

- FastAPI Swagger / OpenAPI

### Version Control and CI/CD

- Git
- GitHub
- GitHub Actions

### AI Enhancement

- Python
- Pandas
- NumPy
- OpenCV
- YOLO / Computer Vision
- Scikit-learn where required

### Planned Deployment

- React frontend on a cloud hosting platform
- FastAPI backend on a cloud hosting platform
- PostgreSQL using a cloud database service
