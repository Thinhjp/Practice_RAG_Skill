import pytest

from app.config import config
from app.services import DatabaseService


@pytest.fixture(autouse=True)
def isolated_runtime(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "UPLOAD_DIR", str(tmp_path / "uploads"))
    monkeypatch.setattr(config, "NORMALIZED_DIR", str(tmp_path / "normalized"))
    monkeypatch.setattr(config, "VECTOR_DB_PATH", str(tmp_path / "vector_db"))
    monkeypatch.setattr(config, "EMBEDDING_BACKEND", "hashing")
    monkeypatch.setattr(config, "EMBEDDING_DIM", 128)
    monkeypatch.setattr(config, "CHUNK_SIZE", 80)
    monkeypatch.setattr(config, "CHUNK_OVERLAP", 20)
    monkeypatch.setattr(config, "SIMILARITY_THRESHOLD", -1.0)
    monkeypatch.setattr(config, "GEMINI_API_KEY", "")
    DatabaseService.clear_database()
    yield
