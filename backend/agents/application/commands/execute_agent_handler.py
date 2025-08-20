from typing import Optional
from .execute_agent_command import ExecuteAgentCommand
from ...core.entities.agent import Agent
from ...core.entities.execution import Execution, ExecutionStep
from ...core.repositories.agent_repository import AgentRepository
from ...core.repositories.execution_repository import ExecutionRepository
from ...core.events.agent_event_observer import AgentEventObserver, AgentEvent, AgentEventType
import time


class ExecuteAgentHandler:
    def __init__(self, agent_repository: AgentRepository, execution_repository: ExecutionRepository, event_observer: AgentEventObserver):
        self.agent_repository = agent_repository
        self.execution_repository = execution_repository
        self.event_observer = event_observer
    
    async def handle(self, command: ExecuteAgentCommand) -> Execution:
        # Get the agent
        agent = await self.agent_repository.get_by_id(command.agent_id)
        if not agent:
            raise ValueError(f"Agent with id {command.agent_id} not found")
        
        # Create execution record
        execution = Execution(
            agent_id=command.agent_id,
            query=command.query,
            status="running",
            started_at=str(time.time())
        )
        
        # Save initial execution
        execution = await self.execution_repository.create(execution)
        
        # Notify observers that execution started
        event = AgentEvent(
            agent_id=command.agent_id,
            event_type=AgentEventType.EXECUTION_STARTED,
            timestamp=time.time(),
            data={"execution_id": execution.id, "query": command.query}
        )
        await self.event_observer.notify(event)
        
        # TODO: Implement actual agent execution logic with LangGraph
        # For now, we'll simulate a simple execution
        
        # Simulate tool execution
        step = ExecutionStep(
            tool_name="web_search",
            input={"query": command.query},
            output={"result": f"Search results for '{command.query}'"},
            timestamp=str(time.time()),
            duration=0.5
        )
        
        execution.steps.append(step)
        execution.result = f"Executed query: {command.query}"
        execution.status = "completed"
        execution.completed_at = str(time.time())
        
        # Update execution
        execution = await self.execution_repository.update(execution)
        
        # Notify observers that execution completed
        event = AgentEvent(
            agent_id=command.agent_id,
            event_type=AgentEventType.EXECUTION_COMPLETED,
            timestamp=time.time(),
            data={"execution_id": execution.id, "result": execution.result}
        )
        await self.event_observer.notify(event)
        
        return execution
