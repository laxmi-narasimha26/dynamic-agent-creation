from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..schemas.agent_schemas import AgentCreateRequest, AgentResponse, AgentListResponse
from ...application.commands.create_agent_command import CreateAgentCommand
from ...application.commands.create_agent_handler import CreateAgentHandler
from ...application.queries.get_agent_query import GetAgentQuery
from ...application.queries.get_agent_handler import GetAgentHandler
from ...application.queries.list_agents_query import ListAgentsQuery
from ...application.queries.list_agents_handler import ListAgentsHandler
from ...infrastructure.persistence.hybrid_agent_repository import HybridAgentRepository
from ...infrastructure.persistence.agent_repository import PostgreSQLAgentRepository
from ...infrastructure.persistence.redis_cache import RedisCache
from ...infrastructure.persistence.database import get_db
from ...infrastructure.persistence.redis_client import redis_client
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

async def get_agent_handlers(db: AsyncSession = Depends(get_db)):
    # Initialize repositories
    postgres_repo = PostgreSQLAgentRepository(db)
    redis_cache = RedisCache(redis_client)
    hybrid_repo = HybridAgentRepository(postgres_repo, redis_cache)
    
    # Initialize handlers
    create_handler = CreateAgentHandler(hybrid_repo, None)  # TODO: Add event observer
    get_handler = GetAgentHandler(hybrid_repo)
    list_handler = ListAgentsHandler(hybrid_repo)
    
    return create_handler, get_handler, list_handler

@router.post("/agents", response_model=AgentResponse, status_code=201)
async def create_agent(
    request: AgentCreateRequest,
    handlers: tuple = Depends(get_agent_handlers)
):
    create_handler, _, _ = handlers
    command = CreateAgentCommand(
        name=request.name,
        description=request.description,
        tools=request.tools
    )
    agent = await create_handler.handle(command)
    return agent

@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    handlers: tuple = Depends(get_agent_handlers)
):
    _, get_handler, _ = handlers
    query = GetAgentQuery(agent_id=agent_id)
    agent = await get_handler.handle(query)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.get("/agents", response_model=AgentListResponse)
async def list_agents(
    skip: int = 0,
    limit: int = 100,
    handlers: tuple = Depends(get_agent_handlers)
):
    _, _, list_handler = handlers
    query = ListAgentsQuery(skip=skip, limit=limit)
    agents = await list_handler.handle(query)
    return AgentListResponse(agents=agents)
