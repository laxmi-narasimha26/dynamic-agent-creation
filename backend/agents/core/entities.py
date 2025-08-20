# Domain entities for agents
from pydantic import BaseModel, Field
from typing import List

class Agent(BaseModel):
    id: str
    name: str
    description: str
    tools: List[str] = Field(default_factory=list)
