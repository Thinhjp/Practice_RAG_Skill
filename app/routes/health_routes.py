from fastapi import APIRouter

from app.config import config
from app.schemas import HealthResponse

router = APIRouter(prefix="/api/v1", tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy", app_name=config.APP_NAME, version=config.API_VERSION
    )
