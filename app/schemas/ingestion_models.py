"""Internal contracts for the upload classification and conversion pipeline."""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Optional


class IngestionRoute(StrEnum):
    DIRECT_TEXT = "direct_text"
    GEMINI_HTML = "gemini_html"
    HYBRID_HTML = "hybrid_html"


@dataclass(frozen=True)
class FileInspection:
    path: str
    original_name: str
    extension: str
    detected_mime: str
    size_bytes: int
    sha256: str


@dataclass
class NativeExtraction:
    text: str
    extractor: str
    printable_ratio: float = 1.0
    page_coverage: float = 1.0
    page_count: int = 0
    has_partial_pages: bool = False
    acceptable: bool = False
    warnings: list[str] = field(default_factory=list)


@dataclass
class ConversionResult:
    html: str
    artifact_path: str
    model: str
    prompt_version: str
    cached: bool = False


@dataclass
class PreparedDocument:
    inspection: FileInspection
    route: IngestionRoute
    text: str
    extractor: str
    html: Optional[str] = None
    normalized_html_path: Optional[str] = None
    converter_model: Optional[str] = None
    prompt_version: Optional[str] = None
    cached_conversion: bool = False
    warnings: list[str] = field(default_factory=list)
