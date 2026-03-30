"""Abstract base class for memory storage backends."""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..utils import MemoryEntry


class BaseBackend(ABC):
    """Abstract interface for memory storage backends."""

    @abstractmethod
    def store(self, entry: MemoryEntry) -> None:
        """Store a memory entry."""
        ...

    @abstractmethod
    def retrieve(self, limit: int = 10, offset: int = 0) -> List[MemoryEntry]:
        """Retrieve recent memory entries."""
        ...

    @abstractmethod
    def search_by_content(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        """Search memories by text content."""
        ...

    @abstractmethod
    def get_all(self) -> List[MemoryEntry]:
        """Retrieve all stored memories."""
        ...

    @abstractmethod
    def delete(self, entry_id: str) -> bool:
        """Delete a memory entry by ID."""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Clear all stored memories."""
        ...

    @abstractmethod
    def count(self) -> int:
        """Return the number of stored memories."""
        ...
