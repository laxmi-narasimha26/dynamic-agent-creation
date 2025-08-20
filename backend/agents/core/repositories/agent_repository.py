from typing import Optional
from ..entities.agent import Agent
from .base import BaseRepository


class AgentRepository(BaseRepository[Agent]):
    async def get_by_name(self, name: str) -> Optional[Agent]:
        # This would be implemented in the concrete repository
        pass
