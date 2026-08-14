"""Business workflow for ingesting a file into the vector store."""

from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.modules import chunking, data_ingestion, embedding, vector_db


class UploadService:
    @staticmethod
    async def process_and_save_file(upload_file: UploadFile) -> dict:
        original_name = Path(upload_file.filename or "").name
        try:
            file_path, text = await data_ingestion.process_uploaded_file(upload_file)
            chunks = chunking.prepare_chunks(
                text, file_path, original_name, method="sentence"
            )
            if not chunks:
                raise ValueError("The document did not produce any chunks")
            embedded_chunks = embedding.embed_chunks(chunks)
            vector_db.append_chunks(embedded_chunks)
            return {
                "file_name": original_name,
                "chunks_count": len(chunks),
                "message": f"Successfully uploaded {original_name} with {len(chunks)} chunks",
            }
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(400, f"Upload failed: {exc}") from exc
