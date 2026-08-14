from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_chat_ui_and_static_assets():
    page = client.get("/")
    assert page.status_code == 200
    assert page.headers["content-type"].startswith("text/html")
    assert "RAGmate" in page.text
    assert "/static/app.js" in page.text

    script = client.get("/static/app.js")
    assert script.status_code == 200
    assert "submitQuestion" in script.text


def test_health_upload_search_and_stats():
    health = client.get("/api/v1/health")
    assert health.status_code == 200
    assert health.json()["status"] == "healthy"

    content = (
        "Retrieval Augmented Generation kết hợp truy xuất tài liệu với mô hình ngôn ngữ. "
        "Vector embedding giúp tìm các đoạn văn liên quan."
    )
    upload = client.post(
        "/api/v1/upload",
        files={"file": ("rag.txt", content.encode("utf-8"), "text/plain")},
    )
    assert upload.status_code == 200, upload.text
    assert upload.json()["chunks_count"] >= 1

    stats = client.get("/api/v1/stats")
    assert stats.status_code == 200
    assert stats.json()["total_chunks"] >= 1

    response = client.post(
        "/api/v1/search",
        json={"query": "vector truy xuất tài liệu", "top_k": 3, "threshold": -1},
    )
    assert response.status_code == 200, response.text
    assert response.json()[0]["file_name"] == "rag.txt"

    answer = client.post(
        "/api/v1/ask",
        json={"query": "RAG sử dụng vector như thế nào?", "top_k": 2, "threshold": -1},
    )
    assert answer.status_code == 200, answer.text
    assert answer.json()["generation_backend"] == "extractive"
    assert answer.json()["sources"]


def test_rejects_unsupported_and_empty_files():
    unsupported = client.post(
        "/api/v1/upload", files={"file": ("bad.exe", b"data", "application/octet-stream")}
    )
    assert unsupported.status_code == 400

    empty = client.post(
        "/api/v1/upload", files={"file": ("empty.txt", b"", "text/plain")}
    )
    assert empty.status_code == 400
