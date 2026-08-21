"""
Servicio de análisis de currículum (CV) usando IA (Claude de Anthropic).
Incluye análisis general del CV y comparación contra una vacante específica.
"""
import json

from anthropic import Anthropic

from app.core.config import settings

ANALYSIS_PROMPT = """Eres un reclutador experto internacional (ATS + reclutamiento humano) con 15 años \
de experiencia colocando candidatos en empresas globales y remotas. Analiza el siguiente currículum \
a fondo y da retroalimentación honesta, específica y accionable.

Responde SOLO con un JSON (sin texto adicional, sin markdown, sin backticks) con esta estructura exacta:
{
  "puntuacion_general": (número del 1 al 10),
  "puntuacion_ats": (número del 1 al 10, qué tan bien pasaría filtros automáticos ATS),
  "nivel_experiencia_estimado": ("Junior" | "Semi-Senior" | "Senior" | "Líder/Gerencial"),
  "resumen": "resumen breve de 2-3 líneas sobre el estado general del CV",
  "fortalezas": ["punto fuerte 1", "punto fuerte 2", "punto fuerte 3"],
  "areas_de_mejora": ["área a mejorar 1 con ejemplo concreto", "área a mejorar 2 con ejemplo concreto"],
  "habilidades_detectadas": ["habilidad 1", "habilidad 2", ...],
  "palabras_clave_faltantes": ["palabra clave que le falta para pasar filtros ATS de su área", ...],
  "sugerencia_titulo_profesional": "un titular profesional sugerido, ej: 'Desarrollador Backend Senior'",
  "titulos_de_puesto_sugeridos": ["título de vacante 1 al que debería aplicar", "título 2", "título 3"],
  "recomendaciones_internacionales": "consejos específicos para postularse a trabajos internacionales/remotos con este perfil"
}

Currículum a analizar:
---
{cv_text}
---
"""

MATCH_PROMPT = """Eres un reclutador experto. Compara el siguiente currículum contra esta vacante \
específica, y evalúa qué tan buen candidato es esta persona para ESTA vacante en particular.

Responde SOLO con un JSON (sin texto adicional, sin markdown, sin backticks) con esta estructura exacta:
{{
  "porcentaje_compatibilidad": (número del 0 al 100),
  "veredicto": "una frase corta y honesta sobre qué tan buen match es",
  "coincidencias": ["habilidad/requisito que SÍ cumple 1", "habilidad/requisito que SÍ cumple 2", ...],
  "brechas": ["requisito de la vacante que NO cumple o falta destacar 1", "brecha 2", ...],
  "consejo_para_postularse": "consejo específico y accionable para mejorar sus chances en ESTA vacante"
}}

Currículum del candidato:
---
{cv_text}
---

Vacante a evaluar:
Título: {job_title}
Empresa: {job_company}
Descripción: {job_description}
---
"""


def _get_client() -> Anthropic:
    if not settings.ANTHROPIC_API_KEY:
        raise ValueError(
            "No hay una API key de Anthropic configurada. "
            "Agrega ANTHROPIC_API_KEY en tu archivo .env"
        )
    return Anthropic(api_key=settings.ANTHROPIC_API_KEY)


def _parse_json_response(raw_text: str) -> dict:
    raw_text = raw_text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()
    return json.loads(raw_text)


def analyze_cv(cv_text: str) -> dict:
    """Envía el texto del CV a Claude y devuelve un análisis estructurado y detallado."""
    client = _get_client()
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": ANALYSIS_PROMPT.format(cv_text=cv_text)}],
    )
    return _parse_json_response(message.content[0].text)


def match_cv_to_job(cv_text: str, job_title: str, job_company: str, job_description: str) -> dict:
    """Compara un CV contra una vacante específica y devuelve un puntaje de compatibilidad."""
    client = _get_client()
    prompt = MATCH_PROMPT.format(
        cv_text=cv_text,
        job_title=job_title or "N/A",
        job_company=job_company or "N/A",
        job_description=(job_description or "Sin descripción disponible.")[:4000],
    )
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    return _parse_json_response(message.content[0].text)
