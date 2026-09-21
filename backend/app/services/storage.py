from functools import lru_cache

from supabase import Client, create_client

from app.config import settings


@lru_cache(maxsize=1)
def get_storage_client() -> Client:
    """
    Create and cache the server-side Supabase client.

    The Supabase Secret key is used only by the FastAPI backend.
    It must never be exposed to the frontend.
    """
    if not settings.supabase_url:
        raise RuntimeError("SUPABASE_URL is not configured")

    if not settings.supabase_secret_key:
        raise RuntimeError("SUPABASE_SECRET_KEY is not configured")

    return create_client(
        settings.supabase_url,
        settings.supabase_secret_key,
    )


def upload_issue_image(
    *,
    storage_path: str,
    contents: bytes,
    content_type: str,
) -> str:
    """
    Upload an issue image to Supabase Storage and return
    its public URL.
    """
    client = get_storage_client()

    client.storage.from_(settings.supabase_storage_bucket).upload(
        storage_path,
        contents,
        {
            "content-type": content_type,
            "upsert": False,
        },
    )

    return client.storage.from_(
        settings.supabase_storage_bucket
    ).get_public_url(storage_path)


def delete_issue_image(storage_path: str) -> None:
    """
    Delete an issue image from Supabase Storage.
    """
    client = get_storage_client()

    client.storage.from_(
        settings.supabase_storage_bucket
    ).remove([storage_path])