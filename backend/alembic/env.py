from logging.config import fileConfig
from pathlib import Path
import os

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import create_engine, pool


config = context.config

# Resolve the backend .env explicitly without importing app.main.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.database import Base  # noqa: E402
from app.models.user import User  # noqa: F401, E402
from app.models.issue import Issue  # noqa: F401, E402
from app.models.issue_update import IssueUpdate  # noqa: F401, E402
from app.models.issue_image import IssueImage  # noqa: F401, E402
from app.models.department import Department  # noqa: F401, E402
from app.models.assignment import Assignment  # noqa: F401, E402
from app.models.notification import Notification  # noqa: F401, E402


target_metadata = Base.metadata


def get_database_url() -> str:
    # Require an explicit target so a normal app DATABASE_URL cannot be migrated
    # accidentally. Supply ALEMBIC_DATABASE_URL for each migration command.
    url = os.getenv("ALEMBIC_DATABASE_URL") or config.get_main_option("sqlalchemy.url")

    if not url:
        raise RuntimeError(
            "ALEMBIC_DATABASE_URL must be set before running Alembic."
        )

    return url


def run_migrations_offline() -> None:
    context.configure(
        url=get_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(
        get_database_url(),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
