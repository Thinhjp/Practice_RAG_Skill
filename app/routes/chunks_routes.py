from typing import Optional

import numpy as np
from fastapi import APIRouter, HTTPException, Query

from app.modules import search, vector_db

router = APIRouter(prefix="/api/v1/chunks", tags=["Chunks Management"])


@router.get("")
async def get_all_chunks(
    file_name: Optional[str] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    try:
        _, metadata = vector_db.load_vector_db()
        filtered = (
            [item for item in metadata if item.get("file_name") == file_name]
            if file_name
            else metadata
        )
        chunks = filtered[offset : offset + limit]
        return {
            "total": len(filtered),
            "offset": offset,
            "limit": limit,
            "count": len(chunks),
            "chunks": chunks,
        }
    except Exception as exc:
        raise HTTPException(400, str(exc)) from exc


@router.get("/search/{query}")
async def search_chunks(
    query: str,
    top_k: int = Query(5, ge=1, le=50),
    threshold: float = Query(0.0, ge=-1, le=1),
):
    try:
        results = search.format_search_results(
            search.search_similar_chunks(query=query, top_k=top_k, threshold=threshold)
        )
        return {"query": query, "results_count": len(results), "results": results}
    except Exception as exc:
        raise HTTPException(400, str(exc)) from exc


@router.get("/{chunk_id}")
async def get_chunk_detail(chunk_id: int):
    try:
        _, metadata = vector_db.load_vector_db()
        chunk = next((item for item in metadata if item.get("chunk_id") == chunk_id), None)
        if chunk is None:
            raise HTTPException(404, "Chunk not found")
        return chunk
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(400, str(exc)) from exc


@router.delete("/{chunk_id}")
async def delete_chunk(chunk_id: int):
    try:
        vectors, metadata = vector_db.load_vector_db()
        index = next(
            (i for i, item in enumerate(metadata) if item.get("chunk_id") == chunk_id),
            None,
        )
        if index is None or vectors is None:
            raise HTTPException(404, "Chunk not found")
        updated_vectors = np.delete(vectors, index, axis=0)
        updated_metadata = [*metadata[:index], *metadata[index + 1 :]]
        vector_db.save_vector_db(updated_vectors, updated_metadata)
        return {"status": "success", "message": f"Deleted chunk {chunk_id}"}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(400, str(exc)) from exc
