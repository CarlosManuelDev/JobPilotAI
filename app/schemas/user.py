from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: Optional[str] = None
    country: Optional[str] = None
    preferred_language: str = "es"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    country: Optional[str] = None
    preferred_language: Optional[str] = None
    headline: Optional[str] = None
    skills: Optional[str] = None
    open_to_remote: Optional[bool] = None


class UserResponse(BaseModel):
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
    is_premium: bool
    cv_analyses_used: int
    created_at: datetime
