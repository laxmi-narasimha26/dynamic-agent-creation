from pydantic import BaseModel
from typing import List


class CreateAgentCommand(BaseModel):
    name: str
    description: str
    tools: List[str] = []
