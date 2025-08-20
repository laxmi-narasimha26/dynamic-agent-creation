# Repository interfaces
from abc import ABC, abstractmethod
from typing import Optional
from .entities import Agent

class AgentRepository(ABC):
    @abstractmethod
    async def create_agent(self, agent: Agent) -> Agent:
        pass

    @abstractmethod
    async def get_agent(self, agent_id: str) -> Optional[Agent]:
        pass

    @abstractmethod
    async def update_agent(self, agent: Agent) -> Agent:
        pass

    @abstractmethod
    async def delete_agent(self, agent_id: str) -> bool:
        pass
