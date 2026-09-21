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