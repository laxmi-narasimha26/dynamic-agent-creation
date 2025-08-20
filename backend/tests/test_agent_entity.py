import pytest
from datetime import datetime
from agents.core.entities.agent import Agent


class TestAgentEntity:
    def test_agent_creation(self):
        """Test that an agent can be created with valid parameters."""
        agent = Agent(
            name="Test Agent",
            description="A test agent",
            tools=["web_search", "calculator"]
        )
        
        assert agent.name == "Test Agent"
        assert agent.description == "A test agent"
        assert agent.tools == ["web_search", "calculator"]
        assert isinstance(agent.id, str)
        assert isinstance(agent.created_at, datetime)
        assert isinstance(agent.updated_at, datetime)
    
    def test_agent_id_is_unique(self):
        """Test that each agent gets a unique ID."""
        agent1 = Agent(name="Agent 1", description="First agent")
        agent2 = Agent(name="Agent 2", description="Second agent")
        
        assert agent1.id != agent2.id
    
    def test_agent_timestamps(self):
        """Test that created_at and updated_at are set correctly."""
        agent = Agent(name="Test Agent", description="A test agent")
        
        assert agent.created_at is not None
        assert agent.updated_at is not None
        assert agent.created_at == agent.updated_at
        
        # Store the original timestamps
        original_created = agent.created_at
        original_updated = agent.updated_at
        
        # Update the agent (this would normally happen through a method)
        agent.name = "Updated Agent"
        
        # In a real implementation, updated_at would be updated here
        # For now, we're just testing that the fields exist
        assert agent.created_at == original_created
