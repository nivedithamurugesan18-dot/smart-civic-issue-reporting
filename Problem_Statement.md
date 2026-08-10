# Problem Statement

## 1. Title

Smart Public Infrastructure Issue Reporting and Prioritization System

---

## 2. Domain

Civic Technology / Smart City / Artificial Intelligence and Data Science

---

## 3. Who is the user? (2-3 user types, with roles)

### 1. Citizen

Citizens are the main users of the system. They can report public
infrastructure problems such as potholes, damaged roads, broken
streetlights, and damaged traffic signs.

Key responsibilities:

- Register and log in to the system.
- Report public infrastructure issues.
- Select the appropriate issue category.
- Enter a description of the problem.
- Upload photographic evidence.
- Provide the location of the issue.
- View their submitted reports.
- Track the status of reported issues.
- View resolution details.

### 2. Administrator / Municipal Officer

Administrators are responsible for managing and monitoring reported
infrastructure issues.

Key responsibilities:

- Log in securely.
- View submitted issue reports.
- Review issue descriptions, photographs, and locations.
- Verify or reject reported issues.
- Assign priority to verified issues.
- Assign issues to the appropriate department.
- Assign issues to field staff.
- Monitor issue progress and resolution.
- Manage departments and field staff.
- View infrastructure statistics and analytics.
- Monitor reported issues using a map.

### 3. Field Staff

Field staff are responsible for handling infrastructure issues
assigned to them.

Key responsibilities:

- Log in securely.
- View assigned issues.
- View issue descriptions, photographs, and locations.
- Update the progress of assigned issues.
- Add maintenance remarks.
- Upload resolution evidence.
- Mark an issue as resolved after completing the work.

---

## 4. What problem are we solving? (3-5 sentences, real-life example)

Public infrastructure problems such as potholes, damaged roads,
broken streetlights, and damaged traffic signs can affect public
safety and daily transportation. Citizens may not have a simple
centralized platform to report these problems with proper photographs
and exact location information. Authorities may also face difficulty
in organizing, verifying, prioritizing, assigning, and tracking a
large number of infrastructure complaints. As a result, important
issues may remain unresolved for a long time.

For example, a citizen may notice a large pothole on a busy road.
They may report the problem through an informal channel, but the
responsible department may not receive enough information about the
exact location or severity of the problem. Even after reporting, the
citizen may not know whether the issue was verified, assigned to a
worker, or resolved. The proposed system provides a centralized
workflow from issue reporting to final resolution.

---

## 5. Proposed Solution (what the application will do, feature-wise)

The proposed system is a web-based platform that connects citizens,
administrators, and field staff through a centralized infrastructure
issue management workflow.

### Citizen Features

- User registration and secure login.
- Create a new infrastructure issue report.
- Select an issue category.
- Enter a detailed description.
- Upload one or more photographs.
- Provide the geographical location.
- View previously submitted reports.
- Track the current status of each report.
- View resolution information after completion.

Initial issue categories include:

- Pothole
- Road Damage
- Broken Streetlight
- Damaged Traffic Sign

The system will be designed so that additional categories can be
added later.

### Administrator Features

- Secure administrator login.
- View all submitted infrastructure reports.
- Review issue descriptions, photographs, and locations.
- Verify or reject reports.
- Assign issue priority.
- Assign issues to appropriate departments.
- Assign issues to field staff.
- Monitor pending, assigned, in-progress, and resolved issues.
- Manage departments and field staff.
- View issue statistics through an administrative dashboard.
- Monitor infrastructure issues through an interactive map.

### Field Staff Features

- Secure field staff login.
- View assigned infrastructure issues.
- View issue descriptions, photographs, and locations.
- Update issue status.
- Add maintenance remarks.
- Upload resolution evidence.
- Mark assigned issues as resolved after completing the work.

### Map-Based Features

- Display reported infrastructure issues on an interactive map.
- Store issue latitude and longitude.
- Show issue locations using map markers.
- Help administrators identify areas with multiple infrastructure
  problems.
- Support location-based issue monitoring.

The planned mapping technologies are Leaflet and OpenStreetMap.

### Issue Status Workflow

Each issue will follow a controlled workflow:

Reported
→ Under Review
→ Verified
→ Assigned
→ In Progress
→ Resolved
→ Closed

This workflow provides a clear history of the issue from the initial
citizen report to final resolution.

