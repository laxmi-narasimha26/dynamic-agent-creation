from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class ExecutionStepResponse(BaseModel):
    id: str
    tool_name: str
    input: Dict[str, Any]
    output: Optional[Dict[str, Any]] = None
    timestamp: str
    duration: Optional[float] = None


class ExecutionCreateRequest(BaseModel):
    agent_id: str
    query: str


class ExecutionResponse(BaseModel):
    id: str
    agent_id: str
    query: str
    steps: List[ExecutionStepResponse]
    result: Optional[str] = None
    status: str
    started_at: str
    completed_at: Optional[str] = None
