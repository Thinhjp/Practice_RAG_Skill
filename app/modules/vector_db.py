"""
=============================================================================
MODULE: VECTOR_DB.PY
Purpose: Store and manage the vector database (embeddings + metadata)
=============================================================================

INSTRUCTIONS:
1. Create the function load_vector_db() to load the database from disk
2. Create the function save_vector_db() to save the database to disk
3. Create the function add_to_vector_db() to add new chunks to the database
4. Create the function get_vector_db_stats() to retrieve database statistics
"""

from typing import List, Dict, Tuple
import numpy as np
import json
import os
from pathlib import Path

from app.config import config


# ============================================================================
# INITIALIZE AND MANAGE VECTOR DATABASE
# ============================================================================

class VectorDB:
    """
    TODO: Create the VectorDB class to manage embedding vectors and metadata

    Attributes:
        vectors (np.ndarray): Matrix containing all embeddings (n_chunks x embedding_dim)
        metadata (List[Dict]): List of metadata corresponding to vectors

    Suggested structure:
    def __init__(self):
        self.vectors = None  # np.ndarray or None if the database is empty
        self.metadata = []   # List of dicts containing chunk information

    def add_chunk(self, chunk_dict):
        # Add a chunk to the database

    def save(self, path):
        # Save vectors and metadata to disk

    def load(self, path):
        # Load vectors and metadata from disk

    def get_size(self):
        # Return the number of chunks in the database
    """
    # Start coding here
    pass

# ============================================================================
# STEP 1: LOAD VECTOR DATABASE
# ============================================================================

def load_vector_db(db_path: str = None) -> Tuple[np.ndarray, List[Dict]]:
    """
    TODO: Load vector database from disk (if it exists)

    Args:
        db_path (str): Path to the directory containing the database
                      Default: config.VECTOR_DB_PATH

    Returns:
        Tuple[np.ndarray, List[Dict]]: (vectors, metadata)
        - vectors: np.ndarray shape (n_chunks, embedding_dim) or None if empty
        - metadata: List[Dict] containing chunk information or [] if empty

    Example:
        vectors, metadata = load_vector_db()
        print(vectors.shape)  # (150, 384)
        print(len(metadata))  # 150

    Suggested implementation:
    - Use default value from config if db_path is None
    - Check if the directory db_path exists
    - Check if the files vectors.npy and metadata.json exist
    - If both exist: Load vectors using np.load(), load metadata using json.load()
    - If not exist: Return (None, [])
    - Return tuple (vectors, metadata)

    Note:
    - Should handle exceptions if the file is corrupted
    - Check if the sizes of vectors and metadata match
    """
    # Start coding here
    pass

# ============================================================================
# STEP 2: SAVE VECTOR DATABASE
# ============================================================================

def save_vector_db(vectors: np.ndarray, metadata: List[Dict], db_path: str = None) -> bool:
    """
    TODO: Save vector database to disk

    Args:
        vectors (np.ndarray): Matrix vectors shape (n_chunks, embedding_dim)
        metadata (List[Dict]): List of metadata corresponding
        db_path (str): Path to the directory containing the database
                      Default: config.VECTOR_DB_PATH

    Returns:
        bool: True if saved successfully, False if failed

    Example:
        success = save_vector_db(vectors, metadata)
        if success:
            print("Database saved successfully!")

    Suggested implementation:
    - Use default value from config if db_path is None
    - Create the directory db_path if it doesn't exist (os.makedirs)
    - Save vectors into file vectors.npy using np.save()
    - Save metadata into file metadata.json using json.dump()
    - Return True if successful
    - Return False and print error message if failed

    Note:
    - Ensure vectors and metadata have compatible sizes
    - Metadata that cannot be JSON serialized (like np.ndarray) needs to be handled
    """
    # Start coding here
    pass

# ============================================================================
# STEP 3: ADD NEW CHUNKS TO DATABASE
# ============================================================================

def add_to_vector_db(chunks: List[Dict], vectors: np.ndarray = None, 
                     metadata: List[Dict] = None) -> Tuple[np.ndarray, List[Dict]]:
    """
    TODO: Add new chunks to the vector database (or create a new one if empty)

    Args:
        chunks (List[Dict]): List of chunks to add
                            Each chunk must have fields:
                            - "embedding": np.ndarray
                            - "text": str
                            - "source": str
                            - "file_name": str
                            - ...other metadata fields
        vectors (np.ndarray): Vectors currently in the database (None if empty)
        metadata (List[Dict]): Metadata currently in the database ([] if empty)

    Returns:
        Tuple[np.ndarray, List[Dict]]: (updated_vectors, updated_metadata)

    Example:
        # First time
        vectors, metadata = add_to_vector_db(chunks1, None, None)

        # Again with new chunks
        vectors, metadata = add_to_vector_db(chunks2, vectors, metadata)

    Suggested implementation:
    - If vectors is None: initialize vectors = np.array([chunk["embedding"] for chunk in chunks])
    - If vectors is not None: concatenate vectors old and new
      * Get embeddings from chunks: new_embeddings = np.array([chunk["embedding"] for chunk in chunks])
      * Concatenate: vectors = np.vstack([vectors, new_embeddings])
    - Prepare metadata new (remove field "embedding" if exists)
    - Concatenate metadata old and new: metadata = metadata + new_metadata
    - Return (vectors, metadata)

    Note:
    - Handle the case of empty chunks
    - Ensure embeddings have compatible size with config.EMBEDDING_DIM
    """
    # Start coding here
    pass

# ============================================================================
# STEP 4: RETRIEVE VECTOR DATABASE STATISTICS
# ============================================================================

def get_vector_db_stats(vectors: np.ndarray = None, metadata: List[Dict] = None) -> Dict:
    """
    TODO: Retrieve statistics about the vector database

    Args:
        vectors (np.ndarray): Vectors currently (optional, if None will load from disk)
        metadata (List[Dict]): Metadata currently (optional, if None will load from disk)

    Returns:
        Dict: Statistics database in the form:
        {
            "total_chunks": 150,
            "embedding_dim": 384,
            "vector_shape": (150, 384),
            "unique_files": 3,
            "files": [
                {"file_name": "file1.pdf", "chunk_count": 50},
                {"file_name": "file2.pdf", "chunk_count": 60},
                {"file_name": "file3.pdf", "chunk_count": 40}
            ]
        }

    Example:
        stats = get_vector_db_stats()
        print(f"Total chunks: {stats['total_chunks']}")

    Suggested implementation:
    - If vectors is None, call load_vector_db() to load
    - Count total chunks: len(metadata)
    - Get embedding_dim from vectors.shape[1]
    - Group chunks by file_name to count chunks per file
    - Create dict containing information and return
    """
    # Start coding here
    pass
