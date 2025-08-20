from typing import Optional, List
from ...core.entities.agent import Agent
from ...core.repositories.agent_repository import AgentRepository
from .agent_repository import PostgreSQLAgentRepository
from .redis_cache import RedisCache


class HybridAgentRepository(AgentRepository):
    def __init__(self, postgres_repo: PostgreSQLAgentRepository, redis_cache: RedisCache):
        self.postgres_repo = postgres_repo
        self.redis_cache = redis_cache
    
    async def create(self, entity: Agent) -> Agent:
        # PostgreSQL for durability
        db_agent = await self.postgres_repo.create(entity)
        
        # Redis for speed
        await self.redis_cache.set_agent(db_agent)
        
        return db_agent
    
    async def get_by_id(self, id: str) -> Optional[Agent]:
        # L1 Cache: Redis
        cached_agent = await self.redis_cache.get_agent(id)
        if cached_agent:
            return cached_agent
        
        # L2 Storage: PostgreSQL
        db_agent = await self.postgres_repo.get_by_id(id)
        if db_agent:
            # Update cache
            await self.redis_cache.set_agent(db_agent)
        
        return db_agent
    
    async def update(self, entity: Agent) -> Agent:
        # Update in PostgreSQL
        updated_agent = await self.postgres_repo.update(entity)
        
        # Invalidate cache
        await self.redis_cache.invalidate_agent(entity.id)
        
        return updated_agent
    
    async def delete(self, id: str) -> bool:
        # Delete from PostgreSQL
        result = await self.postgres_repo.delete(id)
        
        # Invalidate cache
        await self.redis_cache.invalidate_agent(id)
        
        return result
    
    async def list_all(self, skip: int = 0, limit: int = 100) -> List[Agent]:
        # For listing, we'll use PostgreSQL as it's not cacheable
        return await self.postgres_repo.list_all(skip, limit)
