import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from agent_platform.planner.planner import Planner
from agent_platform.executor.executor import AgentExecutor
from agent_platform.executor.worker import WorkerAgent
from agent_platform.memory.store import MemoryStore
from agent_platform.tools.registry import ToolRegistry
from agent_platform.tools.web_search import WEB_SEARCH_TOOL, web_search_handler
from agent_platform.tools.crm_tool import CRM_READ_TOOL, crm_get_contact_handler
from agent_platform.tools.email_tool import EMAIL_TOOL, send_email_handler

app = FastAPI(title="Agent Platform", version="1.0.0")

_registry = ToolRegistry()
_registry.register(WEB_SEARCH_TOOL, web_search_handler)
_registry.register(CRM_READ_TOOL, crm_get_contact_handler)
_registry.register(EMAIL_TOOL, send_email_handler)

_planner = Planner()
_store = MemoryStore()
_worker = WorkerAgent(registry=_registry)
_executor = AgentExecutor(memory_store=_store, worker=_worker)

class RunRequest(BaseModel):
    goal: str

class RunResponse(BaseModel):
    run_id: str
    results: dict[str, str]

@app.post("/runs", response_model=RunResponse)
async def create_run(request: RunRequest):
    run_id = str(uuid.uuid4())
    dag = _planner.plan(request.goal)
    results = await _executor.execute(dag, run_id=run_id)
    return RunResponse(run_id=run_id, results=results)

@app.get("/health")
def health():
    return {"status": "ok"}
