import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, DateTime, Float, Boolean

from app.database.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source = Column(String(50), nullable=False)
    external_id = Column(String(255), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    company = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    country = Column(String(100), nullable=True)
    city = Column(String(255), nullable=True)
    is_remote = Column(Boolean, default=False)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    currency = Column(String(10), nullable=True)
    url = Column(String(1000), nullable=True)
    category = Column(String(255), nullable=True)
    posted_at = Column(DateTime, nullable=True)
    fetched_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Job {self.title} @ {self.company}>"
