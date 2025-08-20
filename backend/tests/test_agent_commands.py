import pytest
from unittest.mock import Mock, AsyncMock
from agents.core.entities.agent import Agent
from agents.application.commands.create_agent_command import CreateAgentCommand
from agents.application.commands.create_agent_handler import CreateAgentHandler
from agents.application.commands.execute_agent_command import ExecuteAgentCommand
from agents.application.commands.execute_agent_handler import ExecuteAgentHandler
from agents.application.queries.get_agent_query import GetAgentQuery
from agents.application.queries.get_agent_handler import GetAgentHandler


class TestCreateAgentHandler:
    @pytest.fixture
    def mock_agent_repo(self):
        return AsyncMock()
    
    @pytest.fixture
    def mock_event_observer(self):
        return Mock()
    
    @pytest.fixture
    def handler(self, mock_agent_repo, mock_event_observer):
        return CreateAgentHandler(mock_agent_repo, mock_event_observer)
    
    @pytest.mark.asyncio
    async def test_handle_create_agent(self, handler, mock_agent_repo, mock_event_observer):
        """Test that an agent can be created through the handler."""
        command = CreateAgentCommand(
            name="Test Agent",
            description="A test agent",
            tools=["web_search"]
        )
        
        # Mock the repository to return a created agent
        created_agent = Agent(
            name=command.name,
            description=command.description,
            tools=command.tools
        )
        mock_agent_repo.create = AsyncMock(return_value=created_agent)
        mock_event_observer.notify = AsyncMock()
        
        # Call the handler
        result = await handler.handle(command)
        
        # Verify the calls
        mock_agent_repo.create.assert_awaited_once()
        mock_event_observer.notify.assert_awaited_once()
        
        # Verify the result
        assert isinstance(result, Agent)
        assert result.name == command.name
        assert result.description == command.description
        assert result.tools == command.tools

class TestGetAgentHandler:
    @pytest.fixture
    def mock_agent_repo(self):
        return AsyncMock()
    
    @pytest.fixture
    def handler(self, mock_agent_repo):
        return GetAgentHandler(mock_agent_repo)
    
    @pytest.mark.asyncio
    async def test_handle_get_agent(self, handler, mock_agent_repo):
        """Test that an agent can be retrieved through the handler."""
        query = GetAgentQuery(agent_id="test-id")
        
        # Mock the repository to return an agent
        expected_agent = Agent(name="Test Agent", description="A test agent")
        mock_agent_repo.get_by_id = AsyncMock(return_value=expected_agent)
        
        # Call the handler
        result = await handler.handle(query)
        
        # Verify the calls
        mock_agent_repo.get_by_id.assert_awaited_once_with(query.agent_id)
        
        # Verify the result
        assert result is expected_agent
    
    @pytest.mark.asyncio
    async def test_handle_get_agent_not_found(self, handler, mock_agent_repo):
        """Test that None is returned when agent is not found."""
        query = GetAgentQuery(agent_id="non-existent-id")
        
        # Mock the repository to return None
        mock_agent_repo.get_by_id = AsyncMock(return_value=None)
        
        # Call the handler
        result = await handler.handle(query)
        
        # Verify the calls
        mock_agent_repo.get_by_id.assert_awaited_once_with(query.agent_id)
        
        # Verify the result
        assert result is None

class TestExecuteAgentHandler:
    @pytest.fixture
    def mock_agent_repo(self):
        return AsyncMock()
    
    @pytest.fixture
    def mock_execution_repo(self):
        return AsyncMock()
    
    @pytest.fixture
    def mock_event_observer(self):
        return Mock()
    
    @pytest.fixture
    def handler(self, mock_agent_repo, mock_execution_repo, mock_event_observer):
        return ExecuteAgentHandler(mock_agent_repo, mock_execution_repo, mock_event_observer)
    
    @pytest.mark.asyncio
    async def test_handle_execute_agent(self, handler, mock_agent_repo, mock_execution_repo, mock_event_observer):
        """Test that an agent can be executed through the handler."""
        command = ExecuteAgentCommand(
            agent_id="test-id",
            query="What is the weather today?"
        )
        
        # Mock the repositories
        agent = Agent(name="Test Agent", description="A test agent", tools=["web_search"])
        mock_agent_repo.get_by_id = AsyncMock(return_value=agent)
        
        # Mock the execution repository
        mock_execution_repo.create = AsyncMock()
        mock_execution_repo.update = AsyncMock()
        
        # Mock the event observer
        mock_event_observer.notify = AsyncMock()
        
        # Call the handler
        result = await handler.handle(command)
        
        # Verify the calls
        mock_agent_repo.get_by_id.assert_awaited_once_with(command.agent_id)
        mock_execution_repo.create.assert_awaited_once()
        mock_execution_repo.update.assert_awaited()
        mock_event_observer.notify.assert_awaited()
        
        # Verify the result is an Execution instance
        assert result.agent_id == command.agent_id
        assert result.query == command.query
        assert result.status in ["completed", "failed"]
