import json
import anthropic
from .dag import TaskDAG

SYSTEM_PROMPT = """You are a task planner. Given a goal, decompose it into a list of tasks as a JSON object.
Return ONLY valid JSON in this exact format:
{
  "nodes": [
    {"id": "t1", "prompt": "Task description", "depends_on": []},
    {"id": "t2", "prompt": "Another task that depends on t1", "depends_on": ["t1"]}
  ]
}
Rules:
- Each task must have a unique id (t1, t2, t3, ...)
- depends_on lists the ids of tasks that must complete before this one starts
- Tasks with no dependencies can run in parallel
- Keep tasks focused and atomic (one clear action each)"""


class Planner:
    def __init__(self, client: anthropic.Anthropic | None = None):
        self._client = client or anthropic.Anthropic()

    def plan(self, goal: str) -> TaskDAG:
        response = self._client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=[{
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"}
            }],
            messages=[{"role": "user", "content": goal}]
        )
        raw = response.content[0].text
        # Strip markdown code fences if present
        if raw.strip().startswith("```"):
            raw = "\n".join(raw.strip().split("\n")[1:-1])
        data = json.loads(raw)
        return TaskDAG(**data)
