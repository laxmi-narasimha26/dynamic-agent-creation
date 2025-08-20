from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import List
import json
import time
import asyncio
from pydantic import BaseModel

from models.agent import Agent
from agents.core.services.tool_registry import get_global_registry
from agents.application.orchestrator import stream_agent_events

router = APIRouter()

# In-memory storage for agents (will be replaced with a database)
agents_db: dict[str, Agent] = {}

# Tools endpoints are defined in agents.presentation.api.tool_routes

@router.post("/agents", response_model=Agent, status_code=201)
async def create_agent(agent: Agent):
    """Create a new agent."""
    if agent.id in agents_db:
        raise HTTPException(status_code=400, detail="Agent with this ID already exists")
    agents_db[agent.id] = agent
    return agent

@router.get("/agents", response_model=List[Agent])
async def list_agents():
    """List all available agents."""
    return list(agents_db.values())

@router.get("/agents/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str):
    """Retrieve a single agent by its ID."""
    agent = agents_db.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.get("/agents/{agent_id}/stream")
async def stream_agent_execution(agent_id: str, query: str):
    """Server-Sent Events streaming execution for an agent.
    Executes the agent's attached tools in sequence and streams progress + final result.
    """
    # Validate agent exists
    agent = agents_db.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    # Normalize query
    q = (query or "").strip()

    # Greeting / small-talk bypass
    greetings = {"hi", "hello", "hey", "hola", "yo", "sup", "good morning", "good afternoon", "good evening"}
    q_l = q.lower().strip()

    async def event_generator():
        try:
            # Connection ack
            yield "data: {\"type\": \"connection\", \"status\": \"connected\"}\n\n"

            # Greeting short-circuit
            if q_l in greetings or any(q_l.startswith(g + " ") for g in greetings):
                msg = "Hello! How can I help you today?"
                yield f"data: {json.dumps({'type':'message','content': msg,'timestamp': time.time()})}\n\n"
                yield f"data: {json.dumps({'type':'result','content': msg,'timestamp': time.time()})}\n\n"
                yield "data: {\"type\": \"complete\"}\n\n"
                return

            # Orchestrated execution with LangGraph
            for ev in stream_agent_events(agent, q):
                etype = ev.get('type')
                content = ev.get('content')
                if etype in {"message", "result"} and content is not None:
                    payload = {'type': etype, 'content': content, 'timestamp': time.time()}
                    yield f"data: {json.dumps(payload)}\n\n"
            # Complete
            yield "data: {\"type\": \"complete\"}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
