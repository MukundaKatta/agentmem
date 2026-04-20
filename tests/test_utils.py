from agent_memory_kit import (
    MemoryEntry,
    cosine_similarity,
    estimate_tokens,
    simple_text_embedding,
    truncate_to_tokens,
)


def test_memory_entry_populates_defaults():
    entry = MemoryEntry(role="user", content="Hello there", tags=["intro"], metadata={"source": "test"})

    assert entry.entry_id.startswith("mem_")
    assert entry.token_count > 0
    assert entry.tags == ["intro"]
    assert entry.metadata == {"source": "test"}


def test_estimate_tokens_for_empty_text():
    assert estimate_tokens("") == 0


def test_truncate_to_tokens_marks_truncation():
    text = "Sentence one. Sentence two is a bit longer. Sentence three keeps going."

    truncated = truncate_to_tokens(text, max_tokens=6)

    assert truncated.endswith(" [truncated]")
    assert len(truncated) < len(text) + len(" [truncated]")


def test_cosine_similarity_handles_zero_vectors():
    assert cosine_similarity([0.0, 0.0], [1.0, 2.0]) == 0.0


def test_simple_text_embedding_returns_requested_dimension():
    embedding = simple_text_embedding("agent memory", dim=32)

    assert len(embedding) == 32
    assert any(value != 0.0 for value in embedding)
