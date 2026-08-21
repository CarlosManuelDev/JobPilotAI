from pydantic import BaseModel


class CVAnalysisResponse(BaseModel):
    puntuacion_general: int
    puntuacion_ats: int
    nivel_experiencia_estimado: str
    resumen: str
    fortalezas: list[str]
    areas_de_mejora: list[str]
    habilidades_detectadas: list[str]
    palabras_clave_faltantes: list[str]
    sugerencia_titulo_profesional: str
    titulos_de_puesto_sugeridos: list[str]
    recomendaciones_internacionales: str


class CVMatchResponse(BaseModel):
    porcentaje_compatibilidad: int
    veredicto: str
    coincidencias: list[str]
    brechas: list[str]
    consejo_para_postularse: str
