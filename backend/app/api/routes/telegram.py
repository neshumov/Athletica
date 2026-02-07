from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.services.telegram import send_telegram_message

router = APIRouter(tags=["telegram"])


@router.post("/telegram/test")
def telegram_test(message: str = "Athletica test message") -> dict:
    result = send_telegram_message(message)
    if result.get("status") != "ok":
        raise HTTPException(status_code=400, detail=result.get("detail"))
    return {"status": "ok"}
