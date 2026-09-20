# SDLC Status and Evidence

This document distinguishes repository evidence from planned work. A phase is not marked complete merely because it appears in an earlier planning document.

| SDLC phase | Status | Evidence and boundary |
|---|---|---|
| Problem Statement | Completed | `Problem_Statement.md` defines the project title, domain, users, problem, proposed solution, roles, entities, success criteria, and scope boundaries. |
| Domain Study | Completed | `docs/DOMAIN_STUDY.md` documents the civic-technology context, target users, current problem, proposed domain workflow, data, limitations, and future opportunities. |
| Requirements | Partially Completed | Functional expectations are recorded in `Problem_Statement.md`, including success criteria and role permissions. There is no separate formal SRS or requirements-traceability matrix in the repository. |
| Tech Stack | Completed | `docs/TECH_STACK.md` records the selected React, FastAPI, PostgreSQL, SQLAlchemy, JWT, Leaflet/OpenStreetMap, Git/GitHub, and future-AI technologies. Some sections retain planning language and are not treated as execution evidence. |
| System Architecture | Partially Completed | The README describes `Frontend → REST API → FastAPI Backend → PostgreSQL Database`, and `docs/SYSTEM_WORKFLOW.md` documents the implemented flow. `docs/diagrams/SYSTEM_ARCHITECTURE.md` exists but is empty, so a complete standalone architecture document is not claimed. |
| ER Diagram / Database Design | Completed | `docs/diagrams/ER_DIAGRAM.svg` and `docs/diagrams/ER_DIAGRAM.drawio` are committed. The repository also contains SQLAlchemy models for users, issues, issue updates, images, departments, assignments, and notifications. |
| Development | Completed | The committed `backend/app/` and `frontend/src/` trees implement authentication, issue reporting, mapping, evidence images, assignment, status/progress, notifications, and role-specific dashboards. The completed runtime verification passed for the implemented application areas. |
| Testing | Completed | `docs/TESTING.md` records the verified runtime, API, frontend, build, dependency, security, and database checks. It explicitly identifies results that were not recorded as standalone tests. No new test run is claimed for the documentation pass. |
| CI/CD | Not Yet Completed | `docs/TECH_STACK.md` describes GitHub Actions as a planned pipeline, but no committed workflow file or completed CI/CD execution evidence was found. |
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

1. A standalone, non-empty system architecture document is still missing; the current workflow document supplies a textual architecture description.
2. A separate requirements specification and traceability matrix are not present.
3. No committed GitHub Actions workflow or CI/CD run evidence is present.
4. No deployment URL or production deployment evidence is present.
5. The AI enhancement remains planned rather than implemented.
