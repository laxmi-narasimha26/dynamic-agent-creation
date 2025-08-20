from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ...core.entities.tool import Tool
from ...core.repositories.tool_repository import ToolRepository
from .models import ToolModel


class PostgreSQLToolRepository(ToolRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, entity: Tool) -> Tool:
        model = ToolModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            type=entity.type,
            config=entity.config
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._model_to_entity(model)
    
    async def get_by_id(self, id: str) -> Optional[Tool]:
        result = await self.session.execute(select(ToolModel).where(ToolModel.id == id))
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None
    
    async def get_by_name(self, name: str) -> Optional[Tool]:
        result = await self.session.execute(select(ToolModel).where(ToolModel.name == name))
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None
    
    async def get_by_type(self, tool_type: str) -> List[Tool]:
        result = await self.session.execute(select(ToolModel).where(ToolModel.type == tool_type))
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    async def update(self, entity: Tool) -> Tool:
        result = await self.session.execute(select(ToolModel).where(ToolModel.id == entity.id))
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"Tool with id {entity.id} not found")
        
        model.name = entity.name
        model.description = entity.description
        model.type = entity.type
        model.config = entity.config
        
        await self.session.commit()
        await self.session.refresh(model)
        return self._model_to_entity(model)
    
    async def delete(self, id: str) -> bool:
        result = await self.session.execute(select(ToolModel).where(ToolModel.id == id))
        model = result.scalar_one_or_none()
        if not model:
            return False
        
        await self.session.delete(model)
        await self.session.commit()
        return True
    
    async def list_all(self, skip: int = 0, limit: int = 100) -> List[Tool]:
        result = await self.session.execute(select(ToolModel).offset(skip).limit(limit))
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    def _model_to_entity(self, model: ToolModel) -> Tool:
        return Tool(
            id=model.id,
            name=model.name,
            description=model.description,
            type=model.type,
            config=model.config
        )
