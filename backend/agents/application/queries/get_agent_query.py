from pydantic import BaseModel


class GetAgentQuery(BaseModel):
    agent_id: str
