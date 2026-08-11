"""
=============================================================================
MODULE: EMBEDDINGS_ROUTES.PY
Purpose: Endpoints to view information about embeddings
=============================================================================

Routes:
- GET /api/v1/embeddings/stats - Retrieve statistics about embeddings
- GET /api/v1/embeddings/sample - Retrieve sample embeddings
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List, Optional

from app.modules import vector_db
import numpy as np


# Create router for embeddings routes
router = APIRouter(
    prefix="/api/v1/embeddings",
    tags=["Embeddings"]
)

# ============================================================================
# ENDPOINT 1: Retrieve embeddings statistics
# ============================================================================

@router.get("/stats")
async def get_embeddings_stats():
    """
    TODO: Endpoint to retrieve statistics about embeddings in the database

    Example:
    GET /api/v1/embeddings/stats

    Response:
    {
        "total_embeddings": 150,
        "embedding_dimension": 384,
        "vector_shape": [150, 384],
        "memory_usage_mb": 0.22,
        "average_norm": 1.0
    }

    Implementation suggestion:
    try:
        vectors, metadata = vector_db.load_vector_db()

        if vectors is None or len(metadata) == 0:
            raise HTTPException(status_code=404, detail="No embeddings found")

        # Calculate statistics
        avg_norm = np.mean([np.linalg.norm(v) for v in vectors])
        memory_size = vectors.nbytes / (1024 * 1024)  # Convert to MB

        return {
            "total_embeddings": len(vectors),
            "embedding_dimension": vectors.shape[1],
            "vector_shape": list(vectors.shape),
            "memory_usage_mb": round(memory_size, 3),
            "average_norm": round(float(avg_norm), 4)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    """
    # Start coding here
    pass

# ============================================================================
# ENDPOINT 2: Retrieve sample embeddings
# ============================================================================

@router.get("/sample")
async def get_embeddings_sample(count: int = Query(5, ge=1, le=20, description="Number of samples")):
    """
    TODO: Endpoint to retrieve sample embeddings from the database

    Query parameters:
    - count: Number of embedding samples (default: 5, max: 20)

    Example:
    GET /api/v1/embeddings/sample?count=10

    Response:
    {
        "count": 10,
        "samples": [
            {
                "chunk_id": 0,
                "file_name": "document.pdf",
                "embedding_sample": [0.1234, -0.5678, ...],  # First 5 values
                "norm": 1.0
            },
            ...
        ]
    }

    Implementation suggestion:
    try:
        vectors, metadata = vector_db.load_vector_db()

        if vectors is None or len(metadata) == 0:
            raise HTTPException(status_code=404, detail="No embeddings found")

        # Random sample or first N
        indices = np.random.choice(len(vectors), min(count, len(vectors)), replace=False)

        samples = []
        for idx in indices:
            vector = vectors[idx]
            samples.append({
                "chunk_id": metadata[idx].get("chunk_id"),
                "file_name": metadata[idx].get("file_name"),
                "embedding_sample": vector[:5].tolist(),  # First 5 values
                "norm": float(np.linalg.norm(vector))
            })

        return {
            "count": len(samples),
            "samples": samples
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    """
    # Start coding here
    pass

# ============================================================================
# ENDPOINT 3: Comparing two embeddings (optional)
# ============================================================================

@router.get("/compare/{chunk_id1}/{chunk_id2}")
async def compare_embeddings(chunk_id1: int, chunk_id2: int):
    """
    TODO: Endpoint to compare two embeddings

    Example:
    GET /api/v1/embeddings/compare/5/10

    Response:
    {
        "chunk_id1": 5,
        "chunk_id2": 10,
        "cosine_similarity": 0.85,
        "euclidean_distance": 0.523
    }

    Implementation suggestion:
    from app.modules import search
    try:
        vectors, metadata = vector_db.load_vector_db()

        if chunk_id1 >= len(vectors) or chunk_id2 >= len(vectors):
            raise HTTPException(status_code=404, detail="Chunk not found")

        cosine_sim = search.calculate_similarity(vectors[chunk_id1], vectors[chunk_id2], "cosine")
        euclidean_sim = search.calculate_similarity(vectors[chunk_id1], vectors[chunk_id2], "euclidean")

        return {
            "chunk_id1": chunk_id1,
            "chunk_id2": chunk_id2,
            "cosine_similarity": round(cosine_sim, 4),
            "euclidean_distance": round(euclidean_sim, 4)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    """
    # Start coding here
    pass
