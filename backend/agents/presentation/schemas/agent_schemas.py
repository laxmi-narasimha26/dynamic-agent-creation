from pydantic import BaseModel
from typing import List, Optional


class AgentCreateRequest(BaseModel):
    name: str
    description: str
    tools: List[str] = []


class AgentResponse(BaseModel):
    id: str
    name: str
    description: str
    tools: List[str]
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class AgentListResponse(BaseModel):
    agents: List[AgentResponse]
