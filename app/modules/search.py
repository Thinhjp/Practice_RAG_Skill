"""
=============================================================================
MODULE: SEARCH.PY
Purpose: Search and retrieve relevant chunks from the vector database
=============================================================================

INSTRUCTIONS:
1. Create the function calculate_similarity() to compute similarity between vectors
2. Create the function search_similar_chunks() to find chunks similar to a query
3. Create the function retrieve_context() to get context around retrieved chunks
4. Create the function format_search_results() to format the search results
"""

from typing import List, Dict, Tuple
import numpy as np

from app.config import config
from app.modules.embedding import embed_text
from app.modules.vector_db import load_vector_db


# ============================================================================
# STEP 1: CALCULATE SIMILARITY BETWEEN VECTORS
# ============================================================================

def calculate_similarity(vector1: np.ndarray, vector2: np.ndarray, 
                        metric: str = "cosine") -> float:
    """
    TODO: Calculate similarity between two vectors

    Args:
        vector1 (np.ndarray): First vector (1D array)
        vector2 (np.ndarray): Second vector (1D array)
        metric (str): Similarity metric ("cosine" or "euclidean")
                     Default: "cosine"

    Returns:
        float: Similarity value (0-1 for cosine, or distance for euclidean)

    Example:
        vec1 = np.array([1, 2, 3])
        vec2 = np.array([1, 2, 3])
        sim = calculate_similarity(vec1, vec2)
        # Output: 1.0 (completely similar)

    Implementation suggestion:

    If metric == "cosine":
    - Cosine similarity = (A · B) / (||A|| * ||B||)
    - Code: sim = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    - Range: [0, 1]

    If metric == "euclidean":
    - Euclidean distance = sqrt(sum((A - B)^2))
    - Code: distance = np.linalg.norm(vector1 - vector2)
    - Smaller distance = more similar
    - Can convert to similarity: sim = 1 / (1 + distance)

    Notes:
    - Handle division by zero if vectors are zero
    - Optionally, add try-except
    """
    # Start coding here
    pass


# ============================================================================
# STEP 2: FIND MOST SIMILAR CHUNKS
# ============================================================================

def search_similar_chunks(query: str, vectors: np.ndarray = None, 
                         metadata: List[Dict] = None, 
                         top_k: int = None, 
                         threshold: float = None) -> List[Dict]:
    """
    TODO: Find top-k chunks most similar to a query

    Args:
        query (str): Query string or text to search
        vectors (np.ndarray): Vectors in the database (optional, will load from disk if None)
        metadata (List[Dict]): Metadata corresponding to vectors (optional, will load from disk if None)
        top_k (int): Number of results to return (default from config)
        threshold (float): Minimum similarity threshold (default from config)

    Returns:
        List[Dict]: List of similar chunks sorted by similarity score
        Each chunk has the form:
        {
            "chunk_id": 0,
            "text": "...",
            "source": "...",
            "file_name": "...",
            "similarity_score": 0.95
        }

    Example:
        results = search_similar_chunks("Hôm nay thời tiết như thế nào?", top_k=5)
        for result in results:
            print(f"{result['file_name']}: {result['similarity_score']:.3f}")
            print(f"  {result['text'][:100]}...")

    Process:
    1. Load vectors and metadata if not already loaded
    2. Embed query text
    3. Calculate similarity between query vector and all vectors
    4. Sort by similarity score descending
    5. Filter out results below threshold
    6. Take top_k results
    7. Format and return

    Implementation suggestion:
    - If vectors is None: vectors, metadata = load_vector_db()
    - query_vector = embed_text(query)
    - similarities = [calculate_similarity(query_vector, v) for v in vectors]
    - Create list of tuples (metadata, similarities)
    - Sort by similarity score descending
    - Filter by threshold
    - Return top_k

    Notes:
    - Handle empty database
    - Handle empty query
    """
    # Start coding here
    pass


# ============================================================================
# STEP 3: RETRIEVE CONTEXT AROUND CHUNKS (OPTIONAL)
# ============================================================================

def retrieve_context(chunk_id: int, metadata: List[Dict], 
                    context_size: int = 2) -> Dict:
    """
    TODO: Retrieve context around a chunk

    Args:
        chunk_id (int): ID of the chunk to retrieve context
        metadata (List[Dict]): List of metadata
        context_size (int): Number of chunks before/after to retrieve (default: 2)

    Returns:
        Dict: Context including chunks before and after
        {
            "main_chunk": {...},
            "context_before": [...],
            "context_after": [...]
        }

    Example:
        context = retrieve_context(chunk_id=50, metadata=metadata, context_size=2)
        # Will take chunks 48, 49 (before) + chunk 50 (main) + chunks 51, 52 (after)

    Implementation suggestion:
    - Check if chunk_id is valid
    - Take the main chunk at position chunk_id
    - Take context chunks before: from max(0, chunk_id - context_size) to chunk_id - 1
    - Take context chunks after: from chunk_id + 1 to min(len(metadata), chunk_id + context_size + 1)
    - Return dict with 3 keys: main_chunk, context_before, context_after
    """
    # Start coding here
    pass


# ============================================================================
# STEP 4: FORMAT SEARCH RESULTS
# ============================================================================

def format_search_results(results: List[Dict], include_scores: bool = True) -> List[Dict]:
    """
    TODO: Format search results before returning to client

    Args:
        results (List[Dict]): List of results from search_similar_chunks()
        include_scores (bool): Return similarity_score or not (default: True)

    Returns:
        List[Dict]: Formatted results, each item includes:
        {
            "chunk_id": 0,
            "text": "...",
            "source": "...",
            "file_name": "...",
            "similarity_score": 0.95  (optional)
        }

    Example:
        results = search_similar_chunks("query")
        formatted = format_search_results(results, include_scores=True)

    Implementation suggestion:
    - Loop through results
    - Keep only the fields needed
    - Round similarity_score to 3-4 decimal places if include_scores=True
    - Optionally, truncate text if too long (e.g., k=500 characters + "...")
    - Return formatted list

    Notes:
    - Customize fields returned based on frontend needs
    - Can add more fields if needed
    """
    # Start coding here
    pass
