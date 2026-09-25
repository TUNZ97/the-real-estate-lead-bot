"""Application configuration loaded from environment variables."""

from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

# Prefer repo-root .env, then backend/.env
_ROOT_ENV = Path(__file__).resolve().parents[3] / ".env"
_BACKEND_ENV = Path(__file__).resolve().parents[2] / ".env"
_ENV_FILES = tuple(
    str(p) for p in (_ROOT_ENV, _BACKEND_ENV) if p.is_file()
) or (".env",)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILES,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Real Estate Lead Bot"
    app_env: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    api_prefix: str = "/api"

    # Local development uses MySQL on the host (no Docker required)
    database_url: str = (
        "mysql+aiomysql://root:password@127.0.0.1:3306/real_estate_lead_bot"
    )

    jwt_secret: str = "change-me-to-a-long-random-string"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    n8n_webhook_secret: str = "change-me-n8n-webhook-secret"

    frontend_url: str = "http://localhost:5173"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    ai_api_key: str = ""
    ai_model: str = "gpt-4o-mini"
    ai_base_url: str = ""
    ai_timeout_seconds: int = 30

    n8n_base_url: str = "http://localhost:5678"
    n8n_webhook_url: str = "http://localhost:5678/webhook"

    @property
    def cors_origin_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def is_development(self) -> bool:
        return self.app_env.lower() in {"development", "dev", "local"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
