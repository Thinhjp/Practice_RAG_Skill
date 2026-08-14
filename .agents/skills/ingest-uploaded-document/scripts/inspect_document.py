"""Inspect an upload with the RAG project's production routing code."""

import argparse
import asyncio
import json
import sys
from pathlib import Path


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument(
        "--convert",
        action="store_true",
        help="Call Gemini when local extraction is insufficient.",
    )
    return parser.parse_args()


async def _run(arguments: argparse.Namespace) -> dict:
    project_root = arguments.project_root.resolve()
    input_path = arguments.file.resolve()
    if not (project_root / "app" / "modules" / "data_ingestion.py").exists():
        raise ValueError("--project-root does not contain the expected RAG application")
    if not input_path.is_file():
        raise ValueError(f"File does not exist: {input_path}")
    sys.path.insert(0, str(project_root))

    from app.config import config
    from app.modules.file_inspection import inspect_file
    from app.modules.gemini_converter import GeminiHtmlConverter
    from app.modules.native_extraction import extract_native
    from app.schemas.ingestion_models import IngestionRoute

    normalized = Path(config.NORMALIZED_DIR)
    if not normalized.is_absolute():
        config.NORMALIZED_DIR = str(project_root / normalized)

    inspection = inspect_file(str(input_path), input_path.name)
    extraction = extract_native(inspection)
    if extraction.acceptable:
        route = IngestionRoute.DIRECT_TEXT
    elif extraction.has_partial_pages:
        route = IngestionRoute.HYBRID_HTML
    else:
        route = IngestionRoute.GEMINI_HTML

    result = {
        "file": inspection.original_name,
        "sha256": inspection.sha256,
        "detected_mime": inspection.detected_mime,
        "size_bytes": inspection.size_bytes,
        "route": route.value,
        "extractor": extraction.extractor,
        "native_text_chars": len(extraction.text),
        "printable_ratio": round(extraction.printable_ratio, 4),
        "page_coverage": round(extraction.page_coverage, 4),
        "warnings": extraction.warnings,
    }
    if route is not IngestionRoute.DIRECT_TEXT and arguments.convert:
        conversion = await GeminiHtmlConverter().convert(inspection)
        result.update(
            {
                "normalized_html_path": conversion.artifact_path,
                "converter_model": conversion.model,
                "prompt_version": conversion.prompt_version,
                "cached": conversion.cached,
            }
        )
    return result


def main() -> int:
    try:
        print(json.dumps(asyncio.run(_run(_arguments())), ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
