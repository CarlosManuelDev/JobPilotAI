from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    source: str
    title: str
    company: Optional[str] = None
    description: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    is_remote: bool
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: Optional[str] = None
    url: Optional[str] = None
    category: Optional[str] = None
    posted_at: Optional[datetime] = None


class JobSearchParams(BaseModel):
    keyword: Optional[str] = None
    country: Optional[str] = None
    remote_only: bool = False
    page: int = 1
    results_per_page: int = 20
