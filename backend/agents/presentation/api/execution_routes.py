from fastapi import APIRouter, Depends, HTTPException
from ..schemas.execution_schemas import ExecutionCreateRequest, ExecutionResponse
from ...application.commands.execute_agent_command import ExecuteAgentCommand
from ...application.commands.execute_agent_handler import ExecuteAgentHandler
from ...infrastructure.persistence.hybrid_agent_repository import HybridAgentRepository
from ...infrastructure.persistence.agent_repository import PostgreSQLAgentRepository
from ...infrastructure.persistence.redis_cache import RedisCache
from ...infrastructure.persistence.database import get_db
from ...infrastructure.persistence.redis_client import redis_client
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

async def get_execution_handlers(db: AsyncSession = Depends(get_db)):
    # Initialize repositories
    postgres_repo = PostgreSQLAgentRepository(db)
    redis_cache = RedisCache(redis_client)
    hybrid_repo = HybridAgentRepository(postgres_repo, redis_cache)
    
    # TODO: Initialize execution repository when it's available
    
    # Initialize handlers
    execute_handler = ExecuteAgentHandler(hybrid_repo, None, None)  # TODO: Add execution repo and event observer
    
    return execute_handler

@router.post("/executions", response_model=ExecutionResponse, status_code=201)
async def execute_agent(
    request: ExecutionCreateRequest,
    handler: ExecuteAgentHandler = Depends(get_execution_handlers)
):
    command = ExecuteAgentCommand(
        agent_id=request.agent_id,
        query=request.query
    )
    execution = await handler.handle(command)
    return execution
