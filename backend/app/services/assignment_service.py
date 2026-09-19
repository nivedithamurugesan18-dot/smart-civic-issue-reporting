from sqlalchemy.orm import Session

from app.repositories.assignment_repository import (
    create_assignment,
    get_issue_assignments,
    get_assignment
)


def create(
    db: Session,
    issue_id: int,
    assigned_to: int,
    assigned_by: int
):
    return create_assignment(
        db,
        issue_id,
        assigned_to,
        assigned_by
    )


def get_for_issue(
    db: Session,
    issue_id: int
):
    return get_issue_assignments(
        db,
        issue_id
    )


def get_by_id(
    db: Session,
    assignment_id: int
):
    return get_assignment(
        db,
        assignment_id
    )