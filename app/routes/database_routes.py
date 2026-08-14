from typing import Dict

from fastapi import APIRouter, HTTPException

from app.modules import vector_db
from app.schemas import DatabaseStats
from app.services import DatabaseService

router = APIRouter(prefix="/api/v1", tags=["Database"])


@router.get("/stats", response_model=DatabaseStats)
async def get_database_stats() -> DatabaseStats:
    try:
        return DatabaseStats(**DatabaseService.get_stats())
    except Exception as exc:
        raise HTTPException(500, str(exc)) from exc


@router.delete("/database")
async def clear_database() -> Dict[str, str]:
    try:
        return DatabaseService.clear_database()
    except Exception as exc:
        raise HTTPException(500, str(exc)) from exc


@router.get("/database/info")
async def get_database_info() -> Dict:
    try:
        return DatabaseService.get_detailed_stats()
    except Exception as exc:
        raise HTTPException(500, str(exc)) from exc


@router.get("/database/export")
async def export_database() -> Dict:
    try:
        vectors, metadata = vector_db.load_vector_db()
        return {
            "metadata": metadata,
            "vectors_shape": list(vectors.shape) if vectors is not None else [0, 0],
            "vectors_sample": vectors[:5, :10].tolist() if vectors is not None else [],
        }
    except Exception as exc:
        raise HTTPException(500, str(exc)) from exc
