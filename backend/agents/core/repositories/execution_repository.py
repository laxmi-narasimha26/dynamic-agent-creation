from typing import List
from ..entities.execution import Execution
from .base import BaseRepository


class ExecutionRepository(BaseRepository[Execution]):
    async def get_by_agent_id(self, agent_id: str) -> List[Execution]:
        # This would be implemented in the concrete repository
        pass
    
    async def get_recent_executions(self, limit: int = 10) -> List[Execution]:
        # This would be implemented in the concrete repository
        pass
