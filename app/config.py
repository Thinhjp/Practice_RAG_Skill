"""
=============================================================================
MODULE: CONFIG.PY
Purpose: Manage common configuration for the entire RAG pipeline
=============================================================================
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# ============================================================================
# GENERAL CONFIGURATION
# ============================================================================
class Config:
    """
    Configuration class containing all necessary parameters for the RAG pipeline.
    
    TODO: Adjust these values according to your project requirements
    """
    
    # ========================================================================
    # APPLICATION CONFIGURATION
    # ========================================================================
    
    # Application name
    APP_NAME = "RAG Pipeline Backend"
    
    # API version
    API_VERSION = "1.0.0"
    
    # Debug mode (True = development, False = production)
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # ========================================================================
    # FILE UPLOAD CONFIGURATION
    # ========================================================================
    
    # Directory to store uploaded files
    UPLOAD_DIR = "./data/uploads"
    
    # Maximum file size (bytes) - 50MB
    MAX_FILE_SIZE = 50 * 1024 * 1024
    
    # Allowed file formats for upload
    ALLOWED_FILE_TYPES = [".pdf", ".txt", ".docx"]
    
    # ========================================================================
    # CHUNKING CONFIGURATION (TEXT SPLITTING)
    # ========================================================================
    
    # Chunk size (number of characters per chunk)
    # TODO: Adjust according to the length of user queries
    CHUNK_SIZE = 500
    
    # Overlap size between chunks (to ensure continuous context)
    # TODO: Increase if you want more overlapping context
    CHUNK_OVERLAP = 100
    
    # ========================================================================
    # EMBEDDING CONFIGURATION (TEXT EMBEDDING)
    # ========================================================================
    
    # Embedding vector size
    # TODO: You can use a different model with different dimensions (256, 384, 768, 1536...)
    EMBEDDING_DIM = 384
    
    # Embedding model used
    # TODO: Change to a different model if needed (all-MiniLM-L6-v2, text-embedding-3-small...)
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    
    # ========================================================================
    # VECTOR DATABASE CONFIGURATION
    # ========================================================================
    
    # Directory path for storing vector database
    VECTOR_DB_PATH = "./data/vector_db"
    
    # File name for storing vector database
    VECTOR_DB_FILE = "vectors.npy"
    
    # File name for storing metadata (information about chunks)
    METADATA_FILE = "metadata.json"
    
    # ========================================================================
    # SEARCH CONFIGURATION (RETRIEVAL)
    # ========================================================================
    
    # Maximum number of results to return
    MAX_RESULTS = 5
    
    # Minimum similarity threshold to return results
    # TODO: Adjust to filter out irrelevant results
    SIMILARITY_THRESHOLD = 0.5
    
    # Metric to measure similarity (cosine or euclidean)
    SIMILARITY_METRIC = "cosine"


# ============================================================================
# CREATE CONFIGURATION INSTANCE
# ============================================================================
config = Config()
