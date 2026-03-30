# agentmem

A lightweight, pluggable memory management library for AI agents. Give your agents short-term, long-term, and semantic memory - without the complexity of a full framework.

## Why agentmem?

As agentic AI systems become the norm in 2026, one of the biggest challenges is **memory management**. Agents need to remember context across conversations, recall relevant past interactions, and forget what's no longer useful - all without blowing up token budgets.

`agentmem` solves this with a simple, modular approach:

- **Short-term memory** - sliding window buffer for recent context
- **Long-term memory** - persistent storage with automatic summarization
- **Semantic memory** - vector-based retrieval for finding relevant past interactions
- **Memory consolidation** - automatically compress and merge old memories to save tokens

## Features

- Drop-in memory management for any LLM-based agent
- Built-in support for multiple storage backends (in-memory, SQLite, JSON files)
- Semantic search using sentence embeddings
- Automatic memory decay and consolidation
- Token-aware memory trimming
- Simple Python API with async support
- Zero heavy dependencies for the core module

## Installation

```bash
pip install agentmem
```

Or install from source:

```bash
git clone https://github.com/MukundaKatta/agentmem.git
cd agentmem
pip install -e .
```

## Quick Start

```python
from agent_memory_kit import AgentMemory

# Create a memory instance
memory = AgentMemory(
    short_term_limit=20,
    long_term_backend="sqlite",
    enable_semantic=True
)

# Add memories
memory.add("user", "My name is Alice and I work at Acme Corp.")
memory.add("assistant", "Nice to meet you, Alice! How can I help you today?")
memory.add("user", "I need help writing a Python script for data analysis.")

# Get recent context (short-term)
recent = memory.get_recent(limit=5)

# Search semantically across all memories
results = memory.search("What company does the user work at?", top_k=3)

# Get a consolidated summary of long-term memories
summary = memory.get_summary()

# Token-aware context building
context = memory.build_context(max_tokens=4000)
```

## Advanced Usage

### Memory Consolidation

```python
from agent_memory_kit import AgentMemory, ConsolidationStrategy

memory = AgentMemory(
    consolidation=ConsolidationStrategy.SUMMARIZE,
    consolidation_threshold=50
)

memory.consolidate()
```

### Custom Storage Backend

```python
from agent_memory_kit import AgentMemory
from agent_memory_kit.backends import SQLiteBackend

backend = SQLiteBackend(db_path="my_agent_memory.db")
memory = AgentMemory(backend=backend)
```

### Async Support

```python
from agent_memory_kit import AsyncAgentMemory

memory = AsyncAgentMemory()
await memory.add("user", "Hello!")
results = await memory.search("greeting", top_k=5)
```

## Architecture

```
agentmem/
  agent_memory_kit/
    __init__.py          # Public API
    memory.py            # Core AgentMemory class
    backends/
      __init__.py
      base.py            # Abstract backend interface
      in_memory.py       # In-memory storage (default)
      sqlite_backend.py  # SQLite persistent storage
      json_backend.py    # JSON file storage
    semantic.py          # Semantic search module
    consolidation.py     # Memory consolidation strategies
    utils.py             # Token counting and helpers
```

## Contributing

Contributions are welcome! Here's how to get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built with inspiration from the agentic AI wave of 2026. Special thanks to the open-source AI community for pushing the boundaries of what agents can do.
