from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class DashboardResponse(BaseModel):
    date: date
    goal_progress: str
    recovery_score: float | None
    latest_recommendation: str | None
