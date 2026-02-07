from __future__ import annotations

from fastapi import FastAPI

from app.api.router import api_router

app = FastAPI(title="Athletica API")
app.include_router(api_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
