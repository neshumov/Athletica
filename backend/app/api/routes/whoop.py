from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.whoop import WhoopAuthUrl, WhoopCallbackResult
from app.services.whoop_oauth import build_auth_url, exchange_code, get_valid_token
from app.workers.tasks import sync_whoop

router = APIRouter(tags=["whoop"])


@router.get("/whoop/auth", response_model=WhoopAuthUrl)
def whoop_auth(db: Session = Depends(get_db)) -> WhoopAuthUrl:
    try:
        url, state = build_auth_url(db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return WhoopAuthUrl(auth_url=url, state=state)


@router.get("/whoop/callback", response_model=WhoopCallbackResult)
def whoop_callback(
    code: str = Query(...), state: str = Query(...), db: Session = Depends(get_db)
) -> WhoopCallbackResult:
    try:
        token = exchange_code(db, code=code, state=state)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return WhoopCallbackResult(status="ok", scope=token.scope)


@router.post("/whoop/sync")
def trigger_sync(db: Session = Depends(get_db)) -> dict:
    token = get_valid_token(db)
    if not token:
        raise HTTPException(status_code=401, detail="WHOOP not authorized")
    sync_whoop.delay()
    return {"status": "queued"}
