import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.issue import Issue
from app.models.user import User
from app.models.issue_update import IssueUpdate

from app.schemas.issue import IssueCreate, IssueResponse
from app.schemas.issue_update import (
    IssueUpdateCreate,
    IssueUpdateResponse
)

from app.dependencies import get_current_user, require_role
from app.services.notification_service import create_safe as create_notification_safe


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/issues",
    tags=["Issues"]
)

logger = logging.getLogger(__name__)


# ============================================================
# STATUS REQUEST SCHEMA
# ============================================================

class IssueStatusUpdate(BaseModel):
    status: str


# ============================================================
# UPDATE ISSUE DETAILS SCHEMA
# ============================================================

class IssueDetailsUpdate(BaseModel):
    title: str
    description: str
    category: str
    priority: str
    severity: str
    location: str


# ============================================================
# ISSUE ASSIGNMENT SCHEMA
# ============================================================

class IssueAssignment(BaseModel):
    assigned_to: int


# ============================================================
# CREATE ISSUE
# ============================================================

@router.post(
    "/",
    response_model=IssueResponse,
    status_code=status.HTTP_201_CREATED
)
def create_issue(
    issue: IssueCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("citizen"))
):
    """
    Create a new public infrastructure issue.

    Only citizens can report new issues.
    """

    new_issue = Issue(
        title=issue.title,
        description=issue.description,
        category=issue.category,
        priority=issue.priority,
        severity=issue.severity,
        location=issue.location,
        latitude=issue.latitude,
        longitude=issue.longitude,
        reported_by=current_user.id
    )

    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)

    try:
        admin_users = (
            db.query(User)
            .filter(User.role == "admin")
            .all()
        )
    except Exception:
        db.rollback()
        logger.exception(
            "Admin notification recipient lookup failed for issue %s.",
            new_issue.id
        )
        admin_users = []

    for admin_user in admin_users:
        create_notification_safe(
            db,
            admin_user.id,
            "New civic issue reported",
            f"Issue #{new_issue.id} has been reported: {new_issue.title}",
            "issue_created",
            new_issue.id
        )

    return new_issue


# ============================================================
# GET MY ISSUES
# ============================================================

@router.get(
    "/my",
    response_model=list[IssueResponse]
)
def get_my_issues(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("citizen"))
):
    """
    Get all issues reported by the currently
    authenticated citizen.
    """

    issues = (
        db.query(Issue)
        .filter(
            Issue.reported_by == current_user.id
        )
        .order_by(Issue.id.desc())
        .all()
    )

    return issues


# ============================================================
# GET ALL ISSUES
# ============================================================

@router.get(
    "/",
    response_model=list[IssueResponse]
)
def get_all_issues(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin", "authority")
    )
):
    """
    Get all reported civic issues.

    Administrators and authority users can
    view all reported issues.
    """

    issues = (
        db.query(Issue)
        .order_by(Issue.id.desc())
        .all()
    )

    return issues


# ============================================================
# GET ASSIGNED ISSUES
# ============================================================

@router.get(
    "/assigned",
    response_model=list[IssueResponse]
)
def get_assigned_issues(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("field_staff")
    )
):
    """
    Get all issues assigned to the currently
    authenticated field staff member.

    Only field staff can access this endpoint.
    """

    issues = (
        db.query(Issue)
        .filter(
            Issue.assigned_to == current_user.id
        )
        .order_by(Issue.id.desc())
        .all()
    )

    return issues


# ============================================================
# GET SINGLE ISSUE
# ============================================================

