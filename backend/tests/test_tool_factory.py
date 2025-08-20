import pytest
from agents.core.services.tool_factory import ToolFactory, ConcreteToolFactory
from agents.infrastructure.external.web_search_tool import WebSearchTool
from agents.infrastructure.external.calculator_tool import CalculatorTool
from agents.infrastructure.external.summarizer_tool import SummarizerTool


class TestToolFactory:
    def test_tool_factory_is_singleton(self):
        """Test that ToolFactory returns the same instance."""
        factory1 = ToolFactory()
        factory2 = ToolFactory()
        
        assert factory1 is factory2
    
    def test_create_prebuilt_tools(self):
        """Test that prebuilt tools can be created."""
        factory = ConcreteToolFactory()
        
        web_search_tool = factory.create_tool("web_search")
        calculator_tool = factory.create_tool("calculator")
        summarizer_tool = factory.create_tool("summarizer")
        
        assert isinstance(web_search_tool, WebSearchTool)
        assert isinstance(calculator_tool, CalculatorTool)
        assert isinstance(summarizer_tool, SummarizerTool)
    
    def test_create_unknown_tool_raises_error(self):
        """Test that creating an unknown tool raises a ValueError."""
        factory = ConcreteToolFactory()
        
        with pytest.raises(ValueError, match="Unknown tool type: unknown_tool"):
            factory.create_tool("unknown_tool")
    
    def test_register_custom_tool(self):
        """Test that custom tools can be registered."""
        factory = ConcreteToolFactory()
        
        # Create a simple custom tool class
        class CustomTool(WebSearchTool):
            pass
        
        factory.register_tool("custom_tool", CustomTool)
        custom_tool = factory.create_tool("custom_tool")
        
        assert isinstance(custom_tool, CustomTool)
