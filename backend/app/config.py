from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Smart Public Infrastructure Issue Reporting System"
    app_version: str = "1.0.0"
    debug: bool = False

    database_url: str
    secret_key: str

    # Comma-separated frontend origins.
    # Example:
    # http://localhost:5173,http://127.0.0.1:5173
    cors_origins: str = (
        "http://localhost:5173,"
        "http://127.0.0.1:5173"
    )

    # Supabase project URL used by the backend Storage client.
    supabase_url: str = ""

    # Current server-side Supabase Secret key.
    # Keep this secret and never expose it to the frontend.
    supabase_secret_key: str = ""

    # Supabase Storage bucket for issue evidence images.
    supabase_storage_bucket: str = "issue-images"

    @property
    def cors_origin_list(self) -> list[str]:
        """Return configured CORS origins as a clean list."""
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]

    class Config:
        env_file = ".env"


settings = Settings()