import pytest
import uuid
import math
from datetime import datetime, timedelta
from core.memory import Memory, MemoryManager


@pytest.fixture
def memory_manager():
    return MemoryManager(capacity=3)


@pytest.fixture
def sample_memory():
    return Memory(
        id=uuid.uuid4(),
        timestamp=datetime.now(),
        content="Sample memory",
        importance=5.0,
        tags=["test", "memory"],
    )


def test_memory_creation(sample_memory):
    assert isinstance(sample_memory.id, uuid.UUID)
    assert isinstance(sample_memory.timestamp, datetime)
    assert sample_memory.content == "Sample memory"
    assert math.isclose(sample_memory.importance, 5.0, rel_tol=1e-9)
    assert sample_memory.tags == ["test", "memory"]
    assert sample_memory.related_entities == []


def test_add_memory(memory_manager, sample_memory):
    memory_manager.add_memory(sample_memory)
    assert len(memory_manager.memories) == 1
    assert memory_manager.memories[0] == sample_memory


def test_clean_memories(memory_manager):
    # Add memories with varying importance
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

    memory_manager.add_memory(mem1)
    memory_manager.add_memory(mem2)
    memory_manager.add_memory(mem3)

    assert len(memory_manager.memories) == 3

    # Add another memory to trigger cleaning
    mem4 = Memory(
        id=uuid.uuid4(),
        timestamp=datetime.now(),
        content="Memory 4",
        importance=0.5,
        tags=["d"],
    )
    memory_manager.add_memory(mem4)

    # After adding mem4, mem1 (the lowest importance) should be removed
    assert len(memory_manager.memories) == 3
    assert mem1 not in memory_manager.memories


def test_decay_memory(memory_manager):
    # Add a memory with a specific timestamp and importance
    past_time = datetime.now() - timedelta(hours=10)
    mem = Memory(
        id=uuid.uuid4(),
        timestamp=past_time,
        content="Old Memory",
        importance=5.0,
        tags=["e"],
    )

    memory_manager.add_memory(mem)

    # Decay the memory
    memory_manager.decay_memory()

    # Check if the importance has decayed correctly
    assert mem.importance < 5.0  # It should have decayed
