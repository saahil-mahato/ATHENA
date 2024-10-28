"""
This module implements a memory management system for intelligent NPCs (Non-Player Characters).
It allows for the creation, storage, and decay of memories based on their importance and timestamps.

Classes:
- Memory: Represents a single memory entry.
- MemoryManager: Manages a collection of Memory objects, including adding, cleaning, and decaying memories.

Usage:
1. Create instances of Memory using the Memory class.
2. Use the MemoryManager class to add and manage these memories.
"""

import uuid
from dataclasses import dataclass, field
from typing import List
from datetime import datetime


@dataclass
class Memory:
    """Represents a single memory entry."""

    id: uuid.UUID  # Unique identifier for the memory
    timestamp: datetime  # Time when the memory was created
    content: str  # Content of the memory
    importance: float  # Importance level of the memory (higher is more important)
    tags: List[str]  # Tags associated with the memory for categorization
    related_entities: List[str] = field(
        default_factory=list
    )  # Entities related to the memory


class MemoryManager:
    """Manages a collection of Memory objects."""

    def __init__(self, capacity: int = 1000, decay_rate: int = 0.1):
        """
        Initializes the MemoryManager with a specified capacity and decay rate.

        Parameters:
        - capacity (int): Maximum number of memories to store. Defaults to 1000.
        - decay_rate (float): Rate at which memories decay over time. Defaults to 0.1.
        """
        self.memories: List[Memory] = []  # List to hold Memory objects
        self.capacity = capacity  # Maximum number of memories allowed
        self.decay_rate = decay_rate  # Rate at which memories lose importance

    def add_memory(self, memory: Memory) -> None:
        """
        Adds a new memory to the manager. If capacity is exceeded, it cleans up less important memories.

        Parameters:
        - memory (Memory): The Memory object to be added.
        """
        if len(self.memories) >= self.capacity:
            self.clean_memories()  # Clean up memories if capacity is reached
        self.memories.append(memory)  # Add new memory

    def clean_memories(self) -> None:
        """Removes the least important memory from the manager."""

        min_importance: float = float(
            "inf"
        )  # Initialize minimum importance as infinity
        earliest_memory: Memory = self.memories[0]  # Start with the first memory

        for memory in self.memories:
            if memory.importance < min_importance:
                min_importance = memory.importance  # Update minimum importance found
                earliest_memory = (
                    memory  # Reset to current memory if a new minimum is found
                )
            elif memory.importance == min_importance:
                # Compare timestamps if importance is the same
                if (
                    earliest_memory is None
                    or memory.timestamp < earliest_memory.timestamp
                ):
                    earliest_memory = memory  # Update to earlier timestamp if necessary

        self.memories.remove(
            earliest_memory
        )  # Remove the least important or oldest memory

    def decay_memory(self) -> None:
        """Applies decay to all memories based on their age and importance."""

        current_time = datetime.now()  # Get current time

        memories_to_remove = []  # List to track memories that need removal

        for memory in self.memories:
            time_passed = (current_time - memory.timestamp).total_seconds() / 3600.0
            decay_rate = 1.0 / (
                memory.importance + 1e-5
            )  # Calculate decay rate based on importance

            # Decrease importance based on time passed and calculated decay rate
            memory.importance -= decay_rate * time_passed

            if memory.importance <= 0:
                memories_to_remove.append(
                    memory
                )  # Mark for removal if importance drops below zero

        for memory in memories_to_remove:
            self.memories.remove(memory)  # Remove decayed memories from the list
