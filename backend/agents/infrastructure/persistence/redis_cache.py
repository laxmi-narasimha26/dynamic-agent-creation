import json
import redis.asyncio as redis
from typing import Optional, Any
from ...core.entities.agent import Agent


class RedisCache:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.cache_ttl = 3600  # 1 hour default TTL
    
    async def get_agent(self, agent_id: str) -> Optional[Agent]:
        cached = await self.redis.get(f"agent:{agent_id}")
        if cached:
            return Agent(**json.loads(cached))
        return None
    
    async def set_agent(self, agent: Agent) -> None:
        await self.redis.setex(
            f"agent:{agent.id}",
            self.cache_ttl,
            agent.model_dump_json()
        )
    
    async def invalidate_agent(self, agent_id: str) -> None:
        await self.redis.delete(f"agent:{agent_id}")
