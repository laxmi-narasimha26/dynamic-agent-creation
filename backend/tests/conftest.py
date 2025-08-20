import sys
import os
import pytest

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(autouse=True)
def setup_environment():
    """Set up environment variables for tests."""
    os.environ.setdefault('DATABASE_URL', 'postgresql://test:test@localhost:5432/test_db')
    os.environ.setdefault('REDIS_URL', 'redis://localhost:6379/1')
    os.environ.setdefault('OPENAI_API_KEY', 'test-key')
    
    yield
    
    # Clean up environment variables after tests
    if 'DATABASE_URL' in os.environ and os.environ['DATABASE_URL'].endswith('test_db'):
        del os.environ['DATABASE_URL']
    if 'REDIS_URL' in os.environ and '6379/1' in os.environ['REDIS_URL']:
        del os.environ['REDIS_URL']
    if 'OPENAI_API_KEY' in os.environ and os.environ['OPENAI_API_KEY'] == 'test-key':
        del os.environ['OPENAI_API_KEY']
