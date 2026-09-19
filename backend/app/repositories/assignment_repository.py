from sqlalchemy.orm import Session

from app.models.assignment import Assignment


def create_assignment(
    db: Session,
    issue_id: int,
    assigned_to: int,
    assigned_by: int
):
    assignment = Assignment(
        issue_id=issue_id,
        assigned_to=assigned_to,
        assigned_by=assigned_by,
        status="assigned"
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment


def get_issue_assignments(
    db: Session,
    issue_id: int
):
    return (
        db.query(Assignment)
        .filter(Assignment.issue_id == issue_id)
        .order_by(Assignment.id.desc())
        .all()
    )


def get_assignment(
    db: Session,
    assignment_id: int
):
    return (
        db.query(Assignment)
        .filter(Assignment.id == assignment_id)
        .first()
    )