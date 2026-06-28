import pytest
from agent_platform.tools.registry import ToolRegistry

def test_register_and_get_tool():
    registry = ToolRegistry()
    tool = {
        "name": "test_tool",
        "description": "A test tool",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    }
    registry.register(tool, handler=lambda **kwargs: "test result")
    tools = registry.get_all()
    assert len(tools) == 1
    assert tools[0]["name"] == "test_tool"

def test_execute_tool_calls_handler():
    registry = ToolRegistry()
    registry.register(
        {"name": "add", "description": "Adds two numbers",
         "input_schema": {"type": "object", "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}}, "required": ["a", "b"]}},
        handler=lambda a, b: str(a + b)
    )
    result = registry.execute("add", {"a": 3, "b": 4})
    assert result == "7"

def test_execute_unknown_tool_raises():
    registry = ToolRegistry()
    with pytest.raises(KeyError):
        registry.execute("nonexistent", {})
