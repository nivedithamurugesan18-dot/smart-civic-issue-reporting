from sqlalchemy.orm import Session

from app.repositories.department_repository import (
    create_department,
    get_all_departments,
    get_department
)


def create(
    db: Session,
    name: str,
    description: str | None = None
):
    return create_department(
        db,
        name,
        description
    )


def get_all(db: Session):
    return get_all_departments(db)


def get_by_id(
    db: Session,
    department_id: int
):
    return get_department(
        db,
        department_id
    )