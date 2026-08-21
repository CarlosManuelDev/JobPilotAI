"""
Configuración central de JobPilotAI.
Lee variables de entorno desde un archivo .env
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "JobPilotAI"
    ENV: str = "development"
    DEBUG: bool = True

    # Base de datos
    DATABASE_URL: str = "sqlite:///./jobpilotai.db"

    # Seguridad / JWT
    SECRET_KEY: str = "CAMBIA_ESTA_CLAVE_EN_PRODUCCION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Adzuna API (gratis, registrate en https://developer.adzuna.com/)
    ADZUNA_APP_ID: str = ""
    ADZUNA_APP_KEY: str = ""

    # Anthropic API (para analisis de CV con IA) - console.anthropic.com
    ANTHROPIC_API_KEY: str = ""

    # Lemon Squeezy (pagos, sin necesidad de empresa) - app.lemonsqueezy.com
    LEMONSQUEEZY_API_KEY: str = ""
    LEMONSQUEEZY_STORE_ID: str = ""
    LEMONSQUEEZY_VARIANT_ID_PREMIUM: str = ""  # ID de la variante del producto premium
    LEMONSQUEEZY_WEBHOOK_SECRET: str = ""
    FRONTEND_URL: str = "http://127.0.0.1:8000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
