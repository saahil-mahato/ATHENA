"""
This module contains unit tests for the memory management system implemented in the `core.memory` module.
It uses pytest framework for testing the Memory and MemoryManager classes.

Tests:
- Memory creation
- Adding memories to MemoryManager
- Cleaning up memories based on importance
- Decaying memory importance over time
"""

import pytest
import uuid
import math
from datetime import datetime, timedelta
from core.memory import Memory, MemoryManager


@pytest.fixture
def memory_manager():
    """Fixture that provides a MemoryManager instance with a capacity of 3."""
    return MemoryManager(capacity=3)


@pytest.fixture
def sample_memory():
    """Fixture that provides a sample Memory instance for testing."""
    return Memory(
        id=uuid.uuid4(),  # Generate a unique UUID for the memory
        timestamp=datetime.now(),  # Set current timestamp
        content="Sample memory",  # Sample content for the memory
        importance=5.0,  # Set initial importance
        tags=["test", "memory"],  # Tags associated with the memory
    )


def test_memory_creation(sample_memory):
    """Test the creation of a Memory object."""
    assert isinstance(sample_memory.id, uuid.UUID)  # Check if ID is a UUID
    assert isinstance(
        sample_memory.timestamp, datetime
    )  # Check if timestamp is a datetime object
    assert (
        sample_memory.content == "Sample memory"
    )  # Verify content matches expected value
    assert math.isclose(
        sample_memory.importance, 5.0, rel_tol=1e-9
    )  # Verify importance using relative tolerance
    assert sample_memory.tags == [
        "test",
        "memory",
    ]  # Check if tags match expected values
    assert (
        sample_memory.related_entities == []
    )  # Ensure related entities list is empty by default


def test_add_memory(memory_manager, sample_memory):
    """Test adding a Memory object to the MemoryManager."""
    memory_manager.add_memory(sample_memory)  # Add the sample memory to the manager
    assert len(memory_manager.memories) == 1  # Check that one memory has been added
    assert (
        memory_manager.memories[0] == sample_memory
    )  # Verify that the added memory is correct


def test_clean_memories(memory_manager):
    """Test the cleaning functionality of MemoryManager when capacity is exceeded."""

    # Create memories with varying importance levels
    mem1 = Memory(
        id=uuid.uuid4(),
        timestamp=datetime.now(),
        content="Memory 1",
        importance=1.0,
        tags=["a"],
    )
    mem2 = Memory(
        id=uuid.uuid4(),
        timestamp=datetime.now(),
        content="Memory 2",
        importance=2.0,
        tags=["b"],
    )
    mem3 = Memory(
        id=uuid.uuid4(),
        timestamp=datetime.now(),
        content="Memory 3",
        importance=3.0,
        tags=["c"],
    )

    # Add memories to the manager
    memory_manager.add_memory(mem1)
    memory_manager.add_memory(mem2)
    memory_manager.add_memory(mem3)

    assert len(memory_manager.memories) == 3  # Ensure all three memories are stored

    # Add another memory to trigger cleaning due to capacity limit
    mem4 = Memory(
        id=uuid.uuid4(),
        timestamp=datetime.now(),
        content="Memory 4",
        importance=0.5,
        tags=["d"],
    )

    memory_manager.add_memory(mem4)  # Add fourth memory

    # After adding mem4, mem1 (the lowest importance) should be removed due to cleaning logic
    assert (
        len(memory_manager.memories) == 3
    )  # Ensure capacity remains at limit after cleaning
    assert mem1 not in memory_manager.memories  # Verify that mem1 has been removed


def test_decay_memory(memory_manager):
    """Test the decay functionality of MemoryManager on an existing memory."""

    # Create a memory with a specific timestamp and importance level
    past_time = datetime.now() - timedelta(hours=10)  # Set timestamp to 10 hours ago
    mem = Memory(
        id=uuid.uuid4(),
        timestamp=past_time,
        content="Old Memory",
        importance=5.0,
        tags=["e"],
    )

    memory_manager.add_memory(mem)  # Add memory to manager

    # Decay the memory's importance based on its age and decay rate
    memory_manager.decay_memory()

    # Check if the importance has decayed correctly (it should be less than initial)
    assert mem.importance < 5.0  # It should have decayed from its original value
