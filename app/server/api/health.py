"""Health check API routes."""

from __future__ import annotations

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse


async def health_check(_: Request) -> JSONResponse:
    """Basic health check endpoint."""
    return JSONResponse({"status": "ok", "message": "API is running"})


async def readiness_check(_: Request) -> JSONResponse:
    """Readiness check - can add DB/service checks here."""
    return JSONResponse({"status": "ready"})


def register_health_routes(app: Starlette) -> None:
    """Register health endpoints on the given Starlette app."""
    app.add_route("/api/health", health_check, methods=["GET"])
    app.add_route("/api/health/ready", readiness_check, methods=["GET"])
