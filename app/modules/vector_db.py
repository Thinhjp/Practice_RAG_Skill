"""A small persistent NumPy vector store for learning RAG mechanics."""

import json
import os
import threading
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from uuid import uuid4

import numpy as np

from app.config import config


_DB_LOCK = threading.RLock()


def _paths(db_path: str | None = None) -> tuple[Path, Path, Path]:
    directory = Path(db_path or config.VECTOR_DB_PATH)
    return directory, directory / config.VECTOR_DB_FILE, directory / config.METADATA_FILE


def _validate(vectors: Optional[np.ndarray], metadata: List[Dict]) -> None:
    if vectors is None:
        if metadata:
            raise ValueError("Metadata exists without vectors")
        return
    if vectors.ndim != 2:
        raise ValueError("Vectors must be a two-dimensional matrix")
    if len(vectors) != len(metadata):
        raise ValueError("Vector and metadata counts do not match")
    if not np.isfinite(vectors).all():
        raise ValueError("Vectors contain non-finite values")


def load_vector_db(db_path: str | None = None) -> Tuple[Optional[np.ndarray], List[Dict]]:
    directory, vectors_path, metadata_path = _paths(db_path)
    if not directory.exists() or (not vectors_path.exists() and not metadata_path.exists()):
        return None, []
    if not vectors_path.exists() or not metadata_path.exists():
        raise RuntimeError("Vector database is incomplete")

    with _DB_LOCK:
        try:
            vectors = np.load(vectors_path, allow_pickle=False).astype(np.float32, copy=False)
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except Exception as exc:
            raise RuntimeError(f"Cannot load vector database: {exc}") from exc
    if not isinstance(metadata, list):
        raise RuntimeError("Metadata file must contain a JSON list")
    _validate(vectors, metadata)
    return vectors, metadata


def save_vector_db(
    vectors: np.ndarray, metadata: List[Dict], db_path: str | None = None
) -> bool:
    matrix = np.asarray(vectors, dtype=np.float32)
    _validate(matrix, metadata)
    directory, vectors_path, metadata_path = _paths(db_path)
    directory.mkdir(parents=True, exist_ok=True)
    token = uuid4().hex
    vectors_temp = directory / f".{config.VECTOR_DB_FILE}.{token}.tmp"
    metadata_temp = directory / f".{config.METADATA_FILE}.{token}.tmp"

    with _DB_LOCK:
        try:
            with vectors_temp.open("wb") as output:
                np.save(output, matrix, allow_pickle=False)
                output.flush()
                os.fsync(output.fileno())
            metadata_temp.write_text(
                json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            os.replace(vectors_temp, vectors_path)
            os.replace(metadata_temp, metadata_path)
        finally:
            vectors_temp.unlink(missing_ok=True)
            metadata_temp.unlink(missing_ok=True)
    return True


def add_to_vector_db(
    chunks: List[Dict],
    vectors: Optional[np.ndarray] = None,
    metadata: Optional[List[Dict]] = None,
) -> Tuple[Optional[np.ndarray], List[Dict]]:
    current_metadata = list(metadata or [])
    if not chunks:
        _validate(vectors, current_metadata)
        return vectors, current_metadata

    try:
        new_vectors = np.vstack(
            [np.asarray(chunk["embedding"], dtype=np.float32).reshape(1, -1) for chunk in chunks]
        )
    except KeyError as exc:
        raise ValueError("Every chunk must have an embedding") from exc

    new_metadata = [
        {key: value for key, value in chunk.items() if key != "embedding"}
        for chunk in chunks
    ]
    if vectors is None:
        updated_vectors = new_vectors
    else:
        current = np.asarray(vectors, dtype=np.float32)
        if current.ndim != 2 or current.shape[1] != new_vectors.shape[1]:
            raise ValueError("New embeddings have a different dimension")
        updated_vectors = np.vstack([current, new_vectors])
    updated_metadata = [*current_metadata, *new_metadata]
    _validate(updated_vectors, updated_metadata)
    return updated_vectors, updated_metadata


def append_chunks(chunks: List[Dict], db_path: str | None = None) -> Tuple[np.ndarray, List[Dict]]:
    """Atomically load, append, and persist chunks for concurrent upload requests."""
    with _DB_LOCK:
        vectors, metadata = load_vector_db(db_path)
        updated_vectors, updated_metadata = add_to_vector_db(chunks, vectors, metadata)
        if updated_vectors is None:
            raise ValueError("No chunks were supplied")
        save_vector_db(updated_vectors, updated_metadata, db_path)
        return updated_vectors, updated_metadata


def get_vector_db_stats(
    vectors: Optional[np.ndarray] = None, metadata: Optional[List[Dict]] = None
) -> Dict:
    if vectors is None and metadata is None:
        vectors, metadata = load_vector_db()
    items = list(metadata or [])
    if vectors is None:
        vectors = np.empty((0, 0), dtype=np.float32)
    _validate(vectors, items)
    counts = Counter(item.get("file_name", "unknown") for item in items)
    return {
        "total_chunks": len(items),
        "embedding_dim": int(vectors.shape[1]) if vectors.size else 0,
        "vector_shape": list(vectors.shape),
        "unique_files": len(counts),
        "files": [
            {"file_name": name, "chunk_count": count}
            for name, count in sorted(counts.items())
        ],
    }


class VectorDB:
    """Object-oriented facade over the functional persistence API."""

    def __init__(self, db_path: str | None = None):
        self.db_path = db_path
        self.vectors, self.metadata = load_vector_db(db_path)

    def add_chunks(self, chunks: List[Dict]) -> None:
        self.vectors, self.metadata = add_to_vector_db(
            chunks, self.vectors, self.metadata
        )

    def save(self) -> bool:
        if self.vectors is None:
            return True
        return save_vector_db(self.vectors, self.metadata, self.db_path)

    def get_size(self) -> int:
        return len(self.metadata)
