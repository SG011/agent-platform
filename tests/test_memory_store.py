import pytest
import fakeredis
from agent_platform.memory.store import MemoryStore

@pytest.fixture
def store():
    client = fakeredis.FakeRedis(decode_responses=True)
    return MemoryStore(client=client)

def test_save_and_get_result(store):
    store.save("run-1", "task-1", "The answer is 42")
    result = store.get("run-1", "task-1")
    assert result == "The answer is 42"

def test_get_missing_returns_none(store):
    assert store.get("run-1", "nonexistent") is None

def test_get_all_results(store):
    store.save("run-2", "t1", "result1")
    store.save("run-2", "t2", "result2")
    all_results = store.get_all_results("run-2")
    assert all_results == {"t1": "result1", "t2": "result2"}
