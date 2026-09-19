from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Smart Public Infrastructure Issue Reporting System"
    app_version: str = "1.0.0"
    debug: bool = False

    class Config:
        env_file = ".env"


settings = Settings()