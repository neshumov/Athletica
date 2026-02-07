from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.recommendation import Recommendation, RecommendationFeedback
from app.schemas.recommendation import RecommendationFeedbackIn, RecommendationOut

router = APIRouter(tags=["recommendations"])


@router.get("/recommendations", response_model=list[RecommendationOut])
def list_recommendations(db: Session = Depends(get_db)) -> list[RecommendationOut]:
    rows = db.query(Recommendation).order_by(Recommendation.date.desc()).limit(30).all()
    return [RecommendationOut.model_validate(r.__dict__) for r in rows]


@router.post("/recommendations/{recommendation_id}/feedback")
def add_feedback(
    recommendation_id: int,
    payload: RecommendationFeedbackIn,
    db: Session = Depends(get_db),
) -> dict:
    exists = db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
    if not exists:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    feedback = RecommendationFeedback(
        recommendation_id=recommendation_id, feedback=payload.feedback
    )
    db.add(feedback)
    db.commit()
    return {"status": "ok"}
