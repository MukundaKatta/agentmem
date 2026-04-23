"""In-memory storage backend - fast, ephemeral storage."""

from .base import BaseBackend
from ..utils import MemoryEntry


class InMemoryBackend(BaseBackend):
    """Store memories in a Python list. Fast but not persistent."""

    def __init__(self):
        self._entries: list[MemoryEntry] = []

    def store(self, entry: MemoryEntry) -> None:
        self._entries.append(entry)

    def retrieve(self, limit: int = 10, offset: int = 0) -> list[MemoryEntry]:
        sorted_entries = sorted(self._entries, key=lambda e: e.timestamp, reverse=True)
        return sorted_entries[offset : offset + limit]

    def search_by_content(self, query: str, top_k: int = 5) -> list[MemoryEntry]:
        query_lower = query.lower()
        matches = [e for e in self._entries if query_lower in e.content.lower()]
        return sorted(matches, key=lambda e: e.timestamp, reverse=True)[:top_k]

    def get_all(self) -> list[MemoryEntry]:
        return list(self._entries)

    def delete(self, entry_id: str) -> bool:
        for i, entry in enumerate(self._entries):
            if entry.entry_id == entry_id:
                self._entries.pop(i)
                return True
        return False

    def clear(self) -> None:
        self._entries.clear()

    def count(self) -> int:
        return len(self._entries)
