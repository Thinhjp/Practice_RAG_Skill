"""
=============================================================================
MODULE: SEARCH_ROUTES.PY
Purpose: Endpoints for search functionality
=============================================================================

Routes:
- POST /api/v1/search - Find similar chunks
"""

from fastapi import APIRouter, HTTPException
from typing import List

from app.services import SearchService
from app.schemas import SearchQuery, SearchResult


# Tạo router cho search routes
router = APIRouter(
    prefix="/api/v1",
    tags=["Search"]
)


# ============================================================================
# ENDPOINT: Search
# ============================================================================
@router.post("/search", response_model=List[SearchResult])
async def search(query_data: SearchQuery):
    """
    TODO: Endpoint to search for similar chunks

    Process:
    1. Receive SearchQuery from the request body
    2. Call SearchService.search_chunks()
    3. Handle exceptions if any
    4. Return List[SearchResult]

    Example request:
    curl -X POST "http://localhost:8000/api/v1/search" \
         -H "Content-Type: application/json" \
         -d '{
             "query": "What is AI?",
             "top_k": 5,
             "threshold": 0.5
         }'

    Example response:
    [
        {
            "chunk_id": 0,
            "text": "AI is...",
            "source": "./data/uploads/document.pdf",
            "file_name": "document.pdf",
            "similarity_score": 0.95
        },
        ...
    ]

    Implementation suggestion:
    try:
        results = SearchService.search_chunks(
            query=query_data.query,
            top_k=query_data.top_k,
            threshold=query_data.threshold
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    """
    # Start coding here
    pass
