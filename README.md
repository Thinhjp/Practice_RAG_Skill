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

Hoặc khởi động bằng launcher:

```powershell
.\start.ps1
```

Trên Git Bash, WSL, Linux hoặc macOS:

```bash
./start.sh
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

## Gemini document conversion

Native text is extracted locally from text, PDF, DOCX, XLSX and PPTX files. Images,
scanned PDFs, and low-quality document extractions are converted to sanitized HTML
with Gemini before structure-aware chunking.

Create a free Gemini API key in Google AI Studio and add it to `.env`:

```dotenv
GEMINI_API_KEY=your-key-here
GEMINI_MODEL=gemini-3.5-flash-lite
```

The key is required only for the `gemini_html` and `hybrid_html` routes. HTML artifacts
are cached in `data/normalized/`. Install LibreOffice and make `soffice` available on
`PATH` if DOCX, XLSX or PPTX files must fall back to visual conversion.

Run the opt-in free-tier smoke test after configuring the key:

```powershell
$env:RUN_GEMINI_LIVE="1"
python -m pytest -q -m live
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
