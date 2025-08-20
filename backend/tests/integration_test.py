import pytest
import os
import sys
import uuid

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import core entities and services
from agents.core.entities.agent import Agent
from agents.core.services.tool_registry import ToolRegistry

# Import tool-related classes
from agents.infrastructure.external.base_tool import BaseTool, ToolInput, ToolOutput
from agents.infrastructure.external.web_search_tool import WebSearchTool
from agents.infrastructure.external.calculator_tool import CalculatorTool
from agents.infrastructure.external.summarizer_tool import SummarizerTool

class TestDynamicAgentSystem:
    """Integration tests for the Dynamic Agent Creation System."""
    
    def test_agent_entity(self):
        """Test the Agent entity creation and properties."""
        # Create an agent
        agent = Agent(
            name="Test Agent",
            description="A test agent for integration testing",
            tools=["web_search", "calculator"]
        )
        
        # Verify agent properties
        assert agent.id is not None
        assert agent.name == "Test Agent"
        assert agent.description == "A test agent for integration testing"
        assert "web_search" in agent.tools
        assert "calculator" in agent.tools
        
        # Create another agent to verify unique IDs
        another_agent = Agent(
            name="Another Test Agent",
            description="Another test agent",
            tools=["summarizer"]
        )
        
        assert agent.id != another_agent.id
        registry = ToolRegistry()
        
        # Check prebuilt tools are already registered
        tools = registry.list_tools()
        assert "web_search" in tools
        assert "calculator" in tools
        assert "summarizer" in tools
        
        # Check tool creation
        calculator = registry.create_tool("calculator")
        assert calculator.name == "calculator"
        
        # Register a tool from code
        code = """
from agents.infrastructure.external.base_tool import BaseTool, ToolInput, ToolOutput
from pydantic import Field

class CustomToolInput(ToolInput):
    text: str = Field(..., description="Text to process")

class CustomTool(BaseTool):
    name = "custom_tool"
    description = "A custom tool for testing"
    args_schema = CustomToolInput
    
    def _run(self, text: str) -> ToolOutput:
        return ToolOutput(content=f"Processed: {text}")
"""
        
        registry.register_from_code(code, "custom_tool")
        tools = registry.list_tools()
        assert "custom_tool" in tools
    
    def test_agent_entity(self):
        """Test the agent entity functionality."""
        # Create an agent
        agent = Agent(
            name="Test Agent",
            description="A test agent",
            tools=["web_search", "calculator"]
        )
        
        # Check agent properties
        assert agent.name == "Test Agent"
        assert agent.description == "A test agent"
        assert agent.tools == ["web_search", "calculator"]
        assert agent.id is not None
        
        # Create another agent to check unique IDs
        another_agent = Agent(
            name="Another Test Agent",
            description="Another test agent",
            tools=["summarizer"]
        )
        
        assert agent.id != another_agent.id
    
    def test_calculator_tool(self):
        """Test the calculator tool functionality."""
        calculator = CalculatorTool()
        
        # Test simple addition
        result = calculator.run(expression="2+2")
        assert "4" in result.content
        
        # Test more complex expression
        result = calculator.run(expression="(10 * 5) / 2")
        assert "25.0" in result.content
        
        # Test error handling
        result = calculator.run(expression="invalid")
        assert "Error" in result.content
    
    def test_web_search_tool(self):
        """Test the web search tool functionality."""
        web_search = WebSearchTool()
        
        # Test search
        result = web_search.run(query="test query")
        assert result.content is not None
        assert len(result.content) > 0
    
    def test_summarizer_tool(self):
        """Test the summarizer tool functionality."""
        summarizer = SummarizerTool()
        
        # Test summarization
        text = "This is a long text that needs to be summarized. " * 10
        result = summarizer.run(text=text)
        assert result.content is not None
        assert len(result.content) < len(text)
    
    def test_base_tool_interface(self):
        """Test that all tools implement the base tool interface correctly."""
        tools = [WebSearchTool(), CalculatorTool(), SummarizerTool()]
        
        for tool in tools:
            # Check tool properties
            assert tool.name is not None
            assert tool.description is not None
            assert tool.args_schema is not None
            
            # Check tool methods
            assert hasattr(tool, "run")
            assert hasattr(tool, "_run")
            
            # Check that the tool can be serialized
            tool_dict = tool.model_dump()
            assert "name" in tool_dict
            assert "description" in tool_dict
