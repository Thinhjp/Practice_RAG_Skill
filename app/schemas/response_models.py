"""Pydantic response contracts for the HTTP API."""

from typing import List, Optional

from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    chunk_id: int
    document_id: Optional[str] = None
    chunk_index: Optional[int] = None
    text: str
    source: str
    file_name: str
    length: Optional[int] = None
    similarity_score: float = Field(ge=-1.0, le=1.0)


class UploadResponse(BaseModel):
    file_name: str
    chunks_count: int = Field(ge=0)
    message: str


class FileInfo(BaseModel):
    file_name: str
    chunk_count: int = Field(ge=0)


class DatabaseStats(BaseModel):
    total_chunks: int = Field(ge=0)
    embedding_dim: int = Field(ge=0)
    unique_files: int = Field(ge=0)
    files: List[FileInfo] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str


class ErrorResponse(BaseModel):
    detail: str
