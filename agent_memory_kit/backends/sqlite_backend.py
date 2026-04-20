"""SQLite-backed persistent memory storage."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import List

from .base import BaseBackend
from ..utils import MemoryEntry


class SQLiteBackend(BaseBackend):
    """Store memories in a local SQLite database."""

    def __init__(self, db_path: str = "agentmem.db"):
        self.db_path = str(Path(db_path))
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._create_schema()

    def _create_schema(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                entry_id TEXT PRIMARY KEY,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp REAL NOT NULL,
                token_count INTEGER NOT NULL,
                relevance_score REAL NOT NULL,
                tags TEXT NOT NULL,
                metadata TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    def _row_to_entry(self, row: sqlite3.Row) -> MemoryEntry:
        return MemoryEntry(
            role=row["role"],
            content=row["content"],
            timestamp=row["timestamp"],
            token_count=row["token_count"],
            relevance_score=row["relevance_score"],
            tags=json.loads(row["tags"]),
            metadata=json.loads(row["metadata"]),
            entry_id=row["entry_id"],
        )

    def store(self, entry: MemoryEntry) -> None:
        self._conn.execute(
            """
            INSERT OR REPLACE INTO memories (
                entry_id, role, content, timestamp, token_count,
                relevance_score, tags, metadata
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry.entry_id,
                entry.role,
                entry.content,
                entry.timestamp,
                entry.token_count,
                entry.relevance_score,
                json.dumps(entry.tags),
                json.dumps(entry.metadata),
            ),
        )
        self._conn.commit()

    def retrieve(self, limit: int = 10, offset: int = 0) -> List[MemoryEntry]:
        cursor = self._conn.execute(
            """
            SELECT * FROM memories
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        )
        return [self._row_to_entry(row) for row in cursor.fetchall()]

    def search_by_content(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        cursor = self._conn.execute(
            """
            SELECT * FROM memories
            WHERE lower(content) LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (f"%{query.lower()}%", top_k),
        )
        return [self._row_to_entry(row) for row in cursor.fetchall()]

    def get_all(self) -> List[MemoryEntry]:
        cursor = self._conn.execute(
            """
            SELECT * FROM memories
            ORDER BY timestamp ASC
            """
        )
        return [self._row_to_entry(row) for row in cursor.fetchall()]

    def delete(self, entry_id: str) -> bool:
        cursor = self._conn.execute(
            "DELETE FROM memories WHERE entry_id = ?",
            (entry_id,),
        )
        self._conn.commit()
        return cursor.rowcount > 0

    def clear(self) -> None:
        self._conn.execute("DELETE FROM memories")
        self._conn.commit()

    def count(self) -> int:
        cursor = self._conn.execute("SELECT COUNT(*) FROM memories")
        return int(cursor.fetchone()[0])

    def close(self) -> None:
        self._conn.close()

    def __del__(self) -> None:
        try:
            self._conn.close()
        except Exception:
            pass