### Issue Prioritization

Administrators can assign a priority to verified issues.

Initial priority levels are:

- Low
- Medium
- High
- Critical

Priority can consider factors such as the type of issue, reported
severity, safety impact, and location.

### Notifications

The system can provide notifications for important events such as:

- Issue verification
- Issue assignment
- Status changes
- Issue resolution

### Future AI Enhancement

During the later enhancement phase, an AI-based computer vision module
will be integrated into the system.

The AI module will analyze uploaded infrastructure images and assist
with:

- Identifying the type of infrastructure issue.
- Detecting visible damage.
- Estimating issue severity.
- Recommending an appropriate priority level.

The planned AI workflow is:

Image Upload
→ Image Processing
→ AI-Based Issue Detection
→ Issue Classification
→ Severity Estimation
→ Priority Recommendation

The AI will be used as a decision-support system. The final
verification and priority decision will remain with the authorized
administrator.

---

## 6. Core Entities / Database Tables (list all, minimum 5)

The system will use the following core database entities.

### 1. Users

Stores information about citizens, administrators, and field staff.

Important fields:

- user_id
- name
- email
- password_hash
- role
- created_at

### 2. Issues

Stores the main information about reported infrastructure problems.

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

Stores photographs associated with infrastructure issue reports.

Important fields:

- image_id
- issue_id
- image_url
- image_type
- uploaded_at

### 4. Departments

Stores information about departments responsible for infrastructure
maintenance.

Important fields:

- department_id
- department_name
- description

### 5. Assignments

Stores assignments of infrastructure issues to departments and field
staff.

Important fields:

- assignment_id
- issue_id
- staff_id
- department_id
- assigned_at
- completed_at

### 6. Status History

Stores the history of important status changes for each issue.

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

The relationships between these entities will be represented in the
Entity-Relationship diagram during the architecture and database
design phase.

---

## 7. User Roles & Permissions (minimum 2 distinct roles)

| Role | Permissions |
|------|-------------|
| Citizen | Register, login, create issues, upload images, provide location, view own reports, track issue status |
| Administrator | Login, view all issues, verify reports, set priority, assign issues, manage departments and field staff, monitor analytics |
| Field Staff | Login, view assigned issues, update status, add remarks, upload resolution evidence, mark issues as resolved |

The system will implement role-based access control so that each user
can access only the functions allowed for their assigned role.

---

## 8. Success Criteria

The project will be considered successful when the following
objectives are achieved:

1. A citizen can register and securely log in to the application.

2. A citizen can create an infrastructure issue report containing an
   issue category, description, photograph, and geographical location.

3. Submitted issues are stored correctly in the database and linked
   to the reporting citizen.

4. An administrator can view and verify submitted issues.

5. An administrator can assign an appropriate priority to verified
   issues.

6. An administrator can assign an issue to a department and field
   staff member.

7. Field staff can view their assigned issues and update their
   progress.

8. Field staff can upload evidence after completing maintenance work.

9. Citizens can track the status of their submitted issues.

10. The system maintains a history of important issue status changes.

11. Administrators can view basic statistics through a dashboard.

12. Reported issues can be displayed on an interactive map.

13. Role-based access prevents users from accessing unauthorized
    functions.

14. The application has a modular architecture separating frontend,
    backend, business logic, and database responsibilities.

15. The backend APIs are documented using Swagger / OpenAPI.

16. The application is testable using the selected testing framework.

17. The application can be deployed as a publicly accessible web
    application.

18. The later AI enhancement can assist with infrastructure issue
    detection, classification, and severity or priority estimation
    from uploaded images.

---

## 9. Out of Scope (clearly list what you will NOT build, to avoid over-commitment)

The following features are outside the scope of the initial 60-day
project:

- Direct integration with official government or municipal systems.
- Automated dispatch of police, ambulance, or fire services.
- Real-world financial or payment processing.
- Automated physical repair of infrastructure.
- Deployment and maintenance of large-scale physical IoT sensor
  networks.
- Nationwide infrastructure monitoring.
- Satellite-based infrastructure monitoring.
- Real-time integration with every existing traffic management
  system.
- Support for every possible type of public infrastructure in the
  initial version.
- Fully autonomous AI decision-making without human verification.

The AI component will be designed as a decision-support feature for
authorized administrators rather than a replacement for human
decision-making.

---

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