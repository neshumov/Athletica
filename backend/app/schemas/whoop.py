from __future__ import annotations

from pydantic import BaseModel, AnyHttpUrl


class WhoopAuthUrl(BaseModel):
    auth_url: AnyHttpUrl
    state: str


class WhoopCallbackResult(BaseModel):
    status: str
    scope: str
