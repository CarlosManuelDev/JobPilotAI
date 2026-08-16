"""
Modelo de Usuario. Pensado para una plataforma internacional de búsqueda de empleo.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import String as SAString

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Credenciales
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # Perfil básico
    full_name = Column(String(255), nullable=True)
    country = Column(String(100), nullable=True)          # país de residencia
    preferred_language = Column(String(10), default="es")  # es, en, etc.

    # Perfil profesional (para matching más adelante)
    headline = Column(String(255), nullable=True)          # ej: "Desarrollador Backend Senior"
    skills = Column(Text, nullable=True)                   # lista separada por comas, o JSON
    cv_text = Column(Text, nullable=True)                  # texto extraído del CV
    open_to_remote = Column(Boolean, default=True)

    # Estado de la cuenta
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
