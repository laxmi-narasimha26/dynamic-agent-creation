from typing import Optional
from .create_agent_command import CreateAgentCommand
from ...core.entities.agent import Agent
from ...core.repositories.agent_repository import AgentRepository
from ...core.events.agent_event_observer import AgentEventObserver, AgentEvent, AgentEventType
import time


class CreateAgentHandler:
    def __init__(self, agent_repository: AgentRepository, event_observer: AgentEventObserver):
        self.agent_repository = agent_repository
        self.event_observer = event_observer
    
    async def handle(self, command: CreateAgentCommand) -> Agent:
        # Create the agent entity
        agent = Agent(
            name=command.name,
            description=command.description,
            tools=command.tools,
            created_at=str(time.time()),
            updated_at=str(time.time())
        )
        
        # Save to repository
        created_agent = await self.agent_repository.create(agent)
        
        # Notify observers
        event = AgentEvent(
            agent_id=created_agent.id,
            event_type=AgentEventType.CREATED,
            timestamp=time.time(),
            data={"name": created_agent.name}
        )
        await self.event_observer.notify(event)
        
        return created_agent
