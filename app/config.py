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
    
    # Allowed file formats. The actual format is verified from the file bytes;
    # the extension is only the first upload gate.
    ALLOWED_FILE_TYPES = [
        ".txt", ".md", ".csv", ".json", ".xml", ".html", ".htm",
        ".pdf", ".docx", ".xlsx", ".pptx",
        ".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff",
    ]

    # Canonical HTML produced by Gemini is cached here.
    NORMALIZED_DIR = os.getenv("NORMALIZED_DIR", "./data/normalized")

    # Local extraction quality. Text-oriented formats only need non-empty text;
    # document formats use these thresholds before an LLM fallback is selected.
    MIN_NATIVE_TEXT_CHARS = int(os.getenv("MIN_NATIVE_TEXT_CHARS", "80"))
    MIN_PAGE_TEXT_CHARS = int(os.getenv("MIN_PAGE_TEXT_CHARS", "40"))
    MIN_TEXT_PAGE_COVERAGE = float(os.getenv("MIN_TEXT_PAGE_COVERAGE", "0.7"))
    MIN_PRINTABLE_RATIO = float(os.getenv("MIN_PRINTABLE_RATIO", "0.85"))

    # Gemini Interactions API. gemini-3.5-flash-lite currently has a free tier
    # and is optimized for high-volume document extraction.
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    GEMINI_API_URL = os.getenv(
        "GEMINI_API_URL",
        "https://generativelanguage.googleapis.com/v1beta/interactions",
    )
    GEMINI_TIMEOUT_SECONDS = float(os.getenv("GEMINI_TIMEOUT_SECONDS", "90"))
    GEMINI_MAX_RETRIES = int(os.getenv("GEMINI_MAX_RETRIES", "2"))
    GEMINI_INLINE_MAX_BYTES = int(
        os.getenv("GEMINI_INLINE_MAX_BYTES", str(20 * 1024 * 1024))
    )
    
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
    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    # "sentence_transformers" provides semantic multilingual embeddings.
    # "hashing" is deterministic, local and useful for fast/offline practice.
    EMBEDDING_BACKEND = os.getenv("EMBEDDING_BACKEND", "hashing")
    
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
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.3"))
    
    # Metric to measure similarity (cosine or euclidean)
    SIMILARITY_METRIC = "cosine"

    # Runnable baseline. Replace AnswerService's extractive generator with an
    # LLM provider when API credentials are available.
    GENERATION_BACKEND = os.getenv("GENERATION_BACKEND", "extractive")


# ============================================================================
# CREATE CONFIGURATION INSTANCE
# ============================================================================
config = Config()
