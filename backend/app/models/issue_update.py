from sqlalchemy import Column, Integer, Text, String, DateTime
from sqlalchemy.sql import func

from app.database import Base


class IssueUpdate(Base):
    __tablename__ = "issue_updates"

    id = Column(Integer, primary_key=True, index=True)

    issue_id = Column(Integer, nullable=False, index=True)

    updated_by = Column(Integer, nullable=False)

    message = Column(Text, nullable=False)

    status = Column(String(50), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )