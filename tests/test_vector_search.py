import numpy as np

from app.modules import chunking, embedding, search, vector_db


def _embedded_documents():
    texts = [
        ("cats.txt", "Mèo thích ăn cá và thường ngủ vào ban ngày."),
        ("python.txt", "Python là ngôn ngữ lập trình dùng để xây dựng FastAPI."),
    ]
    chunks = []
    for name, text in texts:
        prepared = chunking.prepare_chunks(text, f"source/{name}", name)
        chunks.extend(embedding.embed_chunks(prepared))
    return chunks


def test_vector_db_round_trip_and_search():
    chunks = _embedded_documents()
    vectors, metadata = vector_db.add_to_vector_db(chunks)
    assert vectors is not None
    vector_db.save_vector_db(vectors, metadata)

    loaded_vectors, loaded_metadata = vector_db.load_vector_db()
    np.testing.assert_allclose(loaded_vectors, vectors)
    assert loaded_metadata == metadata

    results = search.search_similar_chunks(
        "mèo ăn cá", loaded_vectors, loaded_metadata, top_k=1, threshold=-1
    )
    assert results[0]["file_name"] == "cats.txt"


def test_context_does_not_cross_document_boundary():
    chunks = _embedded_documents()
    _, metadata = vector_db.add_to_vector_db(chunks)
    target = metadata[0]
    context = search.retrieve_context(target["chunk_id"], metadata, context_size=5)
    assert all(
        item["document_id"] == target["document_id"]
        for item in context["context_before"] + context["context_after"]
    )


def test_zero_vector_similarity_is_safe():
    zero = np.zeros(3, dtype=np.float32)
    assert search.calculate_similarity(zero, zero) == 0.0
