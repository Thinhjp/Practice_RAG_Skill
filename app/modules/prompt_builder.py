"""Build a provider-neutral grounded prompt from retrieved chunks."""

from typing import Dict, List


def build_prompt(question: str, contexts: List[Dict]) -> str:
    blocks = []
    for index, context in enumerate(contexts, start=1):
        blocks.append(
            f"[Nguồn {index}: {context.get('file_name', 'unknown')}]\n"
            f"{context.get('text', '')}"
        )
    joined = "\n\n".join(blocks) or "Không có ngữ cảnh liên quan."
    return (
        "Trả lời câu hỏi chỉ dựa trên ngữ cảnh. Nếu không đủ thông tin, hãy nói rõ. "
        "Trích dẫn nguồn bằng dạng [Nguồn N].\n\n"
        f"Ngữ cảnh:\n{joined}\n\nCâu hỏi: {question}\nTrả lời:"
    )
