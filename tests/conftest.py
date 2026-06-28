import pytest
from unittest.mock import MagicMock
import json


@pytest.fixture
def mock_anthropic_response():
    client = MagicMock()
    dag_json = json.dumps({
        "nodes": [
            {"id": "t1", "prompt": "Research lead 1", "depends_on": []},
            {"id": "t2", "prompt": "Draft email for lead 1", "depends_on": ["t1"]}
        ]
    })
    client.messages.create.return_value.content = [
        MagicMock(type="text", text=dag_json)
    ]
    return client
