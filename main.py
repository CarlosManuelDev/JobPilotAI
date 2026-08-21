"""
JobPilotAI - Punto de entrada de la aplicación.
Corre con: uvicorn main:app --reload
Luego abre: http://127.0.0.1:8000  (esa es la app visual)
Documentación técnica: http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.database.database import Base, engine
from app.routers import auth, jobs, cv, payments

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="Plataforma internacional de búsqueda de empleo potenciada con IA",
    version="0.3.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # abierto para desarrollo local; restringir en producción
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(cv.router)
app.include_router(payments.router)

# Sirve el frontend (static/index.html) en la raíz "/"
app.mount("/", StaticFiles(directory="static", html=True), name="static")
