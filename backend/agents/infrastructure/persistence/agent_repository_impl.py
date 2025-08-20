# PostgreSQL + Redis Hybrid Persistence Implementation
from typing import Optional
import json
from src.agents.core.entities import Agent
from src.agents.core.repositories import AgentRepository
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

class HybridAgentRepository(AgentRepository):
    def __init__(self, pg_session: AsyncSession, redis_client: Redis):
        self.pg = pg_session
        self.redis = redis_client
        self.cache_ttl = 3600  # 1 hour

    async def create_agent(self, agent: Agent) -> Agent:
        # Save to postgres and cache
        # ... implementation omitted for brevity
        return agent

    async def get_agent(self, agent_id: str) -> Optional[Agent]:
        cached = await self.redis.get(f"agent:{agent_id}")
        if cached:
            return Agent.parse_raw(cached)
        # Fallback to postgres
        # ... implementation omitted
        return None

    async def update_agent(self, agent: Agent) -> Agent:
        # ... implementation omitted
        return agent

    async def delete_agent(self, agent_id: str) -> bool:
        # ... implementation omitted
        return True
