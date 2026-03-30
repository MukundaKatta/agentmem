"""Utility functions for token counting and text processing."""

import re
import time
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
    tags: list = field(default_factory=list)
    entry_id: Optional[str] = None

    def __post_init__(self):
        if self.token_count == 0:
            self.token_count = estimate_tokens(self.content)
        if self.entry_id is None:
            self.entry_id = f"mem_{int(self.timestamp * 1000)}"


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
    import numpy as np
    a = np.array(vec_a, dtype=np.float32)
    b = np.array(vec_b, dtype=np.float32)
    dot = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot / (norm_a * norm_b))


def simple_text_embedding(text: str, dim: int = 128) -> list:
    """Generate a simple bag-of-characters embedding for text."""
    import numpy as np
    text = text.lower().strip()
    vec = np.zeros(dim, dtype=np.float32)
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
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec.tolist()
