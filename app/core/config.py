"""
Configuración central de JobPilotAI.
Lee variables de entorno desde un archivo .env
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "JobPilotAI"
    ENV: str = "development"  # development | production
    DEBUG: bool = True

    # Base de datos
    DATABASE_URL: str = "sqlite:///./jobpilotai.db"
    # Para producción, algo como:
    # DATABASE_URL: str = "postgresql://user:password@localhost:5432/jobpilotai"

    # Seguridad / JWT
    SECRET_KEY: str = "CAMBIA_ESTA_CLAVE_EN_PRODUCCION"  # usa una clave larga y aleatoria
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 horas
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS (para conectar tu frontend)
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Cachea la instancia de settings para no releer el .env en cada request."""
    return Settings()


settings = get_settings()
