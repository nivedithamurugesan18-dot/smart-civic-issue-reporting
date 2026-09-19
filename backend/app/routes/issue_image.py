import logging
from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.issue import Issue
from app.models.issue_image import IssueImage
from app.models.user import User
from app.schemas.issue_image import IssueImageResponse
from app.services.issue_image_service import create, get_for_issue


logger = logging.getLogger(__name__)

router = APIRouter(tags=["Issue Images"])

ISSUE_UPLOAD_DIR = (
    Path(__file__).resolve().parents[2]
    / "uploads"
    / "issues"
)
ISSUE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_IMAGE_SIZE = 5 * 1024 * 1024
ALLOWED_CONTENT_TYPES = {
    "image/jpeg": (".jpg", ".jpeg"),
    "image/png": (".png",),
    "image/webp": (".webp",),
}


def _is_authorized_for_issue(
    issue: Issue,
    current_user: User
) -> bool:
    if current_user.role == "admin":
        return True

    if current_user.role == "citizen":
        return issue.reported_by == current_user.id

    if current_user.role == "field_staff":
        return issue.assigned_to == current_user.id

    return False


def _get_issue_or_404(
    issue_id: int,
    db: Session
) -> Issue:
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


def _validate_image(
    contents: bytes,
    content_type: str | None,
    original_filename: str | None
) -> str:
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Unsupported image type. Only JPEG, PNG, "
                "and WEBP images are allowed."
            )
        )

    if len(contents) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Image file must not exceed 5 MB"
        )

    extension = Path(original_filename or "").suffix.lower()
    allowed_extensions = ALLOWED_CONTENT_TYPES[content_type]

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The image filename extension does not match its content type"
        )

    if content_type == "image/jpeg":
        is_valid_format = (
            len(contents) >= 3
            and contents[:3] == b"\xff\xd8\xff"
        )
    elif content_type == "image/png":
        is_valid_format = (
            len(contents) >= 24
            and contents[:8] == b"\x89PNG\r\n\x1a\n"
            and contents[12:16] == b"IHDR"
        )
    else:
        is_valid_format = (
            len(contents) >= 12
            and contents[:4] == b"RIFF"
            and contents[8:12] == b"WEBP"
        )

    if not is_valid_format:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is not a valid image"
        )

    return extension


def _stored_file_path(image_url: str) -> Path | None:
    prefix = "/uploads/issues/"

    if not image_url.startswith(prefix):
        return None

    stored_name = image_url[len(prefix):]
    if not stored_name or Path(stored_name).name != stored_name:
        return None

    upload_root = ISSUE_UPLOAD_DIR.resolve()
    candidate = (upload_root / stored_name).resolve()

    try:
        candidate.relative_to(upload_root)
    except ValueError:
        return None

    return candidate


def _remove_stored_file(image_id: int, image_url: str) -> None:
    file_path = _stored_file_path(image_url)

    if file_path is None:
        return

    try:
        file_path.unlink(missing_ok=True)
    except OSError:
        logger.warning(
            "Could not remove the stored file for issue image %s.",
            image_id
        )


@router.post(
    "/issues/{issue_id}/images",
    response_model=IssueImageResponse,
    status_code=status.HTTP_201_CREATED
)
async def upload_issue_image(
    issue_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload one evidence image to an issue."""

    issue = _get_issue_or_404(issue_id, db)

    if not _is_authorized_for_issue(issue, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to upload images to this issue"
        )

    try:
        contents = await file.read(MAX_IMAGE_SIZE + 1)
    finally:
        await file.close()

    extension = _validate_image(
        contents,
        file.content_type,
        file.filename
    )

    generated_filename = f"{uuid4().hex}{extension}"
    file_path = ISSUE_UPLOAD_DIR / generated_filename
    image_url = f"/uploads/issues/{generated_filename}"

    try:
        file_path.write_bytes(contents)
        image = create(
            db,
            issue_id,
            image_url,
            generated_filename
        )
    except Exception:
        db.rollback()
        try:
            file_path.unlink(missing_ok=True)
        except OSError:
            logger.warning(
                "Could not clean up a failed upload for issue %s.",
                issue_id
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to store the issue image"
        )

    return image


@router.get(
    "/issues/{issue_id}/images",
    response_model=list[IssueImageResponse]
)
def get_issue_images(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List evidence images belonging only to the requested issue."""

    _get_issue_or_404(issue_id, db)
    return get_for_issue(db, issue_id)


@router.delete(
    "/issues/{issue_id}/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_issue_image(
    issue_id: int,
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an evidence image after validating issue ownership/assignment."""

    issue = _get_issue_or_404(issue_id, db)

    image = (
        db.query(IssueImage)
        .filter(
            IssueImage.id == image_id,
            IssueImage.issue_id == issue_id
        )
        .first()
    )

    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue image not found"
        )

    if not _is_authorized_for_issue(issue, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete images from this issue"
        )

    image_url = image.image_url
    db.delete(image)
    db.commit()

    _remove_stored_file(image_id, image_url)
    return None


# The original URL-based mutating endpoints are retained only as explicit
# deprecations. New application code must use the issue-specific file workflow.
@router.post(
    "/issue-images/",
    status_code=status.HTTP_410_GONE
)
def deprecated_create_issue_image():
    raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail=(
            "URL-based image creation is deprecated; upload a file via "
            "POST /issues/{issue_id}/images"
        )
    )


@router.get(
    "/issue-images/issue/{issue_id}",
    response_model=list[IssueImageResponse]
)
def legacy_get_issue_images(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    _get_issue_or_404(issue_id, db)
    return get_for_issue(db, issue_id)


@router.delete(
    "/issue-images/{image_id}",
    status_code=status.HTTP_410_GONE
)
def deprecated_delete_issue_image():
    raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail=(
            "Image deletion is now scoped to an issue; use "
            "DELETE /issues/{issue_id}/images/{image_id}"
        )
    )
