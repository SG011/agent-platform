# agent-platform

Multi-agent orchestration platform — Python 3.13, Claude API, asyncio. Decomposes goals into parallel task DAGs, executes agents with tool use, shares results via Redis.

## Architecture

```
User goal → Planner (Claude API) → TaskDAG
TaskDAG → AgentExecutor (asyncio) → parallel WorkerAgents
WorkerAgents → ToolRegistry (web_search, CRM, email) → results
Results → MemoryStore (Redis) → downstream agents
```

## Quick Start

```bash
docker-compose up -d          # Kafka, Redis
export ANTHROPIC_API_KEY=...
uvicorn agent_platform.api.app:app --reload

# Run an agent workflow
curl -X POST http://localhost:8000/runs \
  -H "Content-Type: application/json" \
  -d '{"goal": "Research the top 3 Python web frameworks and summarize their trade-offs"}'
```

## Features
- Claude-powered task decomposition into dependency DAGs
- asyncio parallel execution (up to 20 concurrent agents)
- Tool use: web search, CRM read/write, email send
- Redis shared memory — agents pass results to downstream tasks
- Prompt caching for reduced latency and cost

## Tech Stack
Python 3.13 · Anthropic SDK · asyncio · Redis 7 · Apache Kafka · FastAPI · Pydantic v2
