import asyncio
from typing import Callable, List, Awaitable
from dataclasses import dataclass
from enum import Enum


class AgentEventType(Enum):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
    EXECUTION_STARTED = "execution_started"
    EXECUTION_COMPLETED = "execution_completed"
    EXECUTION_FAILED = "execution_failed"


@dataclass
class AgentEvent:
    agent_id: str
    event_type: AgentEventType
    timestamp: float
    data: dict


class AgentEventObserver:
    def __init__(self):
        self._observers: List[Callable[[AgentEvent], Awaitable[None]]] = []
    
    def subscribe(self, callback: Callable[[AgentEvent], Awaitable[None]]):
        self._observers.append(callback)
    
    async def notify(self, event: AgentEvent):
        await asyncio.gather(*[observer(event) for observer in self._observers])
