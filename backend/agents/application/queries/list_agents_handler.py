from typing import List
from .list_agents_query import ListAgentsQuery
from ...core.entities.agent import Agent
from ...core.repositories.agent_repository import AgentRepository


class ListAgentsHandler:
    def __init__(self, agent_repository: AgentRepository):
        self.agent_repository = agent_repository
    
    async def handle(self, query: ListAgentsQuery) -> List[Agent]:
        return await self.agent_repository.list_all(query.skip, query.limit)
