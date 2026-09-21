import logging
from pathlib import Path
from urllib.parse import unquote, urlparse
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.issue import Issue
from app.models.issue_image import IssueImage
from app.models.user import User
from app.schemas.issue_image import IssueImageResponse
from app.services.storage import (
    delete_issue_image,
    upload_issue_image,
)
from app.dependencies import get_current_user


router = APIRouter()
logger = logging.getLogger(__name__)


# ============================================================
# IMAGE VALIDATION
# ============================================================

MAX_IMAGE_SIZE = 5 * 1024 * 1024

ALLOWED_CONTENT_TYPES = {
    "image/jpeg": (".jpg", ".jpeg"),
    "image/png": (".png",),
    "image/webp": (".webp",),
}


# ============================================================
# AUTHORIZATION
# ============================================================


def _is_authorized_for_issue(
    issue: Issue,
    current_user: User,
) -> bool:
    """
    Check whether the current user is allowed to manage
    images attached to the specified issue.
    """

    if current_user.role == "admin":
        return True

    if current_user.role == "citizen":
        return issue.reported_by == current_user.id

    if current_user.role == "field_staff":
        return issue.assigned_to == current_user.id

    return False


# ============================================================
# FILE VALIDATION
# ============================================================


def _validate_image(
    *,
    contents: bytes,
    content_type: str | None,
    file_name: str | None,
) -> str:
    """
    Validate image MIME type, size, extension and magic bytes.

    Returns the normalized extension.
    """

    if not content_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image content type is required.",
        )

    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Unsupported image type. "
                "Only JPEG, PNG and WEBP images are allowed."
            ),
        )

    if len(contents) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded image is empty.",
        )

    if len(contents) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Image size must not exceed 5 MB.",
        )

    extension = Path(file_name or "").suffix.lower()

    allowed_extensions = ALLOWED_CONTENT_TYPES[content_type]

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image extension does not match the supplied content type.",
        )

    # --------------------------------------------------------
    # Magic-byte validation
    # --------------------------------------------------------

    if content_type == "image/jpeg":
        # JPEG files normally begin with FF D8 FF.
        if not contents.startswith(b"\xff\xd8\xff"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JPEG image.",
            )

    elif content_type == "image/png":
        # PNG signature.
        if not contents.startswith(
            b"\x89PNG\r\n\x1a\n"
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid PNG image.",
            )

    elif content_type == "image/webp":
        # WEBP = RIFF....WEBP
        if (
            len(contents) < 12
            or contents[:4] != b"RIFF"
            or contents[8:12] != b"WEBP"
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid WEBP image.",
            )

    return extension


# ============================================================
# STORAGE PATH HELPERS
# ============================================================


def _build_storage_path(
    *,
    issue_id: int,
    generated_file_name: str,
) -> str:
    """
    Build the object path used inside the Supabase bucket.
    """

    return f"issues/{issue_id}/{generated_file_name}"


def _storage_path_from_public_url(
    image_url: str,
) -> str | None:
    """
    Extract the Supabase Storage object path from a public URL.

    Expected format:

    /storage/v1/object/public/<bucket>/<object-path>
    """

    try:
        parsed = urlparse(image_url)
        path = unquote(parsed.path)

        marker = "/storage/v1/object/public/"

        if marker not in path:
            return None

        storage_path = path.split(marker, 1)[1]

        # Remove bucket name from the beginning.
        parts = storage_path.split("/", 1)

        if len(parts) != 2:
            return None

        return parts[1]

    except Exception:
        logger.exception(
            "Failed to extract Supabase storage path from image URL."
        )
        return None


# ============================================================
# UPLOAD IMAGE
# ============================================================


