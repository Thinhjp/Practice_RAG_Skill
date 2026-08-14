import pytest

from app.modules import chunking


def test_simple_chunking_preserves_overlap():
    text = "abcdefghijklmnopqrstuvwxyz"
    chunks = chunking.split_text_simple(text, chunk_size=10, overlap=3)
    assert chunks[0][-3:] == chunks[1][:3]
    assert all(chunks)


def test_sentence_chunking_and_metadata():
    text = "Câu đầu tiên. Câu thứ hai khá dài. Câu cuối cùng."
    pieces = chunking.split_text_by_sentences(text, chunk_size=35, overlap=15)
    chunks = chunking.add_chunk_metadata(pieces, "source-a", "doc.txt")
    assert len(chunks) >= 2
    assert len({item["chunk_id"] for item in chunks}) == len(chunks)
    assert {item["document_id"] for item in chunks} == {chunks[0]["document_id"]}
    assert [item["chunk_index"] for item in chunks] == list(range(len(chunks)))


@pytest.mark.parametrize("size,overlap", [(0, 0), (10, -1), (10, 10)])
def test_invalid_chunk_settings(size, overlap):
    with pytest.raises(ValueError):
        chunking.split_text_simple("content", size, overlap)
