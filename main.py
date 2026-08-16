"""
JobPilotAI - Punto de entrada de la aplicación.
Corre con: uvicorn main:app --reload
Luego abre: http://localhost:8000/docs
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.database import Base, engine
from app.routers import auth

# Crea las tablas en la base de datos si no existen
# (para producción, usar Alembic en vez de esto)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="Plataforma internacional de búsqueda de empleo potenciada con IA",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": f"Bienvenido a {settings.APP_NAME} 🚀"}
