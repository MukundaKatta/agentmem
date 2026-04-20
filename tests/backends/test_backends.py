from pathlib import Path

from agent_memory_kit import InMemoryBackend, MemoryEntry, SQLiteBackend


def make_entry(role: str, content: str, *, timestamp: float, entry_id: str) -> MemoryEntry:
    return MemoryEntry(
        role=role,
        content=content,
        timestamp=timestamp,
        entry_id=entry_id,
        tags=["test"],
        metadata={"source": "tests"},
    )


def test_in_memory_backend_crud_and_ordering():
    backend = InMemoryBackend()
    older = make_entry("user", "older memory", timestamp=1.0, entry_id="old")
    newer = make_entry("assistant", "newer memory", timestamp=2.0, entry_id="new")

    backend.store(older)
    backend.store(newer)

    assert backend.count() == 2
    assert [entry.entry_id for entry in backend.retrieve(limit=2)] == ["new", "old"]
    assert backend.search_by_content("older", top_k=1)[0].entry_id == "old"
    assert backend.delete("old") is True
    assert backend.count() == 1
    backend.clear()
    assert backend.count() == 0


def test_sqlite_backend_persists_entries_across_instances(tmp_path: Path):
    db_path = tmp_path / "agentmem.sqlite3"
    entry = make_entry("user", "remember this across restarts", timestamp=3.0, entry_id="persisted")

    backend = SQLiteBackend(str(db_path))
    backend.store(entry)
    backend.close()

    reopened = SQLiteBackend(str(db_path))
    entries = reopened.retrieve(limit=5)

    assert reopened.count() == 1
    assert entries[0].entry_id == "persisted"
    assert entries[0].metadata == {"source": "tests"}
    reopened.close()


def test_sqlite_backend_search_delete_and_clear(tmp_path: Path):
    db_path = tmp_path / "agentmem.sqlite3"
    backend = SQLiteBackend(str(db_path))
    first = make_entry("user", "python memory", timestamp=1.0, entry_id="first")
    second = make_entry("assistant", "sqlite memory", timestamp=2.0, entry_id="second")

    backend.store(first)
    backend.store(second)

    assert [entry.entry_id for entry in backend.search_by_content("memory", top_k=5)] == ["second", "first"]
    assert backend.delete("first") is True
    assert backend.delete("missing") is False
    assert backend.count() == 1
    backend.clear()
    assert backend.count() == 0
    backend.close()
