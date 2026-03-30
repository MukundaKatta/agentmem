"""agent-memory-kit: Lightweight, pluggable memory management for AI agents."""

from .memory import AgentMemory, AsyncAgentMemory
from .consolidation import ConsolidationStrategy

__version__ = "0.1.0"
__all__ = ["AgentMemory", "AsyncAgentMemory", "ConsolidationStrategy"]
