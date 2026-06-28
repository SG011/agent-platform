import anthropic
from agent_platform.planner.dag import TaskNode
from agent_platform.tools.registry import ToolRegistry

WORKER_SYSTEM = """You are an expert agent. Complete the given task using available tools.
Return a concise, factual result that can be used by downstream tasks."""

class WorkerAgent:
    def __init__(self, registry: ToolRegistry, client: anthropic.Anthropic | None = None):
        self._registry = registry
        self._client = client or anthropic.Anthropic()

    async def run(self, task: TaskNode, context: dict[str, str]) -> str:
        context_str = "\n".join(f"- {k}: {v}" for k, v in context.items())
        user_message = f"Task: {task.prompt}"
        if context_str:
            user_message += f"\n\nContext from previous tasks:\n{context_str}"

        messages = [{"role": "user", "content": user_message}]
        tools = self._registry.get_all()

        for _ in range(5):  # max 5 tool-use rounds
            response = self._client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=4096,
                system=[{
                    "type": "text",
                    "text": WORKER_SYSTEM,
                    "cache_control": {"type": "ephemeral"}
                }],
                tools=tools,
                messages=messages
            )
            if response.stop_reason == "end_turn":
                for block in response.content:
                    if hasattr(block, "text"):
                        return block.text
                return "Task completed."

            if response.stop_reason == "tool_use":
                messages.append({"role": "assistant", "content": response.content})
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        result = self._registry.execute(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result
                        })
                messages.append({"role": "user", "content": tool_results})

        return "Max tool-use rounds reached."
