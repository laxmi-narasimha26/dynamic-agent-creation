from typing import Dict, Type, Any, Optional
from abc import ABC, abstractmethod
from ..entities.tool import Tool
from ...infrastructure.external.web_search_tool import WebSearchTool
from ...infrastructure.external.calculator_tool import CalculatorTool
from ...infrastructure.external.summarizer_tool import SummarizerTool


class ToolFactory(ABC):
    @abstractmethod
    def create_tool(self, tool_type: str, config: dict) -> Tool: ...


class ConcreteToolFactory(ToolFactory):
    def __init__(self):
        self._registry: Dict[str, Type[Tool]] = {
            'web_search': WebSearchTool,
            'calculator': CalculatorTool,
            'summarizer': SummarizerTool
        }
    
    def create_tool(self, tool_type: str, config: dict) -> Tool:
        tool_class = self._registry.get(tool_type)
        if not tool_class:
            raise ValueError(f"Tool type '{tool_type}' not registered")
        return tool_class(**config)
    
    def register_tool(self, tool_type: str, tool_class: Type[Tool]):
        self._registry[tool_type] = tool_class