@router.get(
    "/{issue_id}",
    response_model=IssueResponse
)
def get_issue(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a single issue.

    Any authenticated user can access an issue by ID.
    """

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

    return issue


# ============================================================
# UPDATE ISSUE STATUS
# ============================================================

@router.patch(
    "/{issue_id}/status",
    response_model=IssueResponse
)
def update_issue_status(
    issue_id: int,
    status_data: IssueStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin", "field_staff")
    )
):
    """
    Update the status of an issue.

    Admin and field staff users can update issue status.

    Every status change is recorded
    in the issue_updates table.
    """

    # --------------------------------------------------------
    # VALIDATE STATUS
    # --------------------------------------------------------

    allowed_statuses = [
        "reported",
        "assigned",
        "in_progress",
        "resolved",
        "closed"
    ]

    new_status = (
        status_data.status
        .lower()
        .strip()
    )

    if new_status not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Invalid issue status",
                "allowed_statuses": allowed_statuses
            }
        )

    # --------------------------------------------------------
    # FIND ISSUE
    # --------------------------------------------------------

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

    if (
        current_user.role == "field_staff"
        and issue.assigned_to != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update issues assigned to you."
        )

    # --------------------------------------------------------
    # CHECK IF STATUS ACTUALLY CHANGED
    # --------------------------------------------------------

    old_status = issue.status

    if old_status == new_status:
        return issue

    # --------------------------------------------------------
    # UPDATE MAIN ISSUE STATUS
    # --------------------------------------------------------

    issue.status = new_status

    # --------------------------------------------------------
    # CREATE STATUS HISTORY UPDATE
    # --------------------------------------------------------

    status_update = IssueUpdate(
        issue_id=issue_id,
        updated_by=current_user.id,
        message=(
            f"Issue status changed from "
            f"'{old_status}' to '{new_status}'."
        ),
        status=new_status
    )

    db.add(status_update)

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    db.commit()
    db.refresh(issue)

    create_notification_safe(
        db,
        issue.reported_by,
        "Issue status updated",
        f"Issue #{issue.id} status changed to {new_status.replace('_', ' ').title()}.",
        "status_changed",
        issue.id
    )

    return issue


# ============================================================
# UPDATE ISSUE DETAILS
# ============================================================

@router.put(
    "/{issue_id}",
    response_model=IssueResponse
)
def update_issue(
    issue_id: int,
    issue_data: IssueDetailsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update the details of an existing issue.

    Citizens can update their own issues.
    Admin can update any issue.
    Field staff can update only assigned issues.
    """

    # --------------------------------------------------------
    # FIND ISSUE
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # CHECK PERMISSION
    # --------------------------------------------------------

    if (
        current_user.role == "field_staff"
        and issue.assigned_to != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update issues assigned to you."
        )

    if (
        current_user.role not in ["admin", "field_staff"]
        and issue.reported_by != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own issues"
        )

    # --------------------------------------------------------
    # UPDATE DETAILS
    # --------------------------------------------------------

    issue.title = issue_data.title
    issue.description = issue_data.description
    issue.category = issue_data.category
    issue.priority = issue_data.priority
    issue.severity = issue_data.severity
    issue.location = issue_data.location

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    db.commit()
    db.refresh(issue)

    return issue


# ============================================================
# DELETE ISSUE
# ============================================================

@router.delete(
    "/{issue_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_issue(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete an issue.

    The issue owner or an admin can delete the issue.
    """

    # --------------------------------------------------------
    # FIND ISSUE
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # CHECK PERMISSION
    # --------------------------------------------------------

    if (
        issue.reported_by != current_user.id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this issue"
        )

    # --------------------------------------------------------
    # DELETE ISSUE
    # --------------------------------------------------------

    db.delete(issue)
    db.commit()

    return None


# ============================================================
# ASSIGN ISSUE
# ============================================================

@router.patch(
    "/{issue_id}/assign",
    response_model=IssueResponse
)
def assign_issue(
    issue_id: int,
    assignment_data: IssueAssignment,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    """
    Assign an issue to a field staff member.

    Only administrators can assign issues.
    """

    # --------------------------------------------------------
    # FIND ISSUE
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # FIND ASSIGNED USER
    # --------------------------------------------------------

    assigned_user = (
        db.query(User)
        .filter(User.id == assignment_data.assigned_to)
        .first()
    )

    if not assigned_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assigned user not found"
        )

    # --------------------------------------------------------
    # CHECK ASSIGNED USER ROLE
    # --------------------------------------------------------

    if assigned_user.role != "field_staff":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Issue can only be assigned to a field staff user"
        )

    # --------------------------------------------------------
    # ASSIGN ISSUE
    # --------------------------------------------------------

    assignment_changed = issue.assigned_to != assigned_user.id
    issue.assigned_to = assigned_user.id

    # Automatically change reported → assigned
    if issue.status == "reported":
        issue.status = "assigned"

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    db.commit()
    db.refresh(issue)

    if assignment_changed:
        create_notification_safe(
            db,
            assigned_user.id,
            "Issue assigned to you",
            f"Issue #{issue.id} has been assigned to you: {issue.title}",
            "issue_assigned",
            issue.id
        )

    return issue


# ============================================================
# ADD ISSUE UPDATE
# ============================================================

@router.post(
    "/{issue_id}/updates",
    response_model=IssueUpdateResponse,
    status_code=status.HTTP_201_CREATED
)
def create_issue_update(
    issue_id: int,
    update_data: IssueUpdateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin", "field_staff")
    )
):
    """
    Add a progress update to an existing civic issue.

    Admin and field staff can add progress updates.
    """

    # --------------------------------------------------------
    # FIND ISSUE
    # --------------------------------------------------------

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

    if (
        current_user.role == "field_staff"
        and issue.assigned_to != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update issues assigned to you."
        )

    # --------------------------------------------------------
    # VALIDATE STATUS
    # --------------------------------------------------------

    allowed_statuses = [
        "reported",
        "assigned",
        "in_progress",
        "resolved",
        "closed"
    ]

    new_status = None

    if update_data.status:
        new_status = (
            update_data.status
            .lower()
            .strip()
        )

        if new_status not in allowed_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Invalid issue status",
                    "allowed_statuses": allowed_statuses
                }
            )

    # --------------------------------------------------------
    # CREATE ISSUE UPDATE
    # --------------------------------------------------------

    new_update = IssueUpdate(
        issue_id=issue_id,
        updated_by=current_user.id,
        message=update_data.message,
        status=new_status
    )

    db.add(new_update)

    # --------------------------------------------------------
    # UPDATE MAIN ISSUE STATUS
    # --------------------------------------------------------

    if new_status:
        issue.status = new_status

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    db.commit()

    db.refresh(new_update)
    db.refresh(issue)

    create_notification_safe(
        db,
        issue.reported_by,
        "New issue progress update",
        f"New progress update added to issue #{issue.id}.",
        "progress_update",
        issue.id
    )

    return new_update


# ============================================================
# GET ISSUE UPDATES
# ============================================================

@router.get(
    "/{issue_id}/updates",
    response_model=list[IssueUpdateResponse]
)
def get_issue_updates(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all progress updates for a specific issue.
    """

    # --------------------------------------------------------
    # FIND ISSUE
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # GET UPDATES
    # --------------------------------------------------------

    updates = (
        db.query(IssueUpdate)
        .filter(IssueUpdate.issue_id == issue_id)
        .order_by(IssueUpdate.id.asc())
        .all()
    )

    return updates
