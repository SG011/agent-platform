import pytest
from agent_platform.planner.dag import TaskNode, TaskDAG

def test_get_ready_tasks_returns_nodes_with_no_deps():
    dag = TaskDAG(nodes=[
        TaskNode(id="t1", prompt="First task", depends_on=[]),
        TaskNode(id="t2", prompt="Second task", depends_on=["t1"]),
    ])
    ready = dag.get_ready_tasks(completed=set())
    assert len(ready) == 1
    assert ready[0].id == "t1"

def test_get_ready_tasks_after_t1_complete_returns_t2():
    dag = TaskDAG(nodes=[
        TaskNode(id="t1", prompt="First task", depends_on=[]),
        TaskNode(id="t2", prompt="Second task", depends_on=["t1"]),
    ])
    ready = dag.get_ready_tasks(completed={"t1"})
    assert len(ready) == 1
    assert ready[0].id == "t2"

def test_is_complete_when_all_done():
    dag = TaskDAG(nodes=[
        TaskNode(id="t1", prompt="p1", depends_on=[]),
        TaskNode(id="t2", prompt="p2", depends_on=["t1"]),
    ])
    assert dag.is_complete({"t1", "t2"}) is True
    assert dag.is_complete({"t1"}) is False
