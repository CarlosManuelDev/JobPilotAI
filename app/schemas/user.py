"""
Schemas Pydantic para Usuario (validación de entrada/salida de la API).
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    """Datos requeridos para registrar un nuevo usuario."""
    email: EmailStr
    password: str = Field(min_length=8, description="Mínimo 8 caracteres")
    full_name: Optional[str] = None
    country: Optional[str] = None
    preferred_language: str = "es"


class UserLogin(BaseModel):
    """Datos requeridos para iniciar sesión."""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Campos que el usuario puede actualizar en su perfil."""
    full_name: Optional[str] = None
    country: Optional[str] = None
    preferred_language: Optional[str] = None
    headline: Optional[str] = None
    skills: Optional[str] = None
    open_to_remote: Optional[bool] = None


class UserResponse(BaseModel):
    """Datos del usuario que se devuelven en las respuestas (sin password)."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    full_name: Optional[str] = None
    country: Optional[str] = None
    preferred_language: str
    headline: Optional[str] = None
    skills: Optional[str] = None
    open_to_remote: bool
    is_active: bool
    is_verified: bool
    created_at: datetime
