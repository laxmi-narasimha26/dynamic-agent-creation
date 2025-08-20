import pytest
from unittest.mock import AsyncMock, Mock
from agents.infrastructure.messaging.streaming_service import AgentStreamingService


class TestAgentStreamingService:
    @pytest.fixture
    def mock_execution_repo(self):
        return AsyncMock()
    
    @pytest.fixture
    def service(self, mock_execution_repo):
        return AgentStreamingService(mock_execution_repo)
    
    def test_generate_streaming_response(self, service):
        """Test that streaming response is generated correctly."""
        agent_id = "test-agent-id"
        query = "What is the weather today?"
        
        # Mock the streaming generator
        mock_generator = Mock()
        service._stream_agent_response = Mock(return_value=mock_generator)
        
        # Call the method
        result = service.stream_agent_response(agent_id, query)
        
        # Verify the result
        assert result is mock_generator
        service._stream_agent_response.assert_called_once_with(agent_id, query)
    
    @pytest.mark.asyncio
    async def test_stream_agent_response(self, service, mock_execution_repo):
        """Test the internal streaming method."""
        agent_id = "test-agent-id"
        query = "What is the weather today?"
        
        # Mock the execution repository
        mock_execution_repo.create = AsyncMock()
        mock_execution_repo.update = AsyncMock()
        
        # Call the method
        generator = service._stream_agent_response(agent_id, query)
        
        # Collect all streamed events
        events = []
        async for event in generator:
            events.append(event)
        
        # Verify we got some events
        assert len(events) > 0
        
        # Verify the execution repository was called
        mock_execution_repo.create.assert_awaited_once()
        mock_execution_repo.update.assert_awaited()
        
        # Verify the structure of events
        for event in events:
            assert "event" in event
            assert "data" in event
            
            data = event["data"]
            assert "type" in data
            
            if data["type"] == "message":
                assert "content" in data
                assert "timestamp" in data
            elif data["type"] == "result":
                assert "content" in data
            elif data["type"] == "complete":
                assert "execution_id" in data
            elif data["type"] == "error":
                assert "message" in data
