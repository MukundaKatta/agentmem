# agentmem

`agentmem` is a lightweight memory primitives library for AI agents, focused on storage backends, memory entries, token-aware utilities, and simple retrieval foundations without the overhead of a full framework.

Memory is one of the hardest parts of building useful agent systems. Agents need a way to store context, retrieve relevant past interactions, and stay within token budgets without forcing every project into the same monolithic architecture. `agentmem` is aimed at that lower layer: practical building blocks you can compose into your own agent stack.

## Why agentmem

Many agent libraries bundle memory into a larger framework. That can be convenient, but it can also make memory hard to reuse outside that ecosystem.

`agentmem` takes a smaller and more modular approach:

- memory entry primitives with metadata
- pluggable backend interfaces
- a simple in-memory backend for fast iteration
- token estimation and truncation helpers
- lightweight embedding and similarity utilities for retrieval experiments

## Current Status

`agentmem` is currently an early-stage library.

The repository already includes the core foundations for memory entries, backend abstractions, and utility helpers. Higher-level memory orchestration APIs are still planned, but the current package is best understood as a composable base layer rather than a full end-to-end memory framework.

## What Is Available Today

- `MemoryEntry` dataclass for storing content and metadata
- `BaseBackend` abstract interface for memory storage implementations
- `InMemoryBackend` for fast, ephemeral storage
- token estimation and truncation utilities
- cosine similarity and simple text embedding helpers

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
from agent_memory_kit import InMemoryBackend, MemoryEntry

backend = InMemoryBackend()

backend.store(MemoryEntry(role="user", content="My name is Alice."))
backend.store(MemoryEntry(role="assistant", content="Nice to meet you, Alice."))
backend.store(MemoryEntry(role="user", content="I need help writing a Python script."))

recent = backend.retrieve(limit=2)
matches = backend.search_by_content("python", top_k=3)

for entry in recent:
    print(entry.role, entry.content)
```

## Utility Helpers

```python
from agent_memory_kit import estimate_tokens, simple_text_embedding, truncate_to_tokens

text = "This is a long memory entry that may need trimming."

token_estimate = estimate_tokens(text)
trimmed = truncate_to_tokens(text, max_tokens=10)
embedding = simple_text_embedding(text)
```

## Architecture

```text
agentmem/
├── agent_memory_kit/
│   ├── __init__.py          # Public exports
│   ├── utils.py             # MemoryEntry + token and embedding helpers
│   └── backends/
│       ├── base.py          # Abstract backend interface
│       └── in_memory.py     # In-memory storage backend
├── setup.py
└── README.md
```

## Project Direction

Over time, `agentmem` is intended to grow toward:

- additional storage backends
- higher-level memory managers
- stronger retrieval strategies
- practical consolidation and decay policies
- easier integration into agent runtimes and workflow systems

## Who This Is For

- developers building their own agent runtime
- teams that want reusable memory primitives without adopting a full framework
- experimenters working on context management and retrieval behavior
- anyone who wants a simpler starting point for agent memory systems

## Contributing

Contributions are welcome, especially around:

- backend implementations
- retrieval quality improvements
- memory lifecycle policies
- tests and examples
- documentation and developer experience

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
