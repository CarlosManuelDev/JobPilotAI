import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    country = Column(String(100), nullable=True)
    preferred_language = Column(String(10), default="es")
    headline = Column(String(255), nullable=True)
    skills = Column(Text, nullable=True)
    cv_text = Column(Text, nullable=True)
    open_to_remote = Column(Boolean, default=True)

    # Suscripción / pagos
    is_premium = Column(Boolean, default=False)
    lemonsqueezy_customer_id = Column(String(255), nullable=True)
    lemonsqueezy_subscription_id = Column(String(255), nullable=True)
    cv_analyses_used = Column(Integer, default=0)  # cuántos análisis gratis ya usó
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<User {self.email}>"
