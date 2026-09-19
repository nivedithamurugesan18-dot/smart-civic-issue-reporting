import logging

from sqlalchemy.orm import Session

from app.repositories.notification_repository import (
    create_notification,
    get_unread_notification_count,
    get_user_notifications,
    mark_notification_read
)


logger = logging.getLogger(__name__)


def create(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    notification_type: str = "general",
    issue_id: int | None = None
):
    return create_notification(
        db,
        user_id,
        title,
        message,
        notification_type,
        issue_id
    )


def create_safe(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    notification_type: str = "general",
    issue_id: int | None = None
):
    """Create a notification without failing the primary operation."""
    try:
        return create(
            db,
            user_id,
            title,
            message,
            notification_type,
            issue_id
        )
    except Exception:
        db.rollback()
        logger.exception(
            "Notification creation failed for user %s.",
            user_id
        )
        return None


def get_for_user(
    db: Session,
    user_id: int
):
    return get_user_notifications(
        db,
        user_id
    )


def get_unread_count(
    db: Session,
    user_id: int
):
    return get_unread_notification_count(
        db,
        user_id
    )


def mark_read(
    db: Session,
    notification_id: int,
    user_id: int
):
    return mark_notification_read(
        db,
        notification_id,
        user_id
    )
