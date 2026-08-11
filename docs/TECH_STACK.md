# Technology Stack Decision

## 1. Project

**Project Name:** Smart Public Infrastructure Issue Reporting and Prioritization System

**Chosen Track:** Python (FastAPI)

---

## 2. Technology Stack Overview

The project will use a modern web application architecture with a React frontend, FastAPI backend, and PostgreSQL database.

The selected technologies are:

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | React.js | Build the web user interface |
| Styling | Tailwind CSS | Create responsive and modern UI |
| Frontend Routing | React Router | Manage application pages and navigation |
| HTTP Client | Axios | Communicate with backend APIs |
| Backend | Python + FastAPI | Build REST APIs and backend services |
| ORM | SQLAlchemy | Connect application logic with database tables |
| Database | PostgreSQL | Store users, issues, assignments, status history and other project data |
| Authentication | JWT | Secure user login and API access |
| Password Security | Password Hashing | Protect user passwords |
| Authorization | Role-Based Access Control | Control access based on user role |
| Maps | Leaflet + OpenStreetMap | Display infrastructure issues on an interactive map |
| Testing | Pytest | Test backend business logic and APIs |
| API Documentation | FastAPI Swagger / OpenAPI | Document and test REST APIs |
| Version Control | Git + GitHub | Track source code and project changes |
| CI/CD | GitHub Actions | Automate testing and build processes |
| AI Enhancement | Python, Pandas, NumPy, OpenCV, YOLO, Scikit-learn | Future AI-based issue detection and priority estimation |

---

## 3. Frontend

### React.js

React.js will be used to build the frontend of the application.

It will provide interfaces for:

- Citizen registration and login
- Reporting infrastructure issues
- Viewing submitted issues
- Tracking issue status
- Administrator dashboard
- Issue verification and prioritization
- Field staff issue management
- Interactive issue map

### Tailwind CSS

Tailwind CSS will be used for responsive styling and user interface design.

The interface should work on:

- Desktop
- Laptop
- Tablet
- Mobile screens

### React Router

React Router will manage navigation between application pages.

### Axios

Axios will be used to send HTTP requests from the React frontend to the FastAPI backend.

---

## 4. Backend

### Python

Python will be used as the main backend programming language.

### FastAPI

FastAPI will be used to develop REST APIs.

The backend will handle:

- User registration
- User login
- Authentication
- Authorization
- Issue reporting
- Issue verification
- Issue prioritization
- Issue assignment
- Status updates
- Issue history
- Dashboard data
- Map-related issue data

The APIs will be organized under:

`/api/`

API versioning such as `/api/v1/` may be used as the project develops.

---

## 5. Database

### PostgreSQL

PostgreSQL will be used as the main relational database.

The database will store structured project information such as:

- Users
- Roles
- Infrastructure issues
- Issue categories
- Issue assignments
- Issue status history
- Locations
- Notifications

The database design will maintain proper relationships between entities.

---

## 6. ORM

### SQLAlchemy

SQLAlchemy will be used as the Object Relational Mapper.

It will allow the FastAPI backend to work with PostgreSQL using Python models and database queries.

Business logic will be separated from database access logic.

---

## 7. Authentication and Security

The application will use JWT-based authentication.

Security mechanisms include:

- JWT authentication
- Password hashing
- Role-based access control
- Environment variables for sensitive configuration
- Protected API endpoints

The main user roles are:

1. Citizen
2. Administrator
3. Field Staff

Each role will receive access only to the functions required for its responsibilities.

---

## 8. Maps and Location

### Leaflet

Leaflet will be used to create interactive maps.

### OpenStreetMap

OpenStreetMap will provide the map data.

The map feature will allow reported infrastructure issues to be displayed according to their geographical location.

---

## 9. Testing

### Pytest

Pytest will be used for backend unit testing.

Testing will cover important business logic such as:

- User operations
- Issue creation
- Issue verification
- Issue prioritization
- Issue assignment
- Status changes
- Permission checks

---

## 10. API Documentation

FastAPI's built-in Swagger/OpenAPI documentation will be used.

The API documentation will help developers understand:

- API endpoints
- HTTP methods
- Request data
- Response data
- Authentication requirements

The documentation will be available through FastAPI's documentation interface.

---

## 11. Version Control

Git and GitHub will be used for source-code management.

The project will follow a feature-branch workflow.

The `main` branch will contain stable project code.

New work will be developed using feature branches and merged through Pull Requests.

Example:

`feature/domain-study`

`feature/tech-stack`

`feature/database-schema`

---

## 12. CI/CD

GitHub Actions will be used for continuous integration and continuous delivery.

The pipeline will later be configured to:

1. Checkout the repository
2. Install dependencies
3. Run linting or basic checks
4. Run automated tests
5. Report failed tests
6. Support deployment after successful checks

---

## 13. Future AI Enhancement

The project has scope for a later AI enhancement.

The planned technologies include:

- Python
- Pandas
- NumPy
- OpenCV
- YOLO / Computer Vision
- Scikit-learn where required

The AI feature may assist administrators by detecting infrastructure problems from uploaded images and estimating issue severity or priority.

The AI system will act as a decision-support tool and will not replace human verification.

---

## 14. Deployment Plan

The planned deployment architecture is:

- React frontend → Cloud hosting platform
- FastAPI backend → Cloud hosting platform
- PostgreSQL → Cloud database service

The college-provided technology stack allows platforms such as Render or Railway for backend hosting and Vercel or Netlify for frontend hosting.

---

## 15. Reason for Choosing This Stack

The Python FastAPI track was selected because it is suitable for building a modular REST API and provides automatic API documentation.

React provides a flexible frontend for the citizen, administrator and field staff interfaces.

PostgreSQL provides a reliable relational database for managing the project's connected entities.

SQLAlchemy provides structured database access from Python.

The selected stack also provides a suitable foundation for the planned AI enhancement.

---

## 16. Technology Decision Summary

| Requirement | Selected Technology |
|---|---|
| Programming Language | Python |
| Frontend | React.js |
| CSS Framework | Tailwind CSS |
| Backend | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | JWT |
| Authorization | Role-Based Access Control |
| Maps | Leaflet + OpenStreetMap |
| Testing | Pytest |
| API Documentation | FastAPI Swagger / OpenAPI |
| Version Control | Git + GitHub |
| CI/CD | GitHub Actions |
| Future AI | OpenCV, YOLO, Scikit-learn |

---

## Conclusion

The selected technology stack provides the required foundation for developing the Smart Public Infrastructure Issue Reporting and Prioritization System.

The architecture will separate the frontend, backend, database and external services so that the application can be developed, tested and deployed in a modular manner.