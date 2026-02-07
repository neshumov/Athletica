from __future__ import annotations

from fastapi import APIRouter

from app.api.routes import dashboard, ml, recommendations, whoop, workouts

api_router = APIRouter()
api_router.include_router(dashboard.router)
api_router.include_router(workouts.router)
api_router.include_router(recommendations.router)
api_router.include_router(whoop.router)
api_router.include_router(ml.router)
