from __future__ import annotations

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ATHLETICA_", case_sensitive=False)

    environment: str = "dev"
    # Default avoids secrets in repo; override via SOPS-decrypted envs in real use.
    database_url: str = "postgresql+psycopg2://localhost/athletica"
    redis_url: str = "redis://redis:6379/0"
    whoop_client_id: str | None = None
    whoop_client_secret: str | None = None
    whoop_redirect_url: AnyHttpUrl | None = None
    whoop_token_url: AnyHttpUrl = "https://api.prod.whoop.com/oauth/oauth2/token"
    whoop_auth_url: AnyHttpUrl = "https://api.prod.whoop.com/oauth/oauth2/auth"

    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None

    mlflow_tracking_uri: str | None = None


settings = Settings()
