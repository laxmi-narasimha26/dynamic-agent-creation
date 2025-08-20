from pydantic import BaseModel


class ExecuteAgentCommand(BaseModel):
    agent_id: str
    query: str
