from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.modules import chunking, embedding, search

router = APIRouter(prefix="/api/v1/test", tags=["Testing"])


class ChunkingTestRequest(BaseModel):
    text: str = Field(min_length=1, max_length=100000)
    method: str = "simple"
    chunk_size: Optional[int] = Field(default=None, gt=0)
    overlap: Optional[int] = Field(default=None, ge=0)


class ChunkingTestResponse(BaseModel):
    total_chunks: int
    chunks: List[Dict]


class EmbeddingTestRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10000)


class EmbeddingTestResponse(BaseModel):
    text: str
    embedding_dim: int
    embedding_sample: List[float]


class SearchTestRequest(BaseModel):
    query: str = Field(min_length=1, max_length=10000)
    top_k: int = Field(default=5, ge=1, le=50)


@router.post("/chunking", response_model=ChunkingTestResponse)
async def test_chunking(request: ChunkingTestRequest):
    try:
        methods = {
            "simple": chunking.split_text_simple,
            "sentence": chunking.split_text_by_sentences,
            "paragraph": chunking.split_text_by_paragraphs,
        }
        splitter = methods[request.method.lower()]
        pieces = splitter(request.text, request.chunk_size, request.overlap)
        chunks = chunking.add_chunk_metadata(pieces, "test", "test.txt")
        return ChunkingTestResponse(total_chunks=len(chunks), chunks=chunks[:10])
    except (KeyError, ValueError) as exc:
        raise HTTPException(400, str(exc)) from exc


@router.post("/embedding", response_model=EmbeddingTestResponse)
async def test_embedding(request: EmbeddingTestRequest):
    try:
        vector = embedding.embed_text(request.text)
        return EmbeddingTestResponse(
            text=request.text,
            embedding_dim=len(vector),
            embedding_sample=vector[:10].tolist(),
        )
    except Exception as exc:
        raise HTTPException(400, str(exc)) from exc


@router.post("/search")
async def test_search(request: SearchTestRequest):
    try:
        results = search.search_similar_chunks(query=request.query, top_k=request.top_k)
        return {"query": request.query, "total_results": len(results), "results": results}
    except Exception as exc:
        raise HTTPException(400, str(exc)) from exc
