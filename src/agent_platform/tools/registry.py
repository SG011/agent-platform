from typing import Callable


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, dict] = {}
        self._handlers: dict[str, Callable] = {}

    def register(self, tool: dict, handler: Callable) -> None:
        self._tools[tool["name"]] = tool
        self._handlers[tool["name"]] = handler

    def get_all(self) -> list[dict]:
        return list(self._tools.values())

    def execute(self, tool_name: str, tool_input: dict) -> str:
        handler = self._handlers[tool_name]  # raises KeyError if not found
        result = handler(**tool_input)
        return str(result)
