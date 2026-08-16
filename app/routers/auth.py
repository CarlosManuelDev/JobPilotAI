"""
Endpoints de autenticación: /register, /login, /me
"""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.services import auth_service
from app.auth.dependencies import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Crea una nueva cuenta de usuario."""
    return auth_service.register_user(db, user_data)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Inicia sesión y devuelve tokens de acceso.
    Usa OAuth2PasswordRequestForm: espera 'username' (aquí es el email) y 'password'
    como form-data, siguiendo el estándar de FastAPI.
    """
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    return auth_service.create_tokens_for_user(user)


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_active_user)):
    """Devuelve el perfil del usuario autenticado."""
    return current_user
