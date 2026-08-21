from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.job import JobResponse
from app.services import jobs_service
from app.models.job import Job

router = APIRouter(prefix="/api/jobs", tags=["Empleos"])


@router.get("/search", response_model=list[JobResponse])
def search_jobs(
    keyword: Optional[str] = Query(None, description="Palabra clave, ej: 'python developer'"),
    country: Optional[str] = Query(None, description="Código de país, ej: 'us', 'de', 'gb'"),
    remote_only: bool = Query(False, description="Solo trabajos remotos"),
    db: Session = Depends(get_db),
):
    """Busca ofertas de empleo combinando varias fuentes (Remotive, Adzuna)."""
    return jobs_service.search_jobs(
        db=db, keyword=keyword, country=country, remote_only=remote_only
    )


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: str, db: Session = Depends(get_db)):
    """Obtiene el detalle completo de una vacante específica por su ID."""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Vacante no encontrada.")
    return job
