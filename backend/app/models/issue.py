from sqlalchemy import Column, Integer, String, Text, Float
from app.database import Base


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False)

    description = Column(Text, nullable=False)

    category = Column(String(100), nullable=False)

    priority = Column(String(50), default="medium")

    severity = Column(String(50), default="medium")

    status = Column(String(50), default="reported")

    location = Column(String(255), nullable=True)

    latitude = Column(Float, nullable=True)

    longitude = Column(Float, nullable=True)

    reported_by = Column(Integer, nullable=False)

    assigned_to = Column(Integer, nullable=True)