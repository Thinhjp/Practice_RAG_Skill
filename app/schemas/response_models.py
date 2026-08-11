"""
=============================================================================
MODULE: RESPONSE_MODELS.PY
Purpose: Define Pydantic models for response data
=============================================================================

Response models are used to:
- Format the output of API endpoints
- Validate responses before returning to clients
- Generate OpenAPI documentation
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class SearchResult(BaseModel):
    """
    TODO: Model for a search result

    Attributes:
        chunk_id (int): ID of the chunk
        text (str): Text content of the chunk
        source (str): File path of the source
        file_name (str): Name of the file
        similarity_score (float): Similarity score (0-1)
    """

    chunk_id: int = Field(
        ...,
        title="Chunk ID",
        description="Unique ID of the chunk"
    )

    text: str = Field(
        ...,
        title="Text",
        description="Text content of the chunk"
    )

    source: str = Field(
        ...,
        title="Source",
        description="File path of the source"
    )

    file_name: str = Field(
        ...,
        title="File Name",
        description="Original file name"
    )

    similarity_score: float = Field(
        ...,
        title="Similarity Score",
        description="Similarity score (0-1)",
        ge=0.0,
        le=1.0
    )


class UploadResponse(BaseModel):
    """
    TODO: Model for upload response

    Attributes:
        file_name (str): Name of the uploaded file
        chunks_count (int): Number of chunks created
        message (str): Result message
    """

    file_name: str = Field(
        ...,
        title="File Name",
        description="Name of the uploaded file"
    )

    chunks_count: int = Field(
        ...,
        title="Chunks Count",
        description="Number of chunks created",
        ge=0
    )

    message: str = Field(
        ...,
        title="Message",
        description="Result message"
    )


class FileInfo(BaseModel):
    """
    TODO: Model for file information in database stats
    """

    file_name: str = Field(
        ...,
        title="File Name",
        description="Name of the file"
    )

    chunk_count: int = Field(
        ...,
        title="Chunk Count",
        description="Number of chunks from this file"
    )


class DatabaseStats(BaseModel):
    """
    TODO: Model for database statistics response

    Attributes:
        total_chunks (int): Total number of chunks
        embedding_dim (int): Dimension of embedding vectors
        unique_files (int): Number of unique files
        files (List[FileInfo]): Detailed information about the files
    """

    total_chunks: int = Field(
        ...,
        title="Total Chunks",
        description="Total number of chunks in the database",
        ge=0
    )

    embedding_dim: int = Field(
        ...,
        title="Embedding Dimension",
        description="Dimension of the embedding vectors"
    )

    unique_files: int = Field(
        ...,
        title="Unique Files",
        description="Number of unique files in the database",
        ge=0
    )

    files: List[FileInfo] = Field(
        default=[],
        title="Files Info",
        description="Detailed information about the files"
    )


class HealthResponse(BaseModel):
    """
    TODO: Model for health check response

    Attributes:
        status (str): Application status
        app_name (str): Application name
        version (str): API version
    """

    status: str = Field(
        ...,
        title="Status",
        description="Application status"
    )

    app_name: str = Field(
        ...,
        title="App Name",
        description="Application name"
    )

    version: str = Field(
        ...,
        title="Version",
        description="API version"
    )


class ErrorResponse(BaseModel):
    """
    TODO: Model for error response
    """
