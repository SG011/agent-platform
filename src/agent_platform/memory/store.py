import redis

class MemoryStore:
    def __init__(self, client: redis.Redis | None = None):
        self._client = client or redis.Redis(
            host="localhost", port=6379, decode_responses=True
        )

    def save(self, run_id: str, task_id: str, result: str) -> None:
        key = f"agent:{run_id}:{task_id}:result"
        self._client.set(key, result, ex=86400)  # 24h TTL

    def get(self, run_id: str, task_id: str) -> str | None:
        key = f"agent:{run_id}:{task_id}:result"
        return self._client.get(key)

    def get_all_results(self, run_id: str) -> dict[str, str]:
        pattern = f"agent:{run_id}:*:result"
        keys = self._client.keys(pattern)
        results = {}
        for key in keys:
            task_id = key.split(":")[2]
            results[task_id] = self._client.get(key)
        return results
