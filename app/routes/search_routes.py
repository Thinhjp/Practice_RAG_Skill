from typing import List

from fastapi import APIRouter, HTTPException

from app.schemas import SearchQuery, SearchResult
from app.services import SearchService

router = APIRouter(prefix="/api/v1", tags=["Search"])


@router.post("/search", response_model=List[SearchResult])
async def search(query_data: SearchQuery):
    try:
        return SearchService.search_chunks(
            query=query_data.query,
            top_k=query_data.top_k,
            threshold=query_data.threshold,
        )
    except Exception as exc:
        raise HTTPException(400, str(exc)) from exc
