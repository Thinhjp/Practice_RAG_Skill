"""Similarity search and neighboring-context retrieval."""

from typing import Dict, List, Optional

import numpy as np

from app.config import config
from app.modules.embedding import embed_text
from app.modules.vector_db import load_vector_db


def calculate_similarity(
    vector1: np.ndarray, vector2: np.ndarray, metric: str = "cosine"
) -> float:
    first = np.asarray(vector1, dtype=np.float32).reshape(-1)
    second = np.asarray(vector2, dtype=np.float32).reshape(-1)
    if first.shape != second.shape:
        raise ValueError("Vectors must have the same shape")
    metric = metric.lower()
    if metric == "cosine":
        denominator = float(np.linalg.norm(first) * np.linalg.norm(second))
        return float(np.dot(first, second) / denominator) if denominator else 0.0
    if metric == "euclidean":
        return float(1.0 / (1.0 + np.linalg.norm(first - second)))
    raise ValueError("metric must be 'cosine' or 'euclidean'")


def search_similar_chunks(
    query: str,
    vectors: Optional[np.ndarray] = None,
    metadata: Optional[List[Dict]] = None,
    top_k: Optional[int] = None,
    threshold: Optional[float] = None,
) -> List[Dict]:
    if not query or not query.strip():
        raise ValueError("Search query cannot be empty")
    if vectors is None and metadata is None:
        vectors, metadata = load_vector_db()
    if vectors is None or not metadata:
        return []
    if len(vectors) != len(metadata):
        raise ValueError("Vector and metadata counts do not match")

    limit = config.MAX_RESULTS if top_k is None else top_k
    minimum = config.SIMILARITY_THRESHOLD if threshold is None else threshold
    if limit <= 0:
        raise ValueError("top_k must be greater than zero")
    if not -1.0 <= minimum <= 1.0:
        raise ValueError("threshold must be between -1 and 1")

    query_vector = embed_text(query)
    matrix = np.asarray(vectors, dtype=np.float32)
    if matrix.ndim != 2 or matrix.shape[1] != query_vector.shape[0]:
        raise ValueError("Query and database embedding dimensions do not match")

    metric = config.SIMILARITY_METRIC.lower()
    if metric == "cosine":
        query_norm = np.linalg.norm(query_vector)
        row_norms = np.linalg.norm(matrix, axis=1)
        denominators = row_norms * query_norm
        scores = np.divide(
            matrix @ query_vector,
            denominators,
            out=np.zeros(len(matrix), dtype=np.float32),
            where=denominators != 0,
        )
    elif metric == "euclidean":
        distances = np.linalg.norm(matrix - query_vector, axis=1)
        scores = 1.0 / (1.0 + distances)
    else:
        raise ValueError("Unsupported similarity metric")

    ranked_indices = np.argsort(scores)[::-1]
    results = []
    for index in ranked_indices:
        score = float(scores[index])
        if score < minimum:
            continue
        results.append({**metadata[int(index)], "similarity_score": score})
        if len(results) == limit:
            break
    return results


def retrieve_context(chunk_id: int, metadata: List[Dict], context_size: int = 2) -> Dict:
    if context_size < 0:
        raise ValueError("context_size cannot be negative")
    main = next((item for item in metadata if item.get("chunk_id") == chunk_id), None)
    if main is None:
        raise ValueError("Chunk not found")
    document_id = main.get("document_id")
    same_document = sorted(
        (item for item in metadata if item.get("document_id") == document_id),
        key=lambda item: item.get("chunk_index", 0),
    )
    position = next(i for i, item in enumerate(same_document) if item.get("chunk_id") == chunk_id)
    return {
        "main_chunk": main,
        "context_before": same_document[max(0, position - context_size) : position],
        "context_after": same_document[position + 1 : position + context_size + 1],
    }


def format_search_results(
    results: List[Dict], include_scores: bool = True
) -> List[Dict]:
    fields = (
        "chunk_id",
        "document_id",
        "chunk_index",
        "text",
        "source",
        "file_name",
        "length",
    )
    formatted = []
    for result in results:
        item = {field: result[field] for field in fields if field in result}
        if include_scores:
            item["similarity_score"] = round(float(result.get("similarity_score", 0.0)), 6)
        formatted.append(item)
    return formatted
