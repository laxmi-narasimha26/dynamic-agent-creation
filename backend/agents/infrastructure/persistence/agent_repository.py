from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ...core.entities.agent import Agent
from ...core.repositories.agent_repository import AgentRepository
from .models import AgentModel


class PostgreSQLAgentRepository(AgentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, entity: Agent) -> Agent:
        model = AgentModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            tools=entity.tools
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._model_to_entity(model)
    
    async def get_by_id(self, id: str) -> Optional[Agent]:
        result = await self.session.execute(select(AgentModel).where(AgentModel.id == id))
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None
    
    async def get_by_name(self, name: str) -> Optional[Agent]:
        result = await self.session.execute(select(AgentModel).where(AgentModel.name == name))
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None
    
    async def update(self, entity: Agent) -> Agent:
        result = await self.session.execute(select(AgentModel).where(AgentModel.id == entity.id))
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"Agent with id {entity.id} not found")
        
        model.name = entity.name
        model.description = entity.description
        model.tools = entity.tools
        
        await self.session.commit()
        await self.session.refresh(model)
        return self._model_to_entity(model)
    
    async def delete(self, id: str) -> bool:
        result = await self.session.execute(select(AgentModel).where(AgentModel.id == id))
        model = result.scalar_one_or_none()
        if not model:
            return False
        
        await self.session.delete(model)
        await self.session.commit()
        return True
    
    async def list_all(self, skip: int = 0, limit: int = 100) -> List[Agent]:
        result = await self.session.execute(select(AgentModel).offset(skip).limit(limit))
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]
    
    def _model_to_entity(self, model: AgentModel) -> Agent:
        return Agent(
            id=model.id,
            name=model.name,
            description=model.description,
            tools=model.tools or []
        )
