from __future__ import annotations

from datetime import date

from fastapi import APIRouter

from app.schemas.dashboard import DashboardResponse

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard() -> DashboardResponse:
    return DashboardResponse(
        date=date.today(),
        goal_progress="Stable",
        recovery_score=None,
        latest_recommendation=None,
    )
