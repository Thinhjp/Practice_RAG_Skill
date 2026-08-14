"""Business workflow for vector retrieval."""

from typing import Dict, List, Optional

from app.modules import search


class SearchService:
    @staticmethod
    def search_chunks(
        query: str,
        top_k: Optional[int] = None,
        threshold: Optional[float] = None,
    ) -> List[Dict]:
        results = search.search_similar_chunks(
            query=query, top_k=top_k, threshold=threshold
        )
        return search.format_search_results(results)
