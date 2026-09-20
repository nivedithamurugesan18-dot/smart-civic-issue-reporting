# SDLC Status and Evidence

This document distinguishes repository evidence from planned work. A phase is not marked complete merely because it appears in an earlier planning document.

| SDLC phase | Status | Evidence and boundary |
|---|---|---|
| Problem Statement | Completed | `Problem_Statement.md` defines the project title, domain, users, problem, proposed solution, roles, entities, success criteria, and scope boundaries. |
| Domain Study | Completed | `docs/DOMAIN_STUDY.md` documents the civic-technology context, target users, current problem, proposed domain workflow, data, limitations, and future opportunities. |
| Requirements | Completed | `docs/REQUIREMENTS_SPECIFICATION.md` provides the formal requirements baseline, including functional and non-functional requirements, business rules, data/interface/security requirements, and a requirements traceability matrix mapped to implementation evidence and recorded verification IDs. |
| Tech Stack | Completed | `docs/TECH_STACK.md` records the selected React, FastAPI, PostgreSQL, SQLAlchemy, JWT, Leaflet/OpenStreetMap, Git/GitHub, and future-AI technologies. Some sections retain planning language and are not treated as execution evidence. |
| System Architecture | Completed | `docs/diagrams/SYSTEM_ARCHITECTURE.md` is the completed standalone architecture document. It records the implemented overview, layered architecture, authentication/RBAC, issue, map, image, notification, database, API, security, and runtime architecture, with a Mermaid diagram, data flow, constraints, and current scope. |
| ER Diagram / Database Design | Completed | `docs/diagrams/ER_DIAGRAM.svg` and `docs/diagrams/ER_DIAGRAM.drawio` are committed. The repository also contains SQLAlchemy models for users, issues, issue updates, images, departments, assignments, and notifications. |
| Development | Completed | The committed `backend/app/` and `frontend/src/` trees implement authentication, issue reporting, mapping, evidence images, assignment, status/progress, notifications, and role-specific dashboards. The completed runtime verification passed for the implemented application areas. |
| Database Migration System | Completed | Alembic `1.16.4` is configured with baseline revision `1b1e22234583`. The existing `smart_civic` database was adopted by stamping that baseline after read-only comparison and backup. FastAPI startup no longer executes `create_all()`; future migration execution is an explicit deployment step. |
| Migration Workflow Documentation | Completed | `docs/ALEMBIC_WORKFLOW.md` documents explicit targeting, autogeneration review, disposable-database testing, rollback cautions, baseline preservation, CI boundaries, and the approved `issues_reported_by_fkey` warning. |
| Testing | Completed | `docs/TESTING.md` records the verified runtime, API, frontend, build, dependency, security, and database checks. It explicitly identifies results that were not recorded as standalone tests. No new application test suite run is claimed for the documentation pass. |
| CI/CD | CI/CD Validation Configured | `.github/workflows/ci.yml` contains backend, Alembic static, and frontend validation. An earlier GitHub Actions run for commit `699c80f` passed the then-existing backend and frontend checks; the newly added Alembic checks have passed locally, while GitHub execution of the current uncommitted workflow remains pending. This does not constitute public or cloud deployment. |
| Deployment | Not Yet Completed | The repository and verification work target local PostgreSQL, local FastAPI, and local Vite execution. No public or cloud deployment was performed or claimed. |
| Enhancement | Not Yet Completed | AI/computer-vision issue detection, severity estimation, and priority recommendation are documented as future ideas in the existing planning documents. No AI implementation is included in the current feature summary. |

## Current documentation evidence set

- [Problem Statement](../Problem_Statement.md)
- [Requirements Specification](./REQUIREMENTS_SPECIFICATION.md)
- [Domain Study](./DOMAIN_STUDY.md)
- [Technology Stack](./TECH_STACK.md)
- [Testing](./TESTING.md)
- [Alembic Workflow](./ALEMBIC_WORKFLOW.md)
- [Validation Summary](./VALIDATION_SUMMARY.md)
- [System Workflow](./SYSTEM_WORKFLOW.md)
- [ER Diagram](./diagrams/ER_DIAGRAM.svg)
- [Final Demo Checklist](./DEMO_CHECKLIST.md)

## Missing or incomplete college evidence

1. No deployment URL or public/cloud deployment evidence is present.
2. The AI enhancement remains planned rather than implemented.
