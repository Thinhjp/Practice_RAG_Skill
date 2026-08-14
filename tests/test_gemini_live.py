"""Opt-in Gemini smoke test. It is skipped during the normal test suite."""

import asyncio
import hashlib
import os

import pytest
from PIL import Image, ImageDraw

from app.config import config
from app.modules.gemini_converter import GeminiHtmlConverter
from app.modules.html_processing import html_to_text
from app.schemas.ingestion_models import FileInspection


@pytest.mark.live
def test_gemini_converts_a_text_image_to_html(tmp_path, monkeypatch):
    if os.getenv("RUN_GEMINI_LIVE") != "1":
        pytest.skip("Set RUN_GEMINI_LIVE=1 to enable the Gemini quota smoke test")
    api_key = os.getenv("GEMINI_API_KEY") or config.GEMINI_API_KEY
    if not api_key:
        pytest.skip("GEMINI_API_KEY is not configured")

    image_path = tmp_path / "invoice.png"
    image = Image.new("RGB", (800, 240), "white")
    ImageDraw.Draw(image).text(
        (40, 80),
        "INVOICE\nTOTAL: 120,000 VND",
        fill="black",
        spacing=12,
    )
    image.save(image_path)
    content = image_path.read_bytes()
    inspection = FileInspection(
        path=str(image_path),
        original_name=image_path.name,
        extension=".png",
        detected_mime="image/png",
        size_bytes=len(content),
        sha256=hashlib.sha256(content).hexdigest(),
    )
    monkeypatch.setattr(config, "NORMALIZED_DIR", str(tmp_path / "normalized"))
    conversion = asyncio.run(GeminiHtmlConverter(api_key=api_key).convert(inspection))
    text = html_to_text(conversion.html).lower()
    assert "invoice" in text
    assert "120" in text
