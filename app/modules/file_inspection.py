"""Detect the real upload format and reject obvious extension spoofing."""

import hashlib
import mimetypes
import zipfile
from pathlib import Path

from app.schemas.ingestion_models import FileInspection


_IMAGE_SIGNATURES = (
    (b"\x89PNG\r\n\x1a\n", "image/png"),
    (b"\xff\xd8\xff", "image/jpeg"),
    (b"GIF87a", "image/gif"),
    (b"GIF89a", "image/gif"),
    (b"BM", "image/bmp"),
    (b"II*\x00", "image/tiff"),
    (b"MM\x00*", "image/tiff"),
)

_MIME_EXTENSIONS = {
    "application/pdf": {".pdf"},
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {".docx"},
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {".xlsx"},
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": {".pptx"},
    "image/png": {".png"},
    "image/jpeg": {".jpg", ".jpeg"},
    "image/webp": {".webp"},
    "image/gif": {".gif"},
    "image/bmp": {".bmp"},
    "image/tiff": {".tif", ".tiff"},
}


def _detect_ooxml(path: Path) -> str | None:
    if not zipfile.is_zipfile(path):
        return None
    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
    except (OSError, zipfile.BadZipFile):
        return None
    if "word/document.xml" in names:
        return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    if "xl/workbook.xml" in names:
        return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    if "ppt/presentation.xml" in names:
        return "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    return "application/zip"


def detect_mime(path: str) -> str:
    file_path = Path(path)
    with file_path.open("rb") as source:
        prefix = source.read(16)
    if prefix.startswith(b"MZ") or prefix.startswith(b"\x7fELF"):
        return "application/x-executable"
    if prefix.startswith(b"%PDF-"):
        return "application/pdf"
    for signature, mime in _IMAGE_SIGNATURES:
        if prefix.startswith(signature):
            return mime
    if prefix.startswith(b"RIFF") and prefix[8:12] == b"WEBP":
        return "image/webp"
    if prefix.startswith(b"PK\x03\x04"):
        return _detect_ooxml(file_path) or "application/zip"
    guessed, _ = mimetypes.guess_type(file_path.name)
    return guessed or "application/octet-stream"


def inspect_file(path: str, original_name: str) -> FileInspection:
    file_path = Path(path)
    extension = Path(original_name).suffix.lower()
    detected_mime = detect_mime(path)

    if detected_mime in {"application/x-msdownload", "application/x-executable"}:
        raise ValueError("Executable uploads are not allowed")
    expected_extensions = _MIME_EXTENSIONS.get(detected_mime)
    if expected_extensions and extension not in expected_extensions:
        expected = ", ".join(sorted(expected_extensions))
        raise ValueError(
            f"File content is {detected_mime}, but extension is {extension or '(none)'}; "
            f"expected: {expected}"
        )
    if detected_mime == "application/zip":
        raise ValueError("Generic ZIP archives are not supported")

    digest = hashlib.sha256()
    with file_path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return FileInspection(
        path=str(file_path),
        original_name=Path(original_name).name,
        extension=extension,
        detected_mime=detected_mime,
        size_bytes=file_path.stat().st_size,
        sha256=digest.hexdigest(),
    )
