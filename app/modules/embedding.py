"""Embedding backends used by the retrieval pipeline."""

import hashlib
import re
from typing import Dict, List

import numpy as np

from app.config import config


class HashingEmbedder:
    """Small deterministic offline embedder for practice and automated tests."""

    def __init__(self, dimension: int):
        self.dimension = dimension

    def _encode_one(self, text: str) -> np.ndarray:
        vector = np.zeros(self.dimension, dtype=np.float32)
        normalized = re.sub(r"\s+", " ", text.casefold()).strip()
        tokens = re.findall(r"\w+", normalized, flags=re.UNICODE)
        features = [*tokens, *(normalized[i : i + 3] for i in range(max(0, len(normalized) - 2)))]
        for feature in features:
            digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=8).digest()
            number = int.from_bytes(digest, "little")
            index = number % self.dimension
            vector[index] += 1.0 if number & 1 else -1.0
        norm = np.linalg.norm(vector)
        if norm:
            vector /= norm
        return vector

    def encode(self, texts, **_: object) -> np.ndarray:
        if isinstance(texts, str):
            return self._encode_one(texts)
        return np.vstack([self._encode_one(text) for text in texts]).astype(np.float32)


_embedding_model = None
_embedding_signature: tuple[str, str, int] | None = None


def initialize_embedder():
    """Lazily initialize the configured embedding backend."""
    global _embedding_model, _embedding_signature
    backend = config.EMBEDDING_BACKEND.strip().lower().replace("-", "_")
    signature = (backend, config.EMBEDDING_MODEL, config.EMBEDDING_DIM)
    if _embedding_model is not None and _embedding_signature == signature:
        return _embedding_model

    if backend == "hashing":
        model = HashingEmbedder(config.EMBEDDING_DIM)
    elif backend == "sentence_transformers":
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError(
                "sentence-transformers is not installed. Install requirements.txt "
                "or set EMBEDDING_BACKEND=hashing."
            ) from exc
        model = SentenceTransformer(config.EMBEDDING_MODEL)
    else:
        raise ValueError(
            "EMBEDDING_BACKEND must be 'sentence_transformers' or 'hashing'"
        )

    _embedding_model = model
    _embedding_signature = signature
    return model


def embed_text(text: str) -> np.ndarray:
    """Embed one non-empty text and return a normalized float32 vector."""
    if not text or not text.strip():
        raise ValueError("Text to embed cannot be empty")
    model = initialize_embedder()
    vector = np.asarray(
        model.encode(text.strip(), convert_to_numpy=True), dtype=np.float32
    ).reshape(-1)
    if not np.isfinite(vector).all():
        raise ValueError("Embedding contains non-finite values")
    norm = np.linalg.norm(vector)
    return vector / norm if norm else vector


def embed_chunks(chunks: List[Dict]) -> List[Dict]:
    """Embed chunks in one batch without mutating the caller's dictionaries."""
    if not chunks:
        return []
    texts = [str(chunk.get("text", "")).strip() for chunk in chunks]
    if any(not text for text in texts):
        raise ValueError("Every chunk must contain non-empty text")

    model = initialize_embedder()
    vectors = np.asarray(
        model.encode(texts, convert_to_numpy=True), dtype=np.float32
    )
    if vectors.ndim == 1:
        vectors = vectors.reshape(1, -1)
    if len(vectors) != len(chunks) or not np.isfinite(vectors).all():
        raise ValueError("Embedding backend returned an invalid matrix")

    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    normalized = np.divide(vectors, norms, out=np.zeros_like(vectors), where=norms != 0)
    return [{**chunk, "embedding": vector} for chunk, vector in zip(chunks, normalized)]


def normalize_embeddings(chunks: List[Dict]) -> List[Dict]:
    result = []
    for chunk in chunks:
        if "embedding" not in chunk:
            raise ValueError("Chunk is missing its embedding")
        vector = np.asarray(chunk["embedding"], dtype=np.float32)
        norm = np.linalg.norm(vector)
        result.append({**chunk, "embedding": vector / norm if norm else vector})
    return result
