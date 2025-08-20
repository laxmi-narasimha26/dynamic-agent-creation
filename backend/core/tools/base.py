from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
from typing import Any, Type

class ToolInput(BaseModel):
    """Base model for tool inputs."""
    pass

class ToolOutput(BaseModel):
    """Base model for tool outputs."""
    content: Any

class BaseTool(ABC):
    """Abstract base class for all tools."""
    name: str
    description: str
    args_schema: Type[BaseModel] = ToolInput

    @abstractmethod
    def _run(self, *args: Any, **kwargs: Any) -> ToolOutput:
        """Run the tool."""
        pass

    def run(self, *args: Any, **kwargs: Any) -> ToolOutput:
        """Public method to run the tool with validation."""
        # In a real system, you'd add validation, logging, etc. here
        return self._run(*args, **kwargs)
