# Format routing

Use extraction quality, not extension alone.

| Format | Native extractor | Fallback |
| --- | --- | --- |
| TXT, MD, CSV, JSON, XML, HTML | Text/structured parser | Reject when empty or invalid |
| PDF | `pypdf`, scored per page | Gemini PDF to HTML |
| DOCX | `python-docx`, including tables and headers | LibreOffice PDF, then Gemini |
| XLSX | `openpyxl`, retaining sheet and row boundaries | LibreOffice PDF, then Gemini |
| PPTX | `python-pptx`, retaining slide boundaries | LibreOffice PDF, then Gemini |
| PNG, JPEG, WebP, GIF, BMP, TIFF | None | Gemini image to HTML |

Select `hybrid_html` when some PDF pages have useful native text but page coverage is below `MIN_TEXT_PAGE_COVERAGE`. Send the whole PDF in the current implementation so Gemini preserves global reading order.

Configure thresholds through `MIN_NATIVE_TEXT_CHARS`, `MIN_PAGE_TEXT_CHARS`, `MIN_TEXT_PAGE_COVERAGE`, and `MIN_PRINTABLE_RATIO`. Calibrate them with representative documents rather than weakening them for one malformed file.
