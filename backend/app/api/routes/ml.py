from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["ml"])


@router.get("/ml/status")
def ml_status() -> dict:
    return {
        "recovery_model": "unknown",
        "progress_model": "unknown",
        "volume_model": "unknown",
    }
