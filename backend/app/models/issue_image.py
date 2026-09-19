from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class IssueImage(Base):
    __tablename__ = "issue_images"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    issue_id = Column(
        Integer,
        ForeignKey("issues.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    image_url = Column(
        String(500),
        nullable=False
    )

    file_name = Column(
        String(255),
        nullable=True
    )