"""Business workflow for ingesting a file into the vector store."""

from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.modules import chunking, data_ingestion, embedding, vector_db
from app.modules.html_processing import prepare_html_chunks


class UploadService:
    @staticmethod
    async def process_and_save_file(upload_file: UploadFile) -> dict:
        original_name = Path(upload_file.filename or "").name
        try:
            document = await data_ingestion.process_uploaded_file(upload_file)
            inspection = document.inspection
            provenance = {
                "detected_mime": inspection.detected_mime,
                "content_sha256": inspection.sha256,
                "ingestion_route": document.route.value,
                "extractor": document.extractor,
                "normalized_html_path": document.normalized_html_path,
                "converter_model": document.converter_model,
                "prompt_version": document.prompt_version,
                "ingestion_warnings": document.warnings,
            }
            if document.html:
                chunks = prepare_html_chunks(
                    document.html,
                    inspection.path,
                    original_name,
                    document_id=inspection.sha256,
                    metadata=provenance,
                )
            else:
                chunks = chunking.prepare_chunks(
                    document.text,
                    inspection.path,
                    original_name,
                    method="sentence",
                    document_id=inspection.sha256,
                    extra_metadata=provenance,
                )
            if not chunks:
                raise ValueError("The document did not produce any chunks")
            embedded_chunks = embedding.embed_chunks(chunks)
            vector_db.append_chunks(embedded_chunks)
            return {
                "file_name": original_name,
                "chunks_count": len(chunks),
                "ingestion_route": document.route.value,
                "detected_mime": inspection.detected_mime,
                "normalized_html_path": document.normalized_html_path,
                "cached_conversion": document.cached_conversion,
                "message": f"Successfully uploaded {original_name} with {len(chunks)} chunks",
            }
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(400, f"Upload failed: {exc}") from exc
