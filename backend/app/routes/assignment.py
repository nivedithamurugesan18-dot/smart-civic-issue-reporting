from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.issue import Issue
from app.schemas.assignment import (
    AssignmentCreate,
    AssignmentResponse
)
from app.services.assignment_service import (
    create,
    get_for_issue,
    get_by_id
)
from app.routes.issue import get_current_user


router = APIRouter(
    prefix="/assignments",
    tags=["Assignments"]
)


@router.post(
    "/",
    response_model=AssignmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_assignment_route(
    assignment: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["admin", "authority"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin or authority users can assign issues"
        )

    issue = (
        db.query(Issue)
        .filter(Issue.id == assignment.issue_id)
        .first()
    )

    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )

    assigned_user = (
        db.query(User)
        .filter(User.id == assignment.assigned_to)
        .first()
    )

    if not assigned_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assigned user not found"
        )

    if assigned_user.role not in ["authority", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Issue can only be assigned to an authority or admin user"
        )

    result = create(
        db,
        assignment.issue_id,
        assignment.assigned_to,
        current_user.id
    )

    issue.assigned_to = assignment.assigned_to

    if issue.status == "reported":
        issue.status = "assigned"

    db.commit()
    db.refresh(result)

    return result


@router.get(
    "/issue/{issue_id}",
    response_model=list[AssignmentResponse]
)
def get_issue_assignments_route(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    issue = (
        db.query(Issue)
        .filter(Issue.id == issue_id)
        .first()
    )

    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )

    return get_for_issue(
        db,
        issue_id
    )


@router.get(
    "/{assignment_id}",
    response_model=AssignmentResponse
)
def get_assignment_route(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assignment = get_by_id(
        db,
        assignment_id
    )

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )

    return assignment