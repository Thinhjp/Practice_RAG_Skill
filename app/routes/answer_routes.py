from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.schemas import SearchQuery
from app.services.answer_service import AnswerService

router = APIRouter(prefix="/api/v1", tags=["RAG Answer"])


class AnswerSource(BaseModel):
    source_number: int
    chunk_id: int
    file_name: str
    similarity_score: float


class AnswerResponse(BaseModel):
    question: str
    answer: str
    sources: List[AnswerSource]
    generation_backend: str
    prompt: str


@router.post("/ask", response_model=AnswerResponse)
async def ask(query_data: SearchQuery):
    try:
        return AnswerService.answer(
            query_data.query, query_data.top_k, query_data.threshold
        )
    except Exception as exc:
        raise HTTPException(400, str(exc)) from exc