@router.post(
    "/issues/{issue_id}/images",
    response_model=IssueImageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_issue_image(
    issue_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload an evidence image for an issue.

    Images are stored in Supabase Storage.
    Image metadata is stored in PostgreSQL.
    """

    issue = (
        db.query(Issue)
        .filter(Issue.id == issue_id)
        .first()
    )

    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found.",
        )

    if not _is_authorized_for_issue(
        issue,
        current_user,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to manage images for this issue.",
        )

    contents = await file.read()

    extension = _validate_image(
        contents=contents,
        content_type=file.content_type,
        file_name=file.filename,
    )

    generated_file_name = (
        f"{uuid4().hex}{extension}"
    )

    storage_path = _build_storage_path(
        issue_id=issue_id,
        generated_file_name=generated_file_name,
    )

    try:
        image_url = upload_issue_image(
            storage_path=storage_path,
            contents=contents,
            content_type=file.content_type,
        )

    except Exception:
        logger.exception(
            "Failed to upload issue image to Supabase Storage."
        )

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to upload image to storage.",
        )

    image = IssueImage(
        issue_id=issue_id,
        image_url=image_url,
        file_name=file.filename,
    )

    try:
        db.add(image)
        db.commit()
        db.refresh(image)

    except Exception:
        db.rollback()

        # The storage upload succeeded but the database insert
        # failed. Attempt to remove the uploaded object so that
        # an orphaned storage file is not left behind.
        try:
            delete_issue_image(storage_path)
        except Exception:
            logger.exception(
                "Failed to clean up Supabase image after "
                "database insert failure."
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save image information.",
        )

    return image


# ============================================================
# LIST ISSUE IMAGES
# ============================================================


@router.get(
    "/issues/{issue_id}/images",
    response_model=list[IssueImageResponse],
)
def get_issue_images(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return all images associated with an issue.
    """

    issue = (
        db.query(Issue)
        .filter(Issue.id == issue_id)
        .first()
    )

    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found.",
        )

    if not _is_authorized_for_issue(
        issue,
        current_user,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to view images for this issue.",
        )

    return (
        db.query(IssueImage)
        .filter(IssueImage.issue_id == issue_id)
        .order_by(IssueImage.id.asc())
        .all()
    )


# ============================================================
# DELETE ISSUE IMAGE
# ============================================================


@router.delete(
    "/issues/{issue_id}/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_issue_image_endpoint(
    issue_id: int,
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete an issue image from Supabase Storage and PostgreSQL.
    """

    image = (
        db.query(IssueImage)
        .filter(
            IssueImage.id == image_id,
            IssueImage.issue_id == issue_id,
        )
        .first()
    )

    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue image not found.",
        )

    issue = (
        db.query(Issue)
        .filter(Issue.id == issue_id)
        .first()
    )

    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found.",
        )

    if not _is_authorized_for_issue(
        issue,
        current_user,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete images for this issue.",
        )

    storage_path = _storage_path_from_public_url(
        image.image_url
    )

    # Delete the database record first, matching the existing
    # application's behavior. If the database operation fails,
    # the storage object is preserved.
    db.delete(image)

    try:
        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete image information.",
        )

    # Remove the corresponding Supabase object after the
    # database record has been removed.
    if storage_path:
        try:
            delete_issue_image(storage_path)

        except Exception:
            # The DB record is already removed. Log the storage
            # failure so it can be cleaned up without exposing
            # internal storage details to the client.
            logger.exception(
                "Image metadata was deleted, but the Supabase "
                "Storage object could not be removed."
            )

    return None


# ============================================================
# LEGACY LOCAL-STORAGE ENDPOINTS
# ============================================================
#
# These endpoints are intentionally retained as deprecated
# compatibility routes. They are not used by the active
# frontend flow.


@router.get(
    "/issues/{issue_id}/images/{image_id}/file",
    status_code=status.HTTP_410_GONE,
)
def legacy_issue_image_file(
    issue_id: int,
    image_id: int,
):
    raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail=(
            "Direct local image-file access is deprecated. "
            "Use the image_url returned by the API."
        ),
    )


@router.get(
    "/issues/{issue_id}/images/{image_id}/download",
    status_code=status.HTTP_410_GONE,
)
def legacy_issue_image_download(
    issue_id: int,
    image_id: int,
):
    raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail=(
            "Local image download is deprecated. "
            "Use the image_url returned by the API."
        ),
    )