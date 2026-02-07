from __future__ import annotations

from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe
from urllib.parse import urlencode

from sqlalchemy.orm import Session

from app.core.config import settings
from app.integrations.whoop_client import (
    WhoopToken,
    exchange_code_for_token,
    refresh_access_token,
)
from app.models.whoop_oauth import WhoopOAuthState, WhoopToken as WhoopTokenModel

SCOPES = [
    "read:recovery",
    "read:cycles",
    "read:workout",
    "read:sleep",
    "read:profile",
    "read:body_measurement",
    "offline",
]


def build_auth_url(db: Session) -> tuple[str, str]:
    if settings.whoop_redirect_url is None:
        raise ValueError("WHOOP redirect URL is not configured")

    state = token_urlsafe(6)[:8]
    db.add(WhoopOAuthState(state=state))
    db.commit()

    params = {
        "client_id": settings.whoop_client_id,
        "redirect_uri": str(settings.whoop_redirect_url),
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "state": state,
    }
    return f"{settings.whoop_auth_url}?{urlencode(params)}", state


def exchange_code(db: Session, code: str, state: str) -> WhoopToken:
    state_row = db.query(WhoopOAuthState).filter(WhoopOAuthState.state == state).first()
    if not state_row:
        raise ValueError("Invalid state")

    db.delete(state_row)
    db.commit()

    token = exchange_code_for_token(code)
    _upsert_token(db, token)
    return token


def get_valid_token(db: Session) -> WhoopTokenModel | None:
    token_row = db.query(WhoopTokenModel).order_by(WhoopTokenModel.id.desc()).first()
    if not token_row:
        return None

    if token_row.expires_at <= datetime.now(timezone.utc):
        if not token_row.refresh_token:
            return None
        new_token = refresh_access_token(token_row.refresh_token)
        _upsert_token(db, new_token)
        token_row = db.query(WhoopTokenModel).order_by(WhoopTokenModel.id.desc()).first()
    return token_row


def force_refresh_token(db: Session) -> WhoopTokenModel | None:
    token_row = db.query(WhoopTokenModel).order_by(WhoopTokenModel.id.desc()).first()
    if not token_row or not token_row.refresh_token:
        return None
    new_token = refresh_access_token(token_row.refresh_token)
    _upsert_token(db, new_token)
    return db.query(WhoopTokenModel).order_by(WhoopTokenModel.id.desc()).first()


def _upsert_token(db: Session, token: WhoopToken) -> None:
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=token.expires_in)

    db.query(WhoopTokenModel).delete()
    db.add(
        WhoopTokenModel(
            access_token=token.access_token,
            refresh_token=token.refresh_token,
            expires_at=expires_at,
            scope=token.scope,
        )
    )
    db.commit()
