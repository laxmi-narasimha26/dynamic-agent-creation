from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import uuid


class ExecutionStep(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tool_name: str
    input: Dict[str, Any]
    output: Optional[Dict[str, Any]] = None
    timestamp: str
    duration: Optional[float] = None


class Execution(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str
    query: str
    steps: List[ExecutionStep] = Field(default_factory=list)
    result: Optional[str] = None
    status: str  # e.g., 'running', 'completed', 'failed'
    started_at: str
    completed_at: Optional[str] = None
