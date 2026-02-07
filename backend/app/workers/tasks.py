from __future__ import annotations

import httpx

from app.db.session import SessionLocal
from app.integrations.whoop_client import WhoopClient
from app.ml.pipeline import train_all_models
from app.services.whoop_oauth import force_refresh_token, get_valid_token
from app.workers.celery_app import celery_app


@celery_app.task
def sync_whoop() -> dict:
    db = SessionLocal()
    try:
        token_row = get_valid_token(db)
        if not token_row:
            return {"status": "unauthorized"}

        client = WhoopClient(token_row.access_token)

        try:
            client.get_cycles()
            return {"status": "ok"}
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 401:
                refreshed = force_refresh_token(db)
                if not refreshed:
                    return {"status": "unauthorized"}
                client = WhoopClient(refreshed.access_token)
                client.get_cycles()
                return {"status": "ok"}
            raise
    except httpx.RequestError as exc:
        raise sync_whoop.retry(exc=exc, countdown=30, max_retries=5)
    except httpx.HTTPStatusError as exc:
        raise sync_whoop.retry(exc=exc, countdown=60, max_retries=3)
    finally:
        db.close()


@celery_app.task
def train_models() -> dict:
    return train_all_models()
