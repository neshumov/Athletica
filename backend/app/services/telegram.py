from __future__ import annotations

import httpx

from app.core.config import settings


def send_telegram_message(text: str, reply_markup: dict | None = None) -> dict:
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        return {"status": "error", "detail": "Telegram credentials not configured"}

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    payload = {"chat_id": settings.telegram_chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    with httpx.Client(timeout=15.0) as client:
        resp = client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
    return {"status": "ok", "telegram": data}
