import pytest
from unittest.mock import MagicMock, patch
from agent_platform.planner.planner import Planner
from agent_platform.planner.dag import TaskDAG, TaskNode


def test_plan_returns_task_dag(mock_anthropic_response):
    planner = Planner(client=mock_anthropic_response)
    dag = planner.plan("Research and email top 3 leads")
    assert isinstance(dag, TaskDAG)
    assert len(dag.nodes) > 0


def test_plan_nodes_have_prompts(mock_anthropic_response):
    planner = Planner(client=mock_anthropic_response)
    dag = planner.plan("Do something complex")
    for node in dag.nodes:
        assert node.prompt
        assert node.id
