from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Recommendation(Base):
    __tablename__ = "recommendation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date] = mapped_column(Date)
    type: Mapped[str] = mapped_column(String(32))
    message: Mapped[str] = mapped_column(String(512))
    confidence_score: Mapped[float] = mapped_column(Float)
    model_version: Mapped[str] = mapped_column(String(64))
    explanation_json: Mapped[dict | None] = mapped_column(JSON)


class RecommendationFeedback(Base):
    __tablename__ = "recommendation_feedback"

    recommendation_id: Mapped[int] = mapped_column(
        ForeignKey("recommendation.id"), primary_key=True
    )
    feedback: Mapped[str] = mapped_column(String(16))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
