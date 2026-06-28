import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from agent_platform.planner.dag import TaskDAG, TaskNode
from agent_platform.executor.executor import AgentExecutor
from agent_platform.memory.store import MemoryStore
from agent_platform.tools.registry import ToolRegistry
import fakeredis

@pytest.fixture
def memory_store():
    client = fakeredis.FakeRedis(decode_responses=True)
    return MemoryStore(client=client)

@pytest.fixture
def mock_worker():
    worker = MagicMock()
    worker.run = AsyncMock(return_value="task completed successfully")
    return worker

@pytest.mark.asyncio
async def test_execute_single_task_dag(memory_store, mock_worker):
    dag = TaskDAG(nodes=[TaskNode(id="t1", prompt="Do something", depends_on=[])])
    executor = AgentExecutor(memory_store=memory_store, worker=mock_worker)
    results = await executor.execute(dag, run_id="run-test-1")
    assert "t1" in results
    assert results["t1"] == "task completed successfully"

@pytest.mark.asyncio
async def test_execute_respects_dependency_order(memory_store, mock_worker):
    dag = TaskDAG(nodes=[
        TaskNode(id="t1", prompt="First", depends_on=[]),
        TaskNode(id="t2", prompt="Second", depends_on=["t1"]),
    ])
    call_order = []
    async def tracked_run(task, context):
        call_order.append(task.id)
        return f"result-{task.id}"
    mock_worker.run = tracked_run
    executor = AgentExecutor(memory_store=memory_store, worker=mock_worker)
    results = await executor.execute(dag, run_id="run-test-2")
    assert call_order.index("t1") < call_order.index("t2")
    assert results == {"t1": "result-t1", "t2": "result-t2"}
