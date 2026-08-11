"""
=============================================================================
HƯỚNG DẪN THỰC HIỆN DỰ ÁN RAG PIPELINE
=============================================================================

GIỚI THIỆU:
Dự án này xây dựng một hệ thống RAG (Retrieval-Augmented Generation) Backend
sử dụng FastAPI. Hệ thống cho phép:
- Upload tài liệu (PDF, TXT, DOCX)
- Chia tài liệu thành chunks
- Tạo embeddings cho chunks
- Lưu vào vector database
- Tìm kiếm và truy xuất chunks tương tự

BƯỚC 1: KHỞI TẠO MÔI TRƯỜNG
─────────────────────────────────────────────────────────────────────────

1.1 Clone dự án / Tạo thư mục rag
    mkdir rag && cd rag

1.2 Tạo virtual environment:
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # hoặc
    venv\\Scripts\\activate  # Windows

1.3 Cài đặt dependencies:
    pip install -r requirements.txt


BƯỚC 2: TRIỂN KHAI MODULE 1 - DATA_INGESTION (Upload & Trích xuất TEXT)
─────────────────────────────────────────────────────────────────────────

File: app/modules/data_ingestion.py

Các hàm cần triển khai:

1. validate_file(filename: str) -> bool
   - Kiểm tra file có đúng định dạng (.pdf, .txt, .docx)
   - So sánh extension với ALLOWED_FILE_TYPES trong config
   
2. extract_text_from_pdf(file_path: str) -> str
   - Dùng PyPDF2 hoặc pypdf để đọc PDF
   - Lặp qua các trang, extract text từ mỗi trang
   
3. extract_text_from_txt(file_path: str) -> str
   - Đơn giản nhất, chỉ cần read file với encoding utf-8
   
4. extract_text_from_docx(file_path: str) -> str
   - Dùng python-docx để đọc Word files
   - Extract text từ paragraphs
   
5. save_uploaded_file(upload_file: UploadFile) -> str
   - Kiểm tra kích thước file (MAX_FILE_SIZE)
   - Tạo thư mục UPLOAD_DIR nếu chưa có
   - Lưu file và return đường dẫn
   
6. process_uploaded_file(upload_file: UploadFile) -> Tuple[str, str]
   - Kết hợp các hàm trên
   - Return (file_path, extracted_text)

Ví dụ test:
    from app.modules import data_ingestion
    # Upload một file PDF
    # data_ingestion.process_uploaded_file(file) sẽ return text


BƯỚC 3: TRIỂN KHAI MODULE 2 - CHUNKING (Chia text thành chunks)
─────────────────────────────────────────────────────────────────────────

File: app/modules/chunking.py

Các hàm cần triển khai:

1. split_text_simple(text: str, chunk_size: int, overlap: int) -> List[str]
   - Chia text theo số ký tự
   - Thêm overlap để giữ ngữ cảnh
   
2. split_text_by_sentences(text: str, chunk_size: int, overlap: int) -> List[str]
   - Thông minh hơn: chia theo câu (không cắt ngang câu)
   - Regex: r'[.!?]+' để tách câu
   
3. split_text_by_paragraphs(text: str, chunk_size: int, overlap: int) -> List[str]
   - Chia theo đoạn văn (split by '\n\n')
   
4. add_chunk_metadata(chunks: List[str], source: str, file_name: str) -> List[Dict]
   - Thêm thông tin: chunk_id, source, file_name, length, ...
   
5. prepare_chunks(text: str, source: str, file_name: str, method: str) -> List[Dict]
   - Kết hợp tất cả các hàm trên
   - method: "simple", "sentence", hoặc "paragraph"

Ví dụ test:
    from app.modules import chunking
    text = "Đây là một đoạn văn bản..."
    chunks = chunking.prepare_chunks(text, "file.pdf", "file.pdf")
    print(len(chunks))  # Số lượng chunks
    print(chunks[0])    # Chunk đầu tiên


BƯỚC 4: TRIỂN KHAI MODULE 3 - EMBEDDING (Tạo vector embeddings)
─────────────────────────────────────────────────────────────────────────

File: app/modules/embedding.py

Các hàm cần triển khai:

1. initialize_embedder() -> SentenceTransformer
   - Tải model SentenceTransformer (lazy loading)
   - Model mặc định: "all-MiniLM-L6-v2"
   - Lưu vào global variable để tránh tải lại nhiều lần
   
2. embed_text(text: str) -> np.ndarray
   - Sử dụng model.encode(text) để tạo embedding
   - Return vector có kích thước EMBEDDING_DIM (384)
   
3. embed_chunks(chunks: List[Dict]) -> List[Dict]
   - Batch process: lấy tất cả texts từ chunks
   - Dùng model.encode(texts) để embedding tất cả một lúc (nhanh hơn)
   - Gán embedding vào mỗi chunk
   
4. normalize_embeddings(chunks: List[Dict]) -> List[Dict]
   - Chuẩn hóa L2: vector / ||vector||
   - Tùy chọn, nhưng giúp tính cosine similarity nhanh hơn

Ví dụ test:
    from app.modules import embedding
    chunks = [...]  # Từ chunking module
    chunks_with_emb = embedding.embed_chunks(chunks)
    print(chunks_with_emb[0]["embedding"].shape)  # (384,)


BƯỚC 5: TRIỂN KHAI MODULE 4 - VECTOR_DB (Lưu & quản lý vector database)
─────────────────────────────────────────────────────────────────────────

File: app/modules/vector_db.py

Các hàm cần triển khai:

1. load_vector_db(db_path: str) -> Tuple[np.ndarray, List[Dict]]
   - Tải vectors từ vectors.npy
   - Tải metadata từ metadata.json
   - Return (None, []) nếu file không tồn tại
   
2. save_vector_db(vectors: np.ndarray, metadata: List[Dict], db_path: str) -> bool
   - Tạo thư mục db_path nếu chưa có
   - Lưu vectors vào vectors.npy
   - Lưu metadata vào metadata.json
   
3. add_to_vector_db(chunks: List[Dict], vectors: np.ndarray, metadata: List[Dict]) -> Tuple
   - Nếu vectors is None: khởi tạo vectors từ chunks đầu tiên
   - Nếu vectors không None: ghép vectors cũ và mới (np.vstack)
   - Ghép metadata
   - Return (vectors, metadata)
   
4. get_vector_db_stats(vectors, metadata) -> Dict
   - Đếm total chunks, embedding_dim, unique files
   - Return thống kê dạng dict


BƯỚC 6: TRIỂN KHAI MODULE 5 - SEARCH (Tìm kiếm & truy xuất)
─────────────────────────────────────────────────────────────────────────

File: app/modules/search.py

Các hàm cần triển khai:

1. calculate_similarity(vector1: np.ndarray, vector2: np.ndarray, metric: str) -> float
   - Cosine similarity: A·B / (||A|| * ||B||)
   - Euclidean distance: sqrt(sum((A-B)^2))
   
2. search_similar_chunks(query: str, vectors, metadata, top_k, threshold) -> List[Dict]
   - Embed query
   - Tính độ tương tự với tất cả chunks
   - Sort theo similarity descending
   - Filter by threshold, lấy top_k
   
3. retrieve_context(chunk_id, metadata, context_size) -> Dict
   - Lấy chunks trước/sau chunk được chỉ định
   - Return {main_chunk, context_before, context_after}
   
4. format_search_results(results, include_scores) -> List[Dict]
   - Định dạng kết quả trước khi trả về
   - Có thể cắt ngắn text, làm tròn scores


BƯỚC 7: TRIỂN KHAI MAIN.PY - FastAPI Application
─────────────────────────────────────────────────────────────────────────

File: app/main.py

Các endpoint cần triển khai:

1. POST /api/v1/upload
   - Nhận file upload
   - Xử lý qua pipeline: trích text -> chunking -> embedding -> lưu DB
   - Return số chunks được tạo
   
2. POST /api/v1/search
   - Nhận query string
   - Tìm chunks tương tự từ database
   - Return danh sách chunks có similarity scores
   
3. GET /api/v1/stats
   - Return thống kê database (total chunks, files, ...)
   
4. GET /api/v1/health
   - Health check endpoint
   
5. DELETE /api/v1/database (tùy chọn)
   - Xóa toàn bộ vector database



Sau khi triển khai tất cả modules, test toàn bộ pipeline:

1. Khởi động server:
   cd app
   python main.py
   # hoặc
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload

2. Test upload (HTTP POST):
   curl -X POST "http://localhost:8000/api/v1/upload" \\
        -F "file=@document.pdf"

3. Test search (HTTP POST):
   curl -X POST "http://localhost:8000/api/v1/search" \\
        -H "Content-Type: application/json" \\
        -d '{"query": "What is AI?", "top_k": 5}'

4. Test stats (HTTP GET):
   curl "http://localhost:8000/api/v1/stats"

5. Test health (HTTP GET):
   curl "http://localhost:8000/api/v1/health"



- fastapi: Web framework
- uvicorn: ASGI server
- python-multipart: Để upload file
- numpy: Numerical computing
- sentence-transformers: Embedding model
- PyPDF2: Đọc file PDF
- python-dotenv: Quản lý environment variables




1. Sử dụng vector database chuyên dụng:
   - Weaviate, Pinecone, Milvus, Faiss
   - Thay vì numpy array + json file

2. Caching results:
   - Lưu cache kết quả tìm kiếm thường xuyên

3. Batch processing:
   - Xử lý nhiều file cùng lúc

4. Database relational:
   - Lưu metadata vào PostgreSQL thay vì JSON

5. Authentication & Authorization:
   - Thêm JWT tokens, role-based access

6. Monitoring & Logging:
   - Thêm logging chi tiết, metrics

7. Async processing:
   - Sử dụng Celery hoặc RQ cho background tasks


