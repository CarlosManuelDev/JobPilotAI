"""
Servicio de pagos con Lemon Squeezy.
Lemon Squeezy actúa como "vendedor oficial" (Merchant of Record), lo que permite
cobrar suscripciones internacionales sin necesidad de tener una empresa registrada.
"""
import hashlib
import hmac

import httpx
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.core.config import settings
from app.models.user import User

FREE_CV_ANALYSES_LIMIT = 1  # cuántos análisis gratis tiene un usuario antes de pedirle premium

LEMONSQUEEZY_API_BASE = "https://api.lemonsqueezy.com/v1"


def _ensure_configured():
    if not settings.LEMONSQUEEZY_API_KEY or not settings.LEMONSQUEEZY_STORE_ID:
        raise HTTPException(
            status_code=500,
            detail="Los pagos no están configurados todavía. Faltan las claves de Lemon Squeezy en el .env",
        )


def _headers():
    return {
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {settings.LEMONSQUEEZY_API_KEY}",
    }


def create_checkout_session(db: Session, user: User) -> str:
    """Crea una sesión de pago (checkout) en Lemon Squeezy y devuelve la URL a la que redirigir."""
    _ensure_configured()

    if not settings.LEMONSQUEEZY_VARIANT_ID_PREMIUM:
        raise HTTPException(
            status_code=500,
            detail="Falta configurar LEMONSQUEEZY_VARIANT_ID_PREMIUM en el .env",
        )

    payload = {
        "data": {
            "type": "checkouts",
            "attributes": {
                "checkout_data": {
                    "email": user.email,
                    "name": user.full_name or "",
                    "custom": {"user_id": user.id},
                },
                "product_options": {
                    "redirect_url": f"{settings.FRONTEND_URL}/?payment=success",
                },
            },
            "relationships": {
                "store": {"data": {"type": "stores", "id": str(settings.LEMONSQUEEZY_STORE_ID)}},
                "variant": {"data": {"type": "variants", "id": str(settings.LEMONSQUEEZY_VARIANT_ID_PREMIUM)}},
            },
        }
    }

    try:
        response = httpx.post(
            f"{LEMONSQUEEZY_API_BASE}/checkouts",
            json=payload,
            headers=_headers(),
            timeout=15,
        )
        response.raise_for_status()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Error al crear el pago con Lemon Squeezy: {e}")

    data = response.json()
    return data["data"]["attributes"]["url"]


def verify_webhook_signature(payload: bytes, signature_header: str) -> bool:
    """Verifica que el webhook realmente viene de Lemon Squeezy (no es falso)."""
    if not settings.LEMONSQUEEZY_WEBHOOK_SECRET:
        return False
    digest = hmac.new(
        settings.LEMONSQUEEZY_WEBHOOK_SECRET.encode("utf-8"),
        payload,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(digest, signature_header or "")


def handle_lemonsqueezy_webhook(db: Session, event: dict) -> dict:
    """Procesa un evento de webhook ya verificado y actualiza el estado premium del usuario."""
    event_name = event.get("meta", {}).get("event_name", "")
    custom_data = event.get("meta", {}).get("custom_data", {}) or {}
    user_id = custom_data.get("user_id")

    attributes = event.get("data", {}).get("attributes", {})
    customer_id = attributes.get("customer_id")
    subscription_id = event.get("data", {}).get("id")

    if event_name in ("subscription_created", "subscription_updated", "subscription_resumed"):
        status_value = attributes.get("status")
        user = None
        if user_id:
            user = db.query(User).filter(User.id == user_id).first()
        elif customer_id:
            user = db.query(User).filter(User.lemonsqueezy_customer_id == str(customer_id)).first()

        if user:
            user.is_premium = status_value in ("active", "on_trial")
            user.lemonsqueezy_customer_id = str(customer_id) if customer_id else user.lemonsqueezy_customer_id
            user.lemonsqueezy_subscription_id = str(subscription_id)
            db.commit()

    elif event_name in ("subscription_cancelled", "subscription_expired"):
        user = db.query(User).filter(User.lemonsqueezy_subscription_id == str(subscription_id)).first()
        if user:
            user.is_premium = False
            db.commit()

    return {"status": "ok", "event": event_name}


def can_use_cv_analysis(user: User) -> bool:
    """Determina si el usuario puede analizar un CV (premium ilimitado, gratis con límite)."""
    if user.is_premium:
        return True
    return user.cv_analyses_used < FREE_CV_ANALYSES_LIMIT


def register_cv_analysis_usage(db: Session, user: User):
    """Incrementa el contador de análisis gratis usados."""
    if not user.is_premium:
        user.cv_analyses_used += 1
        db.commit()
