"""Sanitize Gemini HTML and split it along document structure."""

import re
from dataclasses import dataclass
from typing import Any

from bs4 import BeautifulSoup, Comment, Tag

from app.modules import chunking


ALLOWED_TAGS = {
    "article", "section", "h1", "h2", "h3", "h4", "h5", "h6", "p",
    "ul", "ol", "li", "table", "thead", "tbody", "tfoot", "tr", "th", "td",
    "blockquote", "pre", "code", "figure", "figcaption", "strong", "em", "br",
}
DROP_TAGS = {"script", "style", "iframe", "object", "embed", "link", "meta", "svg"}
ALLOWED_ATTRIBUTES = {"data-page", "data-section-id", "rowspan", "colspan"}
BLOCK_TAGS = {
    "h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "table", "blockquote",
    "pre", "figcaption",
}


def _strip_markdown_fence(value: str) -> str:
    stripped = value.strip()
    match = re.fullmatch(r"```(?:html)?\s*(.*?)\s*```", stripped, flags=re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else stripped


def sanitize_html(value: str) -> str:
    soup = BeautifulSoup(_strip_markdown_fence(value), "html.parser")
    for comment in soup.find_all(string=lambda item: isinstance(item, Comment)):
        comment.extract()
    for tag in soup.find_all(DROP_TAGS):
        tag.decompose()
    for tag in list(soup.find_all(True)):
        if tag.name not in ALLOWED_TAGS:
            tag.unwrap()
            continue
        cleaned: dict[str, str] = {}
        for key, raw_value in tag.attrs.items():
            if key not in ALLOWED_ATTRIBUTES:
                continue
            value_text = " ".join(raw_value) if isinstance(raw_value, list) else str(raw_value)
            if key in {"rowspan", "colspan"} and not value_text.isdigit():
                continue
            cleaned[key] = value_text[:100]
        tag.attrs = cleaned

    article = soup.find("article")
    if article is None:
        contents = "".join(str(item) for item in soup.contents)
        soup = BeautifulSoup(f"<article>{contents}</article>", "html.parser")
        article = soup.article
    if article is None or not article.get_text(" ", strip=True):
        raise ValueError("Converted HTML contains no readable text")
    return str(article)


def html_to_text(value: str) -> str:
    soup = BeautifulSoup(value, "html.parser")
    lines = [line.strip() for line in soup.get_text("\n").splitlines()]
    return "\n".join(line for line in lines if line).strip()


@dataclass
class _Block:
    text: str
    page: str | None
    heading_path: list[str]
    tag: str


def _nearest_page(tag: Tag) -> str | None:
    current: Tag | None = tag
    while current is not None:
        if current.has_attr("data-page"):
            return str(current["data-page"])
        current = current.parent if isinstance(current.parent, Tag) else None
    return None


def _blocks(value: str) -> list[_Block]:
    soup = BeautifulSoup(value, "html.parser")
    headings: list[str] = []
    result: list[_Block] = []
    for tag in soup.find_all(BLOCK_TAGS):
        if any(isinstance(parent, Tag) and parent.name in BLOCK_TAGS for parent in tag.parents):
            continue
        text = " ".join(tag.get_text(" ", strip=True).split())
        if not text:
            continue
        if re.fullmatch(r"h[1-6]", tag.name):
            level = int(tag.name[1])
            headings = headings[: level - 1]
            headings.append(text)
        result.append(_Block(text, _nearest_page(tag), list(headings), tag.name))
    return result


def prepare_html_chunks(
    html: str,
    source: str,
    file_name: str,
    *,
    document_id: str,
    metadata: dict[str, Any] | None = None,
) -> list[dict]:
    """Pack semantic HTML blocks while retaining page and heading breadcrumbs."""
    blocks = _blocks(html)
    if not blocks:
        return []
    pieces: list[tuple[str, _Block]] = []
    current_texts: list[str] = []
    current_block: _Block | None = None

    def flush() -> None:
        nonlocal current_texts, current_block
        if current_texts and current_block is not None:
            pieces.append(("\n\n".join(current_texts), current_block))
        current_texts = []
        current_block = None

    for block in blocks:
        if len(block.text) > chunking.config.CHUNK_SIZE:
            flush()
            for fragment in chunking.split_text_simple(block.text):
                pieces.append((fragment, block))
            continue
        candidate = "\n\n".join([*current_texts, block.text])
        page_changed = current_block is not None and block.page != current_block.page
        if current_texts and (len(candidate) > chunking.config.CHUNK_SIZE or page_changed):
            flush()
        if current_block is None:
            current_block = block
        current_texts.append(block.text)
    flush()

    result = chunking.add_chunk_metadata(
        [text for text, _ in pieces],
        source,
        file_name,
        document_id=document_id,
        extra_metadata=metadata,
    )
    for item, (_, block) in zip(result, pieces):
        item["page"] = block.page
        item["heading_path"] = block.heading_path
        item["content_tag"] = block.tag
    return result
