from sqlalchemy.orm import Session

from app.models.department import Department


def create_department(
    db: Session,
    name: str,
    description: str | None = None
):
    department = Department(
        name=name,
        description=description
    )

    db.add(department)
    db.commit()
    db.refresh(department)

    return department


def get_all_departments(db: Session):
    return (
        db.query(Department)
        .order_by(Department.id.asc())
        .all()
    )


def get_department(
    db: Session,
    department_id: int
):
    return (
        db.query(Department)
        .filter(Department.id == department_id)
        .first()
    )