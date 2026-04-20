"""Public exports for agentmem."""

from .backends import BaseBackend, InMemoryBackend, SQLiteBackend
from .utils import (
    MemoryEntry,
    cosine_similarity,
    estimate_tokens,
    simple_text_embedding,
    truncate_to_tokens,
)

__version__ = "0.1.0"
__all__ = [
    "BaseBackend",
    "InMemoryBackend",
    "SQLiteBackend",
    "MemoryEntry",
    "cosine_similarity",
    "estimate_tokens",
    "simple_text_embedding",
    "truncate_to_tokens",
]
