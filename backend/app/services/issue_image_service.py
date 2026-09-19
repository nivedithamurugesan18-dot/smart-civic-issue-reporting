from sqlalchemy.orm import Session

from app.repositories.issue_image_repository import (
    create_issue_image,
    get_issue_images,
    delete_issue_image
)


def create(
    db: Session,
    issue_id: int,
    image_url: str,
    file_name: str | None = None
):
    return create_issue_image(
        db,
        issue_id,
        image_url,
        file_name
    )


def get_for_issue(
    db: Session,
    issue_id: int
):
    return get_issue_images(
        db,
        issue_id
    )


def delete(
    db: Session,
    image_id: int
):
    return delete_issue_image(
        db,
        image_id
    )