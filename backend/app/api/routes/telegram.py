from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.recommendation import Recommendation, RecommendationFeedback
from app.services.telegram import send_telegram_message

router = APIRouter(tags=["telegram"])


@router.post("/telegram/test")
def telegram_test(message: str = "Athletica test message") -> dict:
    result = send_telegram_message(message)
    if result.get("status") != "ok":
        raise HTTPException(status_code=400, detail=result.get("detail"))
    return {"status": "ok"}


@router.post("/telegram/webhook")
async def telegram_webhook(request: Request, db: Session = Depends(get_db)) -> dict:
    payload = await request.json()
    callback = payload.get("callback_query") if isinstance(payload, dict) else None
    if not callback:
        return {"status": "ignored"}

    data = callback.get("data", "")
    if not data.startswith("rec:"):
        return {"status": "ignored"}
    try:
        _, rec_id, feedback = data.split(":", 2)
        rec_id_int = int(rec_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid callback data")

    exists = db.query(Recommendation).filter(Recommendation.id == rec_id_int).first()
    if not exists:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    existing = (
        db.query(RecommendationFeedback)
        .filter(RecommendationFeedback.recommendation_id == rec_id_int)
        .first()
    )
    if existing:
        existing.feedback = feedback
    else:
        row = RecommendationFeedback(recommendation_id=rec_id_int, feedback=feedback)
        db.add(row)
    db.commit()
    return {"status": "ok"}
