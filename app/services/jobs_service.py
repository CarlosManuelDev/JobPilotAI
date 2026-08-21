"""
Servicio de búsqueda de empleos.
Consulta APIs externas (Remotive y Adzuna) y normaliza los resultados.
"""
from datetime import datetime
from typing import Optional

import httpx
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.job import Job


def fetch_remotive_jobs(keyword: Optional[str] = None, limit: int = 20) -> list[dict]:
    params = {}
    if keyword:
        params["search"] = keyword

    try:
        response = httpx.get("https://remotive.com/api/remote-jobs", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except httpx.HTTPError:
        return []

    jobs = []
    for item in data.get("jobs", [])[:limit]:
        jobs.append({
            "source": "remotive",
            "external_id": str(item.get("id")),
            "title": item.get("title"),
            "company": item.get("company_name"),
            "description": item.get("description"),
            "country": item.get("candidate_required_location"),
            "city": None,
            "is_remote": True,
            "salary_min": None,
            "salary_max": None,
            "currency": None,
            "url": item.get("url"),
            "category": item.get("category"),
            "posted_at": item.get("publication_date"),
        })
    return jobs


def fetch_adzuna_jobs(
    keyword: Optional[str] = None,
    country: str = "us",
    page: int = 1,
    limit: int = 20,
) -> list[dict]:
    if not settings.ADZUNA_APP_ID or not settings.ADZUNA_APP_KEY:
        return []

    params = {
        "app_id": settings.ADZUNA_APP_ID,
        "app_key": settings.ADZUNA_APP_KEY,
        "results_per_page": limit,
        "content-type": "application/json",
    }
    if keyword:
        params["what"] = keyword

    try:
        response = httpx.get(
            f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}",
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
    except httpx.HTTPError:
        return []

    jobs = []
    for item in data.get("results", []):
        jobs.append({
            "source": "adzuna",
            "external_id": str(item.get("id")),
            "title": item.get("title"),
            "company": (item.get("company") or {}).get("display_name"),
            "description": item.get("description"),
            "country": country,
            "city": (item.get("location") or {}).get("display_name"),
            "is_remote": False,
            "salary_min": item.get("salary_min"),
            "salary_max": item.get("salary_max"),
            "currency": "USD",
            "url": item.get("redirect_url"),
            "category": (item.get("category") or {}).get("label"),
            "posted_at": item.get("created"),
        })
    return jobs


def search_jobs(
    db: Session,
    keyword: Optional[str] = None,
    country: Optional[str] = None,
    remote_only: bool = False,
) -> list[Job]:
    all_jobs_raw = []
    all_jobs_raw += fetch_remotive_jobs(keyword=keyword)

    if not remote_only:
        all_jobs_raw += fetch_adzuna_jobs(keyword=keyword, country=country or "us")

    saved_jobs = []
    for raw in all_jobs_raw:
        existing = (
            db.query(Job)
            .filter(Job.source == raw["source"], Job.external_id == raw["external_id"])
            .first()
        )
        if existing:
            saved_jobs.append(existing)
            continue

        posted_at = None
        if raw.get("posted_at"):
            try:
                posted_at = datetime.fromisoformat(str(raw["posted_at"]).replace("Z", "+00:00"))
            except ValueError:
                posted_at = None

        new_job = Job(
            source=raw["source"],
            external_id=raw["external_id"],
            title=raw["title"] or "Sin título",
            company=raw["company"],
            description=raw["description"],
            country=raw["country"],
            city=raw["city"],
            is_remote=raw["is_remote"],
            salary_min=raw["salary_min"],
            salary_max=raw["salary_max"],
            currency=raw["currency"],
            url=raw["url"],
            category=raw["category"],
            posted_at=posted_at,
        )
        db.add(new_job)
        saved_jobs.append(new_job)

    db.commit()
    return saved_jobs
