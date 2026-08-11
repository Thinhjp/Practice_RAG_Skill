"""
=============================================================================
MODULE: CHUNKS_ROUTES.PY
Purpose: Endpoints to manage and view chunks from the database
=============================================================================

Routes:
- GET /api/v1/chunks - Retrieve a list of all chunks
- GET /api/v1/chunks/{chunk_id} - Retrieve details of a specific chunk
- DELETE /api/v1/chunks/{chunk_id} - Delete a specific chunk
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Optional

from app.modules import vector_db


# Tạo router cho chunks routes
router = APIRouter(
    prefix="/api/v1/chunks",
    tags=["Chunks Management"]
)


# ============================================================================
# ENDPOINT 1: Retrieve a list of all chunks
# ============================================================================

@router.get("")
async def get_all_chunks(
    file_name: Optional[str] = Query(None, description="Filter by file name"),
    offset: int = Query(0, ge=0, description="Offset (pagination)"),
    limit: int = Query(10, ge=1, le=100, description="Number of chunks to return")
):
    """
    TODO: Endpoint to retrieve a list of chunks with pagination

    Query parameters:
    - file_name: Filter chunks by file (optional)
    - offset: Starting position (default: 0)
    - limit: Number of chunks to return (default: 10, max: 100)

    Example:
    GET /api/v1/chunks?file_name=document.pdf&offset=0&limit=20

    Implementation suggestion:
    try:
        vectors, metadata = vector_db.load_vector_db()

        if not metadata:
            return {"total": 0, "chunks": []}

        # Filter by file_name if provided
        filtered = metadata
        if file_name:
            filtered = [m for m in metadata if m.get("file_name") == file_name]

        # Pagination
        total = len(filtered)
        chunks = filtered[offset:offset+limit]

        return {
            "total": total,
            "offset": offset,
            "limit": limit,
            "count": len(chunks),
            "chunks": chunks
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    """
    # Start coding here
    pass


# ============================================================================
# ENDPOINT 2: Retrieve details of a specific chunk
# ============================================================================

@router.get("/{chunk_id}")
async def get_chunk_detail(chunk_id: int):
    """
    TODO: Endpoint to retrieve details of a specific chunk

    Example:
    GET /api/v1/chunks/5

    Response:
    {
        "chunk_id": 5,
        "text": "...",
        "source": "...",
        "file_name": "...",
        "length": 450
    }

    Implementation suggestion:
    try:
        vectors, metadata = vector_db.load_vector_db()

        if chunk_id < 0 or chunk_id >= len(metadata):
            raise HTTPException(status_code=404, detail="Chunk not found")

        chunk = metadata[chunk_id]
        return chunk
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    """
    # Start coding here
    pass


# ============================================================================
# ENDPOINT 3: Search chunks
# ============================================================================

@router.get("/search/{query}")
async def search_chunks(
    query: str,
    top_k: int = Query(5, ge=1, le=50, description="Number of results"),
    threshold: float = Query(0.0, ge=0, le=1, description="Similarity threshold")
):
    """
    TODO: Endpoint to search for chunks similar to the query

    Query parameters:
    - query: Text to search
    - top_k: Number of results (default: 5)
    - threshold: Similarity threshold (default: 0.0)

    Example:
    GET /api/v1/chunks/search/AI?top_k=10&threshold=0.5

    Implementation suggestion:
    from app.modules import search

    try:
        results = search.search_similar_chunks(
            query=query,
            top_k=top_k,
            threshold=threshold
        )

        return {
            "query": query,
            "top_k": top_k,
            "results_count": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    """
    # Start coding here
    pass


# ============================================================================
# ENDPOINT 4: Delete a chunk (optional)
# ============================================================================

@router.delete("/{chunk_id}")
async def delete_chunk(chunk_id: int):
    """
    TODO: Endpoint to delete a specific chunk (optional)

    ⚠️ Warning: Deleting a chunk requires rebuilding the vector matrix,
    which is complex. It could be simplified by deleting the entire database
    and rebuilding.

    Implementation suggestion: Could be skipped or implemented later.
    """
    # Start coding here
    pass
