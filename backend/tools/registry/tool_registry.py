# Tool registry with dynamic registration
from typing import Type, Dict
from src.tools.core.base_tool import BaseTool

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Type[BaseTool]] = {}

    def register(self, tool_class: Type[BaseTool]) -> None:
        key = tool_class.name.lower()
        self._tools[key] = tool_class

    def get_tool(self, name: str) -> Type[BaseTool]:
        return self._tools.get(name.lower())

    def list_tools(self):
        return list(self._tools.keys())
