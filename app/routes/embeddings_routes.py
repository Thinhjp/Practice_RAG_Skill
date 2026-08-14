import numpy as np
from fastapi import APIRouter, HTTPException, Query

from app.modules import search, vector_db

router = APIRouter(prefix="/api/v1/embeddings", tags=["Embeddings"])


@router.get("/stats")
async def get_embeddings_stats():
    vectors, metadata = vector_db.load_vector_db()
    if vectors is None or not metadata:
        raise HTTPException(404, "No embeddings found")
    return {
        "total_embeddings": len(vectors),
        "embedding_dimension": vectors.shape[1],
        "vector_shape": list(vectors.shape),
        "memory_usage_mb": round(vectors.nbytes / (1024 * 1024), 4),
        "average_norm": round(float(np.mean(np.linalg.norm(vectors, axis=1))), 6),
    }


@router.get("/sample")
async def get_embeddings_sample(count: int = Query(5, ge=1, le=20)):
    vectors, metadata = vector_db.load_vector_db()
    if vectors is None or not metadata:
        raise HTTPException(404, "No embeddings found")
    indices = range(min(count, len(vectors)))
    samples = [
        {
            "chunk_id": metadata[index].get("chunk_id"),
            "file_name": metadata[index].get("file_name"),
            "embedding_sample": vectors[index, :5].tolist(),
            "norm": float(np.linalg.norm(vectors[index])),
        }
        for index in indices
    ]
    return {"count": len(samples), "samples": samples}


@router.get("/compare/{chunk_id1}/{chunk_id2}")
async def compare_embeddings(chunk_id1: int, chunk_id2: int):
    vectors, metadata = vector_db.load_vector_db()
    if vectors is None:
        raise HTTPException(404, "No embeddings found")
    positions = {item.get("chunk_id"): index for index, item in enumerate(metadata)}
    if chunk_id1 not in positions or chunk_id2 not in positions:
        raise HTTPException(404, "Chunk not found")
    first, second = vectors[positions[chunk_id1]], vectors[positions[chunk_id2]]
    return {
        "chunk_id1": chunk_id1,
        "chunk_id2": chunk_id2,
        "cosine_similarity": round(search.calculate_similarity(first, second), 6),
        "euclidean_distance": round(float(np.linalg.norm(first - second)), 6),
    }
