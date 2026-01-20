"""API routes exports."""

from app.server.api.health import register_health_routes

__all__ = ["register_health_routes"]
