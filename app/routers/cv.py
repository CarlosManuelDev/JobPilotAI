"""
Endpoint para subir y analizar un currículum con IA.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.cv import CVAnalysisResponse, CVMatchResponse
from app.services import file_service, cv_service, payment_service
from app.auth.dependencies import get_current_active_user
from app.models.user import User
from app.models.job import Job

router = APIRouter(prefix="/api/cv", tags=["Currículum (IA)"])


@router.post("/analyze", response_model=CVAnalysisResponse)
async def analyze_cv(
    file: UploadFile = File(..., description="Archivo del CV: PDF, DOCX o TXT"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Sube un CV, extrae su texto, y lo analiza con IA.
    Requiere estar autenticado (usa el botón Authorize con tu token).
    Los usuarios gratis tienen un número limitado de análisis; premium es ilimitado.
    """
    if not payment_service.can_use_cv_analysis(current_user):
        raise HTTPException(
            status_code=402,
            detail=(
                f"Ya usaste tu análisis gratis "
                f"({payment_service.FREE_CV_ANALYSES_LIMIT}). "
                "Actualiza a Premium para análisis ilimitados."
            ),
        )

    file_bytes = await file.read()

    try:
        cv_text = file_service.extract_text(file.filename, file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not cv_text or len(cv_text) < 50:
        raise HTTPException(
            status_code=400,
            detail="No se pudo extraer suficiente texto del archivo. ¿Está vacío o es una imagen escaneada?",
        )

    try:
        analysis = cv_service.analyze_cv(cv_text)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error al analizar el CV con la IA. Intenta de nuevo.")

    # Guardamos el texto del CV en el perfil del usuario para uso futuro (matching)
    current_user.cv_text = cv_text
    db.commit()

    payment_service.register_cv_analysis_usage(db, current_user)

    return analysis


@router.get("/match/{job_id}", response_model=CVMatchResponse)
def match_cv_with_job(
    job_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Compara el CV ya guardado del usuario (del último análisis) contra una vacante
    específica, y devuelve un porcentaje de compatibilidad con recomendaciones.
    """
    if not current_user.cv_text:
        raise HTTPException(
            status_code=400,
            detail="Primero debes analizar tu CV al menos una vez antes de comparar con vacantes.",
        )

    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Vacante no encontrada.")

    try:
        result = cv_service.match_cv_to_job(
            cv_text=current_user.cv_text,
            job_title=job.title,
            job_company=job.company,
            job_description=job.description,
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error al comparar el CV con la vacante. Intenta de nuevo.")

    return result
