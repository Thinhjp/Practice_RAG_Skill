"""
=============================================================================
MODULE: TEST_ROUTES.PY
Purpose: Endpoints to test modules (chunking, embedding, search)
=============================================================================

Routes:
- POST /api/v1/test/chunking - Test splitting text into chunks
- POST /api/v1/test/embedding - Test embedding text
- POST /api/v1/test/search - Test search functionality
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

from app.modules import chunking, embedding, search


# Tạo router cho test routes
router = APIRouter(
    prefix="/api/v1/test",
    tags=["Testing"]
)


# ============================================================================
# MODELS
# ============================================================================

class ChunkingTestRequest(BaseModel):
    """Request model for chunking test"""
    text: str = Field(
        ...,
        title="Text",
        description="Text to split into chunks",
        min_length=1,
        max_length=100000
    )
    method: str = Field(
        default="simple",
        title="Method",
        description="Splitting method ('simple', 'sentence', 'paragraph')"
    )
    chunk_size: Optional[int] = Field(
        default=None,
        title="Chunk Size",
        description="Size of each chunk (default from config)"
    )
    overlap: Optional[int] = Field(
        default=None,
        title="Overlap",
        description="Overlap size (default from config)"
    )

class ChunkingTestResponse(BaseModel):
    """Response model for chunking test"""
    total_chunks: int
    chunks: List[Dict]

class EmbeddingTestRequest(BaseModel):
    """Request model for embedding test"""
    text: str = Field(
        ...,
        title="Text",
        description="Text to embed",
        min_length=1,
        max_length=10000
    )

class EmbeddingTestResponse(BaseModel):
    """Response model for embedding test"""
    text: str
    embedding_dim: int
    embedding_sample: List[float] = Field(
        ...,
        title="Embedding Sample",
        description="First 10 values of the embedding vector"
    )

# ============================================================================
# ENDPOINT 1: Test Chunking
# ============================================================================

@router.post("/chunking", response_model=ChunkingTestResponse)
async def test_chunking(request: ChunkingTestRequest):
    """
    TODO: Endpoint to test splitting text into chunks

    Implementation suggestion:
    try:
        chunks = chunking.prepare_chunks(
            text=request.text,
            source="test",
            file_name="test.txt",
            method=request.method
        )

        return ChunkingTestResponse(
            total_chunks=len(chunks),
            chunks=chunks[:10]  # Return first 10 chunks
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    """
    # Start coding here
    pass

# ============================================================================
# ENDPOINT 2: Test Embedding
# ============================================================================

@router.post("/embedding", response_model=EmbeddingTestResponse)
async def test_embedding(request: EmbeddingTestRequest):
    """
    TODO: Endpoint to test embedding text

    Implementation suggestion:
    try:
        vector = embedding.embed_text(request.text)

        return EmbeddingTestResponse(
            text=request.text,
            embedding_dim=len(vector),
            embedding_sample=vector[:10].tolist()
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    """
    # Start coding here
    pass

# ============================================================================
# ENDPOINT 3: Test Search
# ============================================================================

class SearchTestRequest(BaseModel):
    """Request model for search test"""
    query: str = Field(
        ...,
        title="Query",
        description="Query to search for",
        min_length=1,
        max_length=10000
    )
    top_k: Optional[int] = Field(
        default=5,
        title="Top K",
        description="Number of results",
        ge=1,
        le=50
    )

@router.post("/search")
async def test_search(request: SearchTestRequest):
    """
    TODO: Endpoint to test search functionality

    Implementation suggestion:
    try:
        results = search.search_similar_chunks(
            query=request.query,
            top_k=request.top_k
        )

        return {
            "query": request.query,
            "total_results": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    """
    # Start coding here
    pass
