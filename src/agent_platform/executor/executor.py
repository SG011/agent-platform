import asyncio
from agent_platform.planner.dag import TaskDAG
from agent_platform.memory.store import MemoryStore
from agent_platform.executor.worker import WorkerAgent

class AgentExecutor:
    def __init__(self, memory_store: MemoryStore, worker: WorkerAgent, max_parallel: int = 20):
        self._store = memory_store
        self._worker = worker
        self._semaphore = asyncio.Semaphore(max_parallel)

    async def execute(self, dag: TaskDAG, run_id: str) -> dict[str, str]:
        completed: set[str] = set()
        results: dict[str, str] = {}

        while not dag.is_complete(completed):
            ready = dag.get_ready_tasks(completed)
            if not ready:
                break  # deadlock or all done

            tasks = [self._run_task(node, run_id, completed, results) for node in ready]
            task_results = await asyncio.gather(*tasks)

            for node, result in zip(ready, task_results):
                results[node.id] = result
                self._store.save(run_id, node.id, result)
                completed.add(node.id)

        return results

    async def _run_task(self, node, run_id, completed, results):
        context = {dep: results[dep] for dep in node.depends_on if dep in results}
        async with self._semaphore:
            return await self._worker.run(node, context)
