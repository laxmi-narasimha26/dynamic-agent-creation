from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

class Agent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    tools: List[str] = Field(default_factory=list)
