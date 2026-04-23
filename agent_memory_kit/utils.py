"""Utility functions for token counting and text processing."""

import re
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MemoryEntry:
    """A single memory entry with metadata."""

    role: str
    content: str
    timestamp: float = field(default_factory=time.time)
    token_count: int = 0
    relevance_score: float = 1.0
    tags: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    entry_id: Optional[str] = None

    def __post_init__(self):
        if self.token_count == 0:
            self.token_count = estimate_tokens(self.content)
        if self.entry_id is None:
            self.entry_id = f"mem_{uuid.uuid4().hex}"


def estimate_tokens(text: str) -> int:
    """Estimate token count using a simple heuristic."""
    if not text:
        return 0
    words = len(re.findall(r"\S+", text))
    chars = len(text)
    return max(1, int((words + chars / 4) / 2))


def truncate_to_tokens(text: str, max_tokens: int) -> str:
    """Truncate text to approximately fit within a token budget."""
    current_tokens = estimate_tokens(text)
    if current_tokens <= max_tokens:
        return text
    ratio = max_tokens / current_tokens
    target_chars = int(len(text) * ratio * 0.9)
    truncated = text[:target_chars]
    last_period = truncated.rfind(".")
    last_newline = truncated.rfind("\n")
    break_point = max(last_period, last_newline)
    if break_point > target_chars * 0.5:
        truncated = truncated[: break_point + 1]
    return truncated + " [truncated]"


def cosine_similarity(vec_a, vec_b) -> float:
    """Compute cosine similarity between two vectors."""
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same length.")
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot / (norm_a * norm_b))


def simple_text_embedding(text: str, dim: int = 128) -> list:
    """Generate a simple bag-of-characters embedding for text."""
    text = text.lower().strip()
    vec = [0.0] * dim
    for i, char in enumerate(text):
        idx = ord(char) % dim
        vec[idx] += 1.0 / (1 + i * 0.01)
    words = text.split()
    for i, word in enumerate(words):
        word_hash = hash(word) % dim
        vec[word_hash] += 2.0 / (1 + i * 0.05)
    bigrams = [text[i : i + 2] for i in range(len(text) - 1)]
    for bigram in bigrams:
        bg_hash = hash(bigram) % dim
        vec[bg_hash] += 0.5
    norm = sum(value * value for value in vec) ** 0.5
    if norm > 0:
        vec = [value / norm for value in vec]
    return vec
