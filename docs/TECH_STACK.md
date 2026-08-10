# Technology Stack Decision

## 1. Project Technology Strategy

The project will follow the Python technology track and will use
FastAPI as the backend framework.

The selected technologies are intended to support a modular,
maintainable, secure, testable, and deployable full-stack
application.

The technology stack is divided into frontend, backend, database,
authentication, mapping, testing, AI, version control, CI/CD, and
deployment layers.


## 2. Selected Technology Stack

| Layer | Technology | Purpose |
|------|------------|---------|
| Frontend | React.js | Build the user interface |
| Styling | Tailwind CSS | Create responsive and consistent UI |
| Backend | Python FastAPI | Build REST APIs and application business logic |
| ORM | SQLAlchemy | Interact with the relational database |
| Database | PostgreSQL | Store users, issues, assignments, images, status history, and notifications |
| Authentication | JWT | Secure user authentication and role-based access |
| Mapping | Leaflet | Display infrastructure issues on an interactive map |
| Map Data | OpenStreetMap | Provide map data for location visualization |
| API Testing | Thunder Client | Test REST APIs during development |
| Backend Testing | Pytest | Write and execute automated backend tests |
| API Documentation | Swagger / OpenAPI | Document and test REST API endpoints |
| AI | Python, YOLO, OpenCV | Detect and analyze infrastructure issues from images |
| Data Science | Pandas, NumPy, Scikit-learn | Data processing, analysis, and machine learning |
| Version Control | Git | Track source-code changes |
| Repository | GitHub | Store source code and project documentation |
| CI/CD | GitHub Actions | Automate testing and build validation |
| Deployment | Cloud Hosting | Make the application publicly accessible |


## 3. Frontend — React.js

### Selected Technology

React.js

### Reason for Selection

React.js will be used to develop the frontend of the application.

The system contains multiple user roles and dashboards, including
citizen, administrator, and field staff interfaces.

React's component-based architecture is suitable for building
reusable UI components and maintaining separate pages for different
functional modules.

### Planned Usage

React.js will be used for:

- Login and registration pages
- Citizen dashboard
- Issue reporting form
- Issue tracking page
- Administrator dashboard
- Field staff dashboard
- Issue details page
- Map interface
- Analytics interface


## 4. Styling — Tailwind CSS

### Selected Technology

Tailwind CSS

### Reason for Selection

Tailwind CSS will be used to create a responsive and consistent
interface.

It allows the application to maintain a common visual design across
citizen, administrator, and field staff interfaces.

### Planned Usage

- Responsive layouts
- Forms
- Dashboard cards
- Navigation
- Tables
- Status indicators
- Modal dialogs
- Mobile-friendly interfaces


## 5. Backend — Python FastAPI

### Selected Technology

FastAPI

### Reason for Selection

FastAPI will be used to develop the REST API and backend business
logic.

The project requires multiple modules including authentication,
issue reporting, issue management, assignment, status tracking,
notifications, and analytics.

FastAPI provides a suitable structure for building modular REST APIs
and also provides automatic OpenAPI/Swagger documentation.

### Planned Backend Modules

- Authentication
- Users
- Issues
- Issue Images
- Departments
- Assignments
- Status History
- Notifications
- Analytics


## 6. Database — PostgreSQL

### Selected Technology

PostgreSQL

### Reason for Selection

The project requires a relational database because several entities
are connected through relationships.

Examples include:

- Users and Issues
- Issues and Images
- Issues and Assignments
- Departments and Assignments
- Issues and Status History
- Users and Notifications

PostgreSQL is therefore selected as the primary database for the
application.


## 7. ORM — SQLAlchemy

### Selected Technology

SQLAlchemy

### Reason for Selection

SQLAlchemy will provide the database interaction layer between the
FastAPI backend and PostgreSQL.

It will allow database tables to be represented as application
models and will help maintain organized database operations.


## 8. Authentication and Authorization

### Selected Technology

JWT Authentication

### Reason for Selection

The application has multiple user roles with different permissions.

JWT-based authentication will be used to identify authenticated
users when they access protected API endpoints.

Role-based access control will be implemented for:

- Citizen
- Administrator
- Field Staff

The backend will verify the user's identity and role before allowing
access to protected operations.


## 9. Mapping — Leaflet and OpenStreetMap

### Selected Technologies

