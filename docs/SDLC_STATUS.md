# SDLC Status and Evidence

This document distinguishes repository evidence from planned work. A phase is not marked complete merely because it appears in an earlier planning document.

| SDLC phase | Status | Evidence and boundary |
|---|---|---|
| Problem Statement | Completed | `Problem_Statement.md` defines the project title, domain, users, problem, proposed solution, roles, entities, success criteria, and scope boundaries. |
| Domain Study | Completed | `docs/DOMAIN_STUDY.md` documents the civic-technology context, target users, current problem, proposed domain workflow, data, limitations, and future opportunities. |
| Requirements | Partially Completed | Functional expectations are recorded in `Problem_Statement.md`, including success criteria and role permissions. There is no separate formal SRS or requirements-traceability matrix in the repository. |
| Tech Stack | Completed | `docs/TECH_STACK.md` records the selected React, FastAPI, PostgreSQL, SQLAlchemy, JWT, Leaflet/OpenStreetMap, Git/GitHub, and future-AI technologies. Some sections retain planning language and are not treated as execution evidence. |
| System Architecture | Completed | `docs/diagrams/SYSTEM_ARCHITECTURE.md` is the completed standalone architecture document. It records the implemented overview, layered architecture, authentication/RBAC, issue, map, image, notification, database, API, security, and runtime architecture, with a Mermaid diagram, data flow, constraints, and current scope. |
| ER Diagram / Database Design | Completed | `docs/diagrams/ER_DIAGRAM.svg` and `docs/diagrams/ER_DIAGRAM.drawio` are committed. The repository also contains SQLAlchemy models for users, issues, issue updates, images, departments, assignments, and notifications. |
| Development | Completed | The committed `backend/app/` and `frontend/src/` trees implement authentication, issue reporting, mapping, evidence images, assignment, status/progress, notifications, and role-specific dashboards. The completed runtime verification passed for the implemented application areas. |
| Testing | Completed | `docs/TESTING.md` records the verified runtime, API, frontend, build, dependency, security, and database checks. It explicitly identifies results that were not recorded as standalone tests. No new test run is claimed for the documentation pass. |
| CI/CD | CI Validation Workflow Added | `.github/workflows/ci.yml` validates backend syntax/configuration imports and frontend lint/production build on pushes to `main` and pull requests targeting `main`. A successful GitHub Actions execution has not yet been verified. |
| Deployment | Not Yet Completed | The repository and verification work target local PostgreSQL, local FastAPI, and local Vite execution. No public or cloud deployment was performed or claimed. |
| Enhancement | Not Yet Completed | AI/computer-vision issue detection, severity estimation, and priority recommendation are documented as future ideas in the existing planning documents. No AI implementation is included in the current feature summary. |

## Current documentation evidence set

- [Problem Statement](../Problem_Statement.md)
- [Domain Study](./DOMAIN_STUDY.md)
- [Technology Stack](./TECH_STACK.md)
- [Testing](./TESTING.md)
- [Validation Summary](./VALIDATION_SUMMARY.md)
- [System Workflow](./SYSTEM_WORKFLOW.md)
- [ER Diagram](./diagrams/ER_DIAGRAM.svg)
- [Final Demo Checklist](./DEMO_CHECKLIST.md)

## Missing or incomplete college evidence

1. A separate requirements specification and traceability matrix are not present.
2. The GitHub Actions workflow is committed, but a successful CI/CD run has not yet been verified in GitHub.
3. No deployment URL or public/cloud deployment evidence is present.
4. The AI enhancement remains planned rather than implemented.
