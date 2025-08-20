import pytest
from unittest.mock import AsyncMock, Mock
from agents.core.entities.agent import Agent
from agents.core.repositories.agent_repository import AgentRepository
from agents.infrastructure.persistence.agent_repository import PostgreSQLAgentRepository
from agents.infrastructure.persistence.hybrid_agent_repository import HybridAgentRepository
from agents.infrastructure.persistence.redis_cache import RedisCache


class TestPostgreSQLAgentRepository:
    @pytest.fixture
    def mock_db_session(self):
        return AsyncMock()
    
    @pytest.fixture
    def repo(self, mock_db_session):
        return PostgreSQLAgentRepository(mock_db_session)
    
    def test_create_agent(self, repo, mock_db_session):
        """Test that an agent can be created."""
        agent = Agent(name="Test Agent", description="A test agent")
        
        # Mock the database operations
        mock_db_session.add = Mock()
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock()
        
        # Call the method
        result = repo.create(agent)
        
        # Verify the calls
        mock_db_session.add.assert_called_once_with(agent)
        mock_db_session.commit.assert_awaited_once()
        mock_db_session.refresh.assert_awaited_once_with(agent)
        
        # Verify the result
        assert result is agent
    
    def test_get_by_id(self, repo, mock_db_session):
        """Test that an agent can be retrieved by ID."""
        agent_id = "test-id"
        expected_agent = Agent(name="Test Agent", description="A test agent")
        
        # Mock the database operations
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none = Mock(return_value=expected_agent)
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        
        # Call the method
        result = repo.get_by_id(agent_id)
        
        # Verify the calls
        mock_db_session.execute.assert_awaited_once()
        mock_result.scalar_one_or_none.assert_called_once()
        
        # Verify the result
        assert result is expected_agent
    
    def test_get_by_name(self, repo, mock_db_session):
        """Test that an agent can be retrieved by name."""
        agent_name = "Test Agent"
        expected_agent = Agent(name=agent_name, description="A test agent")
        
        # Mock the database operations
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none = Mock(return_value=expected_agent)
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        
        # Call the method
        result = repo.get_by_name(agent_name)
        
        # Verify the calls
        mock_db_session.execute.assert_awaited_once()
        mock_result.scalar_one_or_none.assert_called_once()
        
        # Verify the result
        assert result is expected_agent

class TestHybridAgentRepository:
    @pytest.fixture
    def mock_postgres_repo(self):
        return Mock()
    
    @pytest.fixture
    def mock_redis_cache(self):
        return Mock()
    
    @pytest.fixture
    def repo(self, mock_postgres_repo, mock_redis_cache):
        return HybridAgentRepository(mock_postgres_repo, mock_redis_cache)
    
    def test_get_by_id_from_cache(self, repo, mock_postgres_repo, mock_redis_cache):
        """Test that an agent is retrieved from cache when available."""
        agent_id = "test-id"
        expected_agent = Agent(name="Test Agent", description="A test agent")
        
        # Mock the cache to return an agent
        mock_redis_cache.get_agent = Mock(return_value=expected_agent)
        
        # Call the method
        result = repo.get_by_id(agent_id)
        
        # Verify the calls
        mock_redis_cache.get_agent.assert_called_once_with(agent_id)
        mock_postgres_repo.get_by_id.assert_not_called()
        
        # Verify the result
        assert result is expected_agent
    
    def test_get_by_id_from_database(self, repo, mock_postgres_repo, mock_redis_cache):
        """Test that an agent is retrieved from database when not in cache."""
        agent_id = "test-id"
        expected_agent = Agent(name="Test Agent", description="A test agent")
        
        # Mock the cache to return None and the database to return an agent
        mock_redis_cache.get_agent = Mock(return_value=None)
        mock_postgres_repo.get_by_id = Mock(return_value=expected_agent)
        mock_redis_cache.set_agent = Mock()
        
        # Call the method
        result = repo.get_by_id(agent_id)
        
        # Verify the calls
        mock_redis_cache.get_agent.assert_called_once_with(agent_id)
        mock_postgres_repo.get_by_id.assert_called_once_with(agent_id)
        mock_redis_cache.set_agent.assert_called_once_with(agent_id, expected_agent)
        
        # Verify the result
        assert result is expected_agent
