from pydantic import BaseModel


class TaskNode(BaseModel):
    id: str
    prompt: str
    depends_on: list[str] = []


class TaskDAG(BaseModel):
    nodes: list[TaskNode]

    def get_ready_tasks(self, completed: set[str]) -> list[TaskNode]:
        return [
            n for n in self.nodes
            if n.id not in completed
            and all(dep in completed for dep in n.depends_on)
        ]

    def is_complete(self, completed: set[str]) -> bool:
        return all(n.id in completed for n in self.nodes)
