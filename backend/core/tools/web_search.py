from .base import BaseTool, ToolInput, ToolOutput
from pydantic import Field

class WebSearchInput(ToolInput):
    query: str = Field(..., description="The search query to execute.")

class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Searches the web for the given query."
    args_schema = WebSearchInput

    def _run(self, query: str) -> ToolOutput:
        # Mock implementation
        return ToolOutput(content=f"Search results for '{query}': LangGraph is a library for building stateful, multi-actor applications with LLMs.")
