"""API routes exports."""

from app.server.api.health import router as health_router

__all__ = ["health_router"]
