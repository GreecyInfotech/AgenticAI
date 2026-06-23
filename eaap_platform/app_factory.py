"""Shared FastAPI bootstrap."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from eaap_platform.logging import setup_logging


def create_service_app(title: str, version: str = "1.0.0", metrics: bool = True) -> FastAPI:
    setup_logging()
    app = FastAPI(title=title, version=version)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "healthy", "service": title, "version": version}

    if metrics:
        app.mount("/metrics", make_asgi_app())

    return app