- Leaflet
- OpenStreetMap

### Reason for Selection

Location is an important part of public infrastructure issue
management.

Leaflet will be used to display issue locations through an
interactive map.

OpenStreetMap will provide the map data used for visualization.

### Planned Features

- Display issue markers
- Show issue locations
- View issue details from map markers
- Identify areas with multiple reports
- Support location-based monitoring


## 10. API Documentation — Swagger / OpenAPI

### Selected Technology

Swagger / OpenAPI

### Reason for Selection

The backend will contain multiple REST API endpoints.

Automatic API documentation will make it easier to understand,
test, and maintain the API during development.

FastAPI will provide the OpenAPI documentation for the available
endpoints.


## 11. API Testing — Thunder Client

### Selected Technology

Thunder Client

### Reason for Selection

Thunder Client will be used during development to test REST API
endpoints.

It will help verify:

- Request parameters
- Request bodies
- Authentication
- Response status codes
- API error handling
- CRUD operations


## 12. Automated Testing — Pytest

### Selected Technology

Pytest

### Reason for Selection

Pytest will be used to create automated tests for backend business
logic and services.

Tests will be created for important operations such as:

- User authentication
- Issue creation
- Issue validation
- Priority assignment
- Issue assignment
- Status updates
- Authorization


## 13. AI and Data Science Technologies

### Selected Technologies

- Python
- Pandas
- NumPy
- OpenCV
- YOLO / Computer Vision
- Scikit-learn

### Reason for Selection

The project has a natural opportunity for an AI enhancement based on
infrastructure images.

The planned AI component will analyze uploaded images and assist in
identifying infrastructure issues.

### Planned AI Workflow

Image
→ Preprocessing
→ Computer Vision Model
→ Issue Detection
→ Issue Classification
→ Severity Estimation
→ Priority Recommendation

The AI feature will be implemented during the later enhancement
phase rather than the initial MVP phase.


## 14. Data Science and Analytics

Pandas and NumPy will be used for data processing and analysis.

Scikit-learn may be used for machine learning tasks where
appropriate.

Possible analytical features include:

- Issue frequency analysis
- Issue category distribution
- Location-based analysis
- Resolution time analysis
- Priority trends
- Department performance
- Frequently affected locations


## 15. Version Control — Git and GitHub

### Selected Technologies

- Git
- GitHub

### Reason for Selection

Git will be used to track source-code changes throughout the
60-day development period.

GitHub will be used as the central repository for:

- Source code
- Documentation
- Project history
- Issues
- Pull requests
- CI/CD workflows

Meaningful commits will be maintained throughout the development
process according to the project requirements.


## 16. CI/CD — GitHub Actions

### Selected Technology

GitHub Actions

### Reason for Selection

GitHub Actions will be used to automate development checks.

The planned workflow is:

Code Push / Pull Request
        ↓
Install Dependencies
        ↓
Run Linting
        ↓
Run Automated Tests
        ↓
Build Validation


## 17. Deployment

The final application will be deployed using cloud hosting.

The planned deployment architecture is:

React Frontend
        ↓
Cloud Hosting

FastAPI Backend
        ↓
Cloud Hosting

PostgreSQL Database
        ↓
Cloud Database Service

The exact hosting providers will be finalized during the deployment
phase based on availability and project requirements.


## 18. Technology Selection Summary

The selected stack provides the required capabilities for the
project:

### Frontend

React.js + Tailwind CSS

### Backend

Python + FastAPI + SQLAlchemy

### Database

PostgreSQL

### Authentication

JWT + Role-Based Access Control

### Maps

Leaflet + OpenStreetMap

### Testing

Pytest + Thunder Client

### API Documentation

Swagger / OpenAPI

### AI

Python + OpenCV + YOLO

### Data Science

Pandas + NumPy + Scikit-learn

### Version Control

Git + GitHub

### CI/CD

GitHub Actions

### Deployment

Cloud Hosting


## 19. Final Technology Decision

The project will use the Python FastAPI technology track for the
complete capstone development period.

The selected stack provides a practical combination of modern
frontend development, REST API development, relational database
management, authentication, mapping, automated testing, CI/CD,
cloud deployment, and AI capabilities.

The technology choices are intended to keep the project achievable
within the capstone timeline while providing sufficient scope for
real-world functionality and AI/Data Science enhancement.