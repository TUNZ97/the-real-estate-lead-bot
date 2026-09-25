"""FastAPI application entrypoint."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup hooks (DB pool, etc.) will be added in later phases
    yield
    # Shutdown hooks


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        docs_url="/docs" if settings.is_development else None,
        redoc_url="/redoc" if settings.is_development else None,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["health"])
    async def health() -> dict:
        return {"status": "ok", "service": settings.app_name}

    @app.get("/ready", tags=["health"])
    async def ready() -> dict:
        # Will check DB connectivity in Phase 2+
        return {"status": "ready"}

    # API routers will be mounted here in Phase 3
    # from app.api.v1.router import api_router
    # app.include_router(api_router, prefix=settings.api_prefix)

    return app


app = create_app()
