"""Text chunking strategies and chunk metadata."""

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List
from uuid import NAMESPACE_URL, uuid5

from app.config import config


def _settings(chunk_size: int | None, overlap: int | None) -> tuple[int, int]:
    size = config.CHUNK_SIZE if chunk_size is None else chunk_size
    shared = config.CHUNK_OVERLAP if overlap is None else overlap
    if size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if shared < 0 or shared >= size:
        raise ValueError("overlap must satisfy 0 <= overlap < chunk_size")
    return size, shared


def split_text_simple(
    text: str, chunk_size: int | None = None, overlap: int | None = None
) -> List[str]:
    size, shared = _settings(chunk_size, overlap)
    cleaned = text.strip()
    if not cleaned:
        return []
    step = size - shared
    chunks = []
    start = 0
    while start < len(cleaned):
        end = min(start + size, len(cleaned))
        chunks.append(cleaned[start:end].strip())
        if end == len(cleaned):
            break
        start += step
    return chunks


def _pack_segments(
    segments: List[str], separator: str, chunk_size: int, overlap: int
) -> List[str]:
    """Pack complete segments and preserve complete trailing segments as overlap."""
    expanded: List[str] = []
    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue
        if len(segment) <= chunk_size:
            expanded.append(segment)
        else:
            expanded.extend(split_text_simple(segment, chunk_size, overlap))

    chunks: List[str] = []
    current: List[str] = []
    for segment in expanded:
        candidate = separator.join([*current, segment])
        if current and len(candidate) > chunk_size:
            chunks.append(separator.join(current))
            carry: List[str] = []
            carry_length = 0
            for previous in reversed(current):
                added = len(previous) + (len(separator) if carry else 0)
                if carry_length + added > overlap:
                    break
                carry.insert(0, previous)
                carry_length += added
            current = carry
            if current and len(separator.join([*current, segment])) > chunk_size:
                current = []
        current.append(segment)
    if current:
        final = separator.join(current)
        if not chunks or final != chunks[-1]:
            chunks.append(final)
    return chunks


def split_text_by_sentences(
    text: str, chunk_size: int | None = None, overlap: int | None = None
) -> List[str]:
    size, shared = _settings(chunk_size, overlap)
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return _pack_segments(sentences, " ", size, shared)


def split_text_by_paragraphs(
    text: str, chunk_size: int | None = None, overlap: int | None = None
) -> List[str]:
    size, shared = _settings(chunk_size, overlap)
    paragraphs = re.split(r"\n\s*\n", text.strip())
    return _pack_segments(paragraphs, "\n\n", size, shared)


def add_chunk_metadata(chunks: List[str], source: str, file_name: str) -> List[Dict]:
    document_id = uuid5(NAMESPACE_URL, str(Path(source).resolve())).hex
    created_at = datetime.now(timezone.utc).isoformat()
    result = []
    for index, text in enumerate(chunks):
        chunk_uuid = uuid5(NAMESPACE_URL, f"{document_id}:{index}")
        result.append(
            {
                "chunk_id": chunk_uuid.int,
                "document_id": document_id,
                "chunk_index": index,
                "text": text,
                "source": source,
                "file_name": Path(file_name).name,
                "length": len(text),
                "created_at": created_at,
            }
        )
    return result


def prepare_chunks(
    text: str, source: str, file_name: str, method: str = "sentence"
) -> List[Dict]:
    methods = {
        "simple": split_text_simple,
        "sentence": split_text_by_sentences,
        "paragraph": split_text_by_paragraphs,
    }
    try:
        chunks = methods[method.lower()](text)
    except KeyError as exc:
        raise ValueError(f"Unknown chunking method: {method}") from exc
    return add_chunk_metadata(chunks, source, file_name)
