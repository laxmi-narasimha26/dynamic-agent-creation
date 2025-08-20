import pytest
from agents.core.services.tool_registry import ToolRegistry
from agents.infrastructure.external.web_search_tool import WebSearchTool
from agents.infrastructure.external.calculator_tool import CalculatorTool


class TestToolRegistry:
    @pytest.fixture
    def registry(self):
        return ToolRegistry()
    
    def test_register_and_get_tool(self, registry):
        """Test that a tool can be registered and retrieved."""
        tool = WebSearchTool()
        registry.register_tool("web_search", tool)
        
        retrieved_tool = registry.get_tool("web_search")
        
        assert retrieved_tool is tool
    
    def test_get_all_tools(self, registry):
        """Test that all registered tools can be retrieved."""
        web_search_tool = WebSearchTool()
        calculator_tool = CalculatorTool()
        
        registry.register_tool("web_search", web_search_tool)
        registry.register_tool("calculator", calculator_tool)
        
        all_tools = registry.get_all_tools()
        
        assert len(all_tools) == 2
        assert "web_search" in all_tools
        assert "calculator" in all_tools
        assert all_tools["web_search"] is web_search_tool
        assert all_tools["calculator"] is calculator_tool
    
    def test_is_tool_registered(self, registry):
        """Test that we can check if a tool is registered."""
        tool = WebSearchTool()
        registry.register_tool("web_search", tool)
        
        assert registry.is_tool_registered("web_search") is True
        assert registry.is_tool_registered("calculator") is False
    
    def test_register_tool_from_code(self, registry):
        """Test that a tool can be registered from code."""
        code = '''
class CustomTool(WebSearchTool):
    name = "custom_tool"
    description = "A custom tool"
'''
        
        registry.register_tool_from_code("custom_tool", code)
        
        assert registry.is_tool_registered("custom_tool") is True
        
        tool = registry.get_tool("custom_tool")
        assert tool.name == "custom_tool"
        assert tool.description == "A custom tool"
    
    def test_execute_tool(self, registry):
        """Test that a tool can be executed."""
        tool = WebSearchTool()
        registry.register_tool("web_search", tool)
        
        result = registry.execute_tool("web_search", {"query": "test query"})
        
        assert result is not None
        assert "content" in result
        assert isinstance(result["content"], str)
