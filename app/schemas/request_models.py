"""
=============================================================================
MODULE: REQUEST_MODELS.PY
Purpose: Define Pydantic models for request data
=============================================================================

Pydantic models are used to:
- Validate input data from HTTP requests
- Automatically generate OpenAPI documentation
- Serialize/deserialize JSON data
"""

from pydantic import BaseModel, Field
from typing import Optional


class SearchQuery(BaseModel):
    """
    TODO: Model for search requests

    Attributes:
        query (str): The question or text to search for (required)
        top_k (int): Number of results to return (optional, default from config)
        threshold (float): Minimum similarity threshold (optional, default from config)

    Example JSON request:
    {
        "query": "How is the weather today?",
        "top_k": 5,
        "threshold": 0.5
    }
    """

    query: str = Field(
        ...,
        title="Search Query",
        description="The question or text to search for",
        min_length=1,
        max_length=10000
    )

    top_k: Optional[int] = Field(
        default=None,
        title="Top K",
        description="Number of results to return",
        ge=1,
        le=100
    )

    threshold: Optional[float] = Field(
        default=None,
        title="Similarity Threshold",
        description="Minimum similarity threshold (0-1)",
        ge=-1.0,
        le=1.0
    )


# TODO: Add other request models if needed (e.g., ClearDatabaseRequest)
