from sqlalchemy.orm import Session

from app.models.issue_image import IssueImage


def create_issue_image(
    db: Session,
    issue_id: int,
    image_url: str,
    file_name: str | None = None
):
    image = IssueImage(
        issue_id=issue_id,
        image_url=image_url,
        file_name=file_name
    )

    db.add(image)
    db.commit()
    db.refresh(image)

    return image


def get_issue_images(
    db: Session,
    issue_id: int
):
    return (
        db.query(IssueImage)
        .filter(IssueImage.issue_id == issue_id)
        .order_by(IssueImage.id.asc())
        .all()
    )


def delete_issue_image(
    db: Session,
    image_id: int
):
    image = (
        db.query(IssueImage)
        .filter(IssueImage.id == image_id)
        .first()
    )

    if image:
        db.delete(image)
        db.commit()

    return image