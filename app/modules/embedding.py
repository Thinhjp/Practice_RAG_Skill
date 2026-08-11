"""
=============================================================================
MODULE: EMBEDDING.PY
Purpose: Generate vector embeddings from text chunks
=============================================================================

INSTRUCTIONS:
1. Initialize the embedding model (SentenceTransformer)
2. Create the function embed_text() to convert text into vectors
3. Create the function embed_chunks() to generate embeddings for a list of chunks
4. Create the function normalize_embeddings() to normalize vectors (optional)
"""

from typing import List, Dict
import numpy as np

from app.config import config

# TODO: Import SentenceTransformer
# from sentence_transformers import SentenceTransformer


# ============================================================================
# STEP 1: INITIALIZE EMBEDDING MODEL
# ============================================================================

# TODO: Declare a global variable for the embedding model to enable lazy loading
# embedding_model = None

def initialize_embedder():
    """
    TODO: Initialize the embedding model (lazy loading)

    Implementation suggestion:
    - Declare a global embedding_model
    - Check if embedding_model is None
    - Load the model using SentenceTransformer(config.EMBEDDING_MODEL)
    - Optionally, add try-except to handle errors

    Example:
        global embedding_model
        if embedding_model is None:
            embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
        return embedding_model
    """
    # Start coding here
    pass


# ============================================================================
# STEP 2: EMBED A SINGLE TEXT
# ============================================================================

def embed_text(text: str) -> np.ndarray:
    """
    TODO: Convert a text segment into an embedding vector

    Args:
        text (str): Text to embed

    Returns:
        np.ndarray: Embedding vector (1D array)

    Example:
        text = "Hello, this is a text to embed"
        vector = embed_text(text)
        # Output: array([0.1234, -0.5678, 0.9012, ...]) with size EMBEDDING_DIM

    Implementation suggestion:
    - Call initialize_embedder() to get the model
    - Use model.encode(text) to generate the embedding
    - Optionally, convert to a numpy array
    - Return the vector

    Notes:
    - Ensure the text is not empty; if empty, return a zero vector
    - Handle errors if the text is too long
    """
    # Start coding here
    pass


# ============================================================================
# STEP 3: EMBED A LIST OF CHUNKS
# ============================================================================

def embed_chunks(chunks: List[Dict]) -> List[Dict]:
    """
    TODO: Generate embeddings for all chunks in the list

    Args:
        chunks (List[Dict]): List of chunks from the chunking module
                            Each chunk has the format:
                            {
                                "chunk_id": 0,
                                "text": "...",
                                "source": "...",
                                "file_name": "..."
                            }

    Returns:
        List[Dict]: List of chunks with an additional "embedding" field
                   {
                       "chunk_id": 0,
                       "text": "...",
                       "source": "...",
                       "file_name": "...",
                       "embedding": [0.1234, -0.5678, ...]  # numpy array
                   }

    Example:
        chunks = [
            {"chunk_id": 0, "text": "Text 1", "source": "file.pdf", "file_name": "file.pdf"},
            {"chunk_id": 1, "text": "Text 2", "source": "file.pdf", "file_name": "file.pdf"}
        ]
        result = embed_chunks(chunks)
        # result[0]["embedding"] will be the vector for "Text 1"

    Implementation suggestion:
    - Extract the list of texts from chunks (extract "text" field)
    - Use SentenceTransformer.encode() with the list for batch processing
    - Iterate over chunks and embeddings to assign embeddings to each chunk
    - Return chunks with the additional "embedding" field

    Notes:
    - Batch processing is faster than looping
    - Optionally, use convert_to_numpy=True in encode()
    """
    # Start coding here
    pass


# ============================================================================
# STEP 4: NORMALIZE EMBEDDINGS (OPTIONAL)
# ============================================================================

def normalize_embeddings(chunks: List[Dict]) -> List[Dict]:
    """
    TODO: Normalize embedding vectors (L2 normalization) - optional

    Args:
        chunks (List[Dict]): List of chunks with embeddings

    Returns:
        List[Dict]: List of chunks with normalized embeddings

    Example:
        Normalization helps cosine similarity calculations as it becomes
        equivalent to the dot product of two normalized vectors.

    Implementation suggestion:
    - Iterate over chunks
    - Retrieve the embedding of each chunk
    - Compute the L2 norm: norm = sqrt(sum(x^2))
    - Divide each element by the norm
    - Update the embedding in the chunk

    Formula for L2 normalization:
        x_normalized = x / ||x||
        In numpy: x / np.linalg.norm(x)
    """
    # Start coding here
    pass
