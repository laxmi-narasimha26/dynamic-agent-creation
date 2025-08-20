from typing import Optional
from .get_agent_query import GetAgentQuery
from ...core.entities.agent import Agent
from ...core.repositories.agent_repository import AgentRepository


class GetAgentHandler:
    def __init__(self, agent_repository: AgentRepository):
        self.agent_repository = agent_repository
    
    async def handle(self, query: GetAgentQuery) -> Optional[Agent]:
        return await self.agent_repository.get_by_id(query.agent_id)
