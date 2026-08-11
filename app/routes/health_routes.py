"""
=============================================================================
MODULE: HEALTH_ROUTES.PY
Purpose: Endpoints for health checks
=============================================================================

Routes:
- GET /api/v1/health - Health check endpoint
"""

from fastapi import APIRouter

from app.config import config
from app.schemas import HealthResponse


# Tạo router cho health routes
router = APIRouter(
    prefix="/api/v1",
    tags=["Health"]
)


# ============================================================================
# ENDPOINT: Health Check
# ============================================================================
@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    TODO: Endpoint to check the application's health status

    This endpoint is used by:
    - Load balancers to check if the server is ready
    - Kubernetes readiness probes
    - Monitoring systems

    Example request:
    curl "http://localhost:8000/api/v1/health"

    Example response:
    {
        "status": "healthy",
        "app_name": "RAG Pipeline Backend",
        "version": "1.0.0"
    }

    Implementation suggestion:
    # Simplest approach - just return the status
    return HealthResponse(
        status="healthy",
        app_name=config.APP_NAME,
        version=config.API_VERSION
    )

    # Alternatively, add additional checks:
    # - database connection
    # - file system access
    # - memory usage
    # - etc.
    """
    # Start coding here
    pass
