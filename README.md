# Practice RAG Backend

FastAPI backend để thực hành pipeline:

```text
Upload → Extract → Chunk → Embed → Vector store → Retrieve
```

Hỗ trợ TXT, PDF và DOCX. Vector store được lưu bằng NumPy + JSON để có thể quan sát trực tiếp logic RAG trước khi chuyển sang FAISS, Qdrant hoặc dịch vụ vector database.

## Chạy bằng Python 3.14 trên Windows

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn app.main:app --reload
```

Mặc định dùng hashing backend để chạy tức thì, offline và thuận tiện quan sát pipeline:

```dotenv
EMBEDDING_BACKEND=hashing
```

Hashing backend phù hợp để học pipeline nhưng chủ yếu đo tương đồng từ vựng. Để bật semantic search tiếng Việt, cài thêm backend:

```powershell
python -m pip install -r requirements-semantic.txt
```

Sau đó sửa `.env`:

```dotenv
EMBEDDING_BACKEND=sentence_transformers
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

API docs: <http://127.0.0.1:8000/api/docs>

## Test

```powershell
python -m pytest -q
```

## API chính

- `POST /api/v1/upload`
- `POST /api/v1/search`
- `POST /api/v1/ask`
- `GET /api/v1/stats`
- `GET /api/v1/chunks`
- `GET /api/v1/embeddings/stats`
- `DELETE /api/v1/database`
- `GET /api/v1/health`

`POST /api/v1/ask` mặc định trả lời theo kiểu extractive và kèm nguồn, nên không cần API key. `app/services/answer_service.py` là điểm thay backend này bằng LLM khi cần sinh câu trả lời tự nhiên hơn.
