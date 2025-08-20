from fastapi import APIRouter, Depends
from ...infrastructure.messaging.streaming_service import AgentStreamingService

router = APIRouter()

streaming_service = AgentStreamingService()

@router.get("/stream/{agent_id}")
async def stream_agent_response(agent_id: str, query: str):
    """Stream the agent's response to a query using Server-Sent Events."""
    return await streaming_service.stream_agent_response(query, agent_id)
