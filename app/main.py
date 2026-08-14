"""
=============================================================================
MODULE: MAIN.PY
Purpose: Main FastAPI application - combines all routes and starts the server
=============================================================================

Structure after refactoring:
- app/main.py: Initialize FastAPI app, import routes
- app/schemas/: Pydantic models (request/response)
- app/services/: Business logic
- app/routes/: API endpoints
- app/modules/: RAG pipeline logic

Benefits:
✓ Code is easy to maintain
✓ Easy to test individual components
✓ Easy to extend with new routes
✓ Clear separation of concerns
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import config
from app.routes import (
    upload_router,
    search_router,
    database_router,
    health_router,
    test_router,
    chunks_router,
    embeddings_router,
    answer_router
)


# ============================================================================
# INITIALIZE FASTAPI APP
# ============================================================================

app = FastAPI(
    title=config.APP_NAME,
    version=config.API_VERSION,
    description="RAG Pipeline Backend - Intelligent search system based on vector embeddings",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# ============================================================================
# CORS CONFIGURATION (OPTIONAL)
# ============================================================================

# TODO: If frontend runs on a different domain, enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Or ["http://localhost:3000", ...]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# ============================================================================
# REGISTER ROUTES
# ============================================================================

# TODO: Add routes to the app
# Method 1: Include routers from routes/
app.include_router(upload_router)
app.include_router(search_router)
app.include_router(database_router)
app.include_router(health_router)
app.include_router(test_router)
app.include_router(chunks_router)
app.include_router(embeddings_router)
app.include_router(answer_router)


# ============================================================================
# ROOT ENDPOINT (TÙY CHỌN)
# ============================================================================

@app.get("/")
async def root():
    return FileResponse(STATIC_DIR / "index.html")



# ============================================================================
# KHỞI ĐỘNG SERVER
# ============================================================================


# ============================================================================
# KHỞI ĐỘNG SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print(f"""
    ╔════════════════════════════════════════════════════════════════╗
    ║  Starting {config.APP_NAME:<36} ║
    ║  Version: {config.API_VERSION:<48} ║
    ║  Debug: {str(config.DEBUG):<53} ║
    ║                                                                ║
    ║  📚 API Docs: http://localhost:8000/api/docs                  ║
    ║  🔍 OpenAPI: http://localhost:8000/api/openapi.json           ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=config.DEBUG
    )

