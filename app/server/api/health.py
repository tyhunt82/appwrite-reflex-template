"""Health check API routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "ok", "message": "API is running"}


@router.get("/health/ready")
async def readiness_check():
    """Readiness check - can add DB/service checks here."""
    return {"status": "ready"}
