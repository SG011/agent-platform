import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from fastapi.testclient import TestClient
from agent_platform.planner.dag import TaskDAG, TaskNode


@pytest.fixture
def client():
    mock_anthropic = MagicMock()
    with patch("anthropic.Anthropic", return_value=mock_anthropic):
        from agent_platform.api import app as app_module
        import importlib
        importlib.reload(app_module)
        yield TestClient(app_module.app)


def test_health_returns_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_create_run_returns_run_id_and_results(client):
    mock_dag = TaskDAG(nodes=[TaskNode(id="t1", prompt="Do something", depends_on=[])])
    from agent_platform.api import app as app_module

    app_module._planner.plan = MagicMock(return_value=mock_dag)
    app_module._executor.execute = AsyncMock(return_value={"t1": "task result"})

    resp = client.post("/runs", json={"goal": "Research something"})
    assert resp.status_code == 200
    data = resp.json()
    assert "run_id" in data
    assert "results" in data
    assert data["results"]["t1"] == "task result"
