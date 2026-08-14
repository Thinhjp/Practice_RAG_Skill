"""
Khởi tạo package routes - Chứa các HTTP endpoints
"""
from .upload_routes import router as upload_router
from .search_routes import router as search_router
from .database_routes import router as database_router
from .health_routes import router as health_router
from .test_routes import router as test_router
from .chunks_routes import router as chunks_router
from .embeddings_routes import router as embeddings_router
from .answer_routes import router as answer_router

__all__ = [
    'upload_router',
    'search_router',
    'database_router',
    'health_router',
    'test_router',
    'chunks_router',
    'embeddings_router',
    'answer_router'
]
