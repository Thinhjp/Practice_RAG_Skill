"""Runnable retrieval-augmented answer baseline."""

from typing import Dict, Optional

from app.config import config
from app.modules.prompt_builder import build_prompt
from app.services.search_service import SearchService


class AnswerService:
    @staticmethod
    def answer(
        question: str,
        top_k: Optional[int] = None,
        threshold: Optional[float] = None,
    ) -> Dict:
        contexts = SearchService.search_chunks(question, top_k, threshold)
        prompt = build_prompt(question, contexts)
        if not contexts:
            answer = "Không tìm thấy thông tin phù hợp trong kho tài liệu."
        elif config.GENERATION_BACKEND == "extractive":
            # A deterministic, grounded baseline that needs no API key.
            answer = "\n\n".join(
                f"{context['text']} [Nguồn {index}]"
                for index, context in enumerate(contexts, start=1)
            )
        else:
            raise ValueError(
                f"Unsupported generation backend: {config.GENERATION_BACKEND}"
            )
        sources = [
            {
                "source_number": index,
                "chunk_id": context["chunk_id"],
                "file_name": context["file_name"],
                "similarity_score": context["similarity_score"],
            }
            for index, context in enumerate(contexts, start=1)
        ]
        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "generation_backend": config.GENERATION_BACKEND,
            "prompt": prompt,
        }
