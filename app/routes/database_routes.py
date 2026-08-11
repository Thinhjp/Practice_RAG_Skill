"""
=============================================================================
MODULE: DATABASE_ROUTES.PY
Purpose: Endpoints for managing the vector database
=============================================================================

Routes:
- GET /api/v1/stats - Retrieve database statistics
- DELETE /api/v1/database - Delete the database (optional)
"""

from fastapi import APIRouter, HTTPException
from typing import Dict

from app.services import DatabaseService
from app.schemas import DatabaseStats


# Tạo router cho database routes
router = APIRouter(
    prefix="/api/v1",
    tags=["Database"]
)


# ============================================================================
# ENDPOINT: Retrieve database statistics
# ============================================================================

@router.get("/stats", response_model=DatabaseStats)
async def get_database_stats() -> DatabaseStats:
    """
    TODO: Endpoint to retrieve database statistics

    Process:
    1. Call DatabaseService.get_stats()
    2. Convert to DatabaseStats response
    3. Return to client

    Example request:
    curl "http://localhost:8000/api/v1/stats"

    Example response:
    {
        "total_chunks": 150,
        "embedding_dim": 384,
        "unique_files": 3,
        "files": [
            {"file_name": "doc1.pdf", "chunk_count": 50},
            {"file_name": "doc2.pdf", "chunk_count": 60},
            {"file_name": "doc3.pdf", "chunk_count": 40}
        ]
    }

    Implementation suggestion:
    try:
        stats = DatabaseService.get_stats()
        return DatabaseStats(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    """
    # Start coding here
    pass


# ============================================================================
# ENDPOINT: Delete the database (OPTIONAL)
# ============================================================================

@router.delete("/database")
async def clear_database() -> Dict[str, str]:
    """
    TODO: Endpoint to delete the entire vector database

    ⚠️ WARNING: This action cannot be undone!

    Process:
    1. Call DatabaseService.clear_database()
    2. Handle exceptions if any
    3. Return confirmation

    Example request:
    curl -X DELETE "http://localhost:8000/api/v1/database"

    Example response:
    {
        "message": "Database cleared successfully",
        "status": "success"
    }

    Implementation suggestion:
    try:
        result = DatabaseService.clear_database()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    """
    # Start coding here
    pass


# ============================================================================
# ENDPOINT 3: Retrieve detailed database information
# ============================================================================

@router.get("/database/info")
async def get_database_info() -> Dict:
    """
    TODO: Endpoint to retrieve detailed database information

    Example:
    GET /api/v1/database/info

    Response:
    {
        "database_path": "./data/vector_db",
        "vectors_file": "vectors.npy",
        "metadata_file": "metadata.json",
        "database_exists": true,
        "size_mb": 0.22
    }
    """
    # Start coding here
    pass


# ============================================================================
# ENDPOINT 4: Export database (optional)
# ============================================================================

@router.get("/database/export")
async def export_database() -> Dict:
    """
    TODO: Endpoint to export the database as a dictionary (for backup/restore)

    Response:
    {
        "metadata": [...],
        "vectors_shape": [150, 384],
        "vectors_sample": [[0.1, 0.2, ...], ...]
    }
    """
    # Start coding here
    pass
