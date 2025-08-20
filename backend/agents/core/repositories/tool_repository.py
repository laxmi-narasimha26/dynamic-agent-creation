from typing import List, Optional
from ..entities.tool import Tool
from .base import BaseRepository


class ToolRepository(BaseRepository[Tool]):
    async def get_by_name(self, name: str) -> Optional[Tool]:
        # This would be implemented in the concrete repository
        pass
    
    async def get_by_type(self, tool_type: str) -> List[Tool]:
        # This would be implemented in the concrete repository
        pass
