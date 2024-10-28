import uuid
from dataclasses import dataclass, field
from typing import List
from datetime import datetime


@dataclass
class Memory:
    id: uuid.UUID
    timestamp: datetime
    content: str
    importance: float
    tags: List[str]
    related_entities: List[str] = field(default_factory=list)


class MemoryManager:
    def __init__(self, capacity: int = 1000, decay_rate: int = 0.1):
        self.memories: List[Memory] = []
        self.capacity = capacity
        self.decay_rate = decay_rate

    def add_memory(self, memory: Memory) -> None:
        if len(self.memories) >= self.capacity:
            self.clean_memories()
        self.memories.append(memory)

    def clean_memories(self) -> None:
        min_importance: float = float('inf')
        earliest_memory: Memory = self.memories[0]

        for memory in self.memories:
            if memory.importance < min_importance:
                min_importance = memory.importance
                earliest_memory = memory  # Reset to current memory if a new minimum is found
            elif memory.importance == min_importance:
                # Compare timestamps if importance is the same
                if earliest_memory is None or memory.timestamp < earliest_memory.timestamp:
                    earliest_memory = memory

        self.memories.remove(earliest_memory)

    def decay_memory(self) -> None:
        current_time = datetime.now()

        memories_to_remove = []

        for memory in self.memories:
            time_passed = (current_time - memory.timestamp).total_seconds() / 3600.0
            decay_rate = 1.0 / (memory.importance + 1e-5)
            memory.importance -= decay_rate * time_passed
            if memory.importance <= 0:
                memories_to_remove.append(memory)

        for memory in memories_to_remove:
            self.memories.remove(memory)
