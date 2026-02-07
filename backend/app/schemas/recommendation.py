from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class RecommendationOut(BaseModel):
    id: int
    date: date
    type: str
    message: str
    confidence_score: float
    model_version: str
    explanation_json: dict | None


class RecommendationFeedbackIn(BaseModel):
    feedback: str
