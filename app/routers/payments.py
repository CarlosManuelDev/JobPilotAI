"""
Endpoints de pagos: crear sesión de pago, webhook de Lemon Squeezy, y estado de suscripción.
"""
import json

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.database import get_db
from app.services import payment_service
from app.auth.dependencies import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/api/payments", tags=["Pagos"])


class CheckoutResponse(BaseModel):
    checkout_url: str


class SubscriptionStatus(BaseModel):
    is_premium: bool
    cv_analyses_used: int
    free_analyses_limit: int


@router.post("/create-checkout-session", response_model=CheckoutResponse)
def create_checkout(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Crea una sesión de pago en Lemon Squeezy y devuelve la URL a la que el usuario debe ir a pagar."""
    url = payment_service.create_checkout_session(db, current_user)
    return {"checkout_url": url}


@router.get("/status", response_model=SubscriptionStatus)
def subscription_status(current_user: User = Depends(get_current_active_user)):
    """Consulta si el usuario tiene premium activo y cuántos análisis gratis le quedan."""
    return {
        "is_premium": current_user.is_premium,
        "cv_analyses_used": current_user.cv_analyses_used,
        "free_analyses_limit": payment_service.FREE_CV_ANALYSES_LIMIT,
    }


@router.post("/webhook")
async def lemonsqueezy_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Endpoint que Lemon Squeezy llama automáticamente cuando ocurre un evento
    (pago exitoso, cancelación, etc). No lo llama el usuario directamente.
    """
    payload = await request.body()
    signature = request.headers.get("x-signature", "")

    if not payment_service.verify_webhook_signature(payload, signature):
        raise HTTPException(status_code=400, detail="Firma de webhook inválida.")

    event = json.loads(payload)
    return payment_service.handle_lemonsqueezy_webhook(db, event)
