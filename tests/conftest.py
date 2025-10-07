"""
Pytest configuration and fixtures for testing AI agents.
All OpenAI API calls are mocked to avoid actual API usage during tests.
"""

import pytest
from unittest.mock import Mock, MagicMock
import numpy as np


@pytest.fixture
def mock_openai_api_key():
    """Provide a mock API key for testing."""
    return "test-api-key-12345"


@pytest.fixture
def mock_openai_client(monkeypatch):
    """Mock the OpenAI client to avoid actual API calls."""
    mock_client = MagicMock()
    
    # Mock chat completions
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock()]
    mock_completion.choices[0].message.content = "This is a mocked response from the LLM."
    mock_client.chat.completions.create.return_value = mock_completion
    
    # Mock embeddings
    mock_embedding_response = MagicMock()
    mock_embedding_response.data = [MagicMock()]
    mock_embedding_response.data[0].embedding = np.random.rand(3072).tolist()
    mock_client.embeddings.create.return_value = mock_embedding_response
    
    # Mock the OpenAI class to return our mock client
    def mock_openai_init(*args, **kwargs):
        return mock_client
    
    from unittest.mock import patch
    with patch('src.phase_1.workflow_agents.base_agents.OpenAI', side_effect=mock_openai_init):
        yield mock_client


@pytest.fixture
def sample_persona():
    """Provide a sample persona for testing."""
    return "You are a helpful assistant"


@pytest.fixture
def sample_knowledge():
    """Provide sample knowledge for testing."""
    return "The capital of France is Paris. France is located in Europe."


@pytest.fixture
def sample_prompt():
    """Provide a sample prompt for testing."""
    return "What is the capital of France?"


@pytest.fixture
def mock_evaluation_criteria():
    """Provide mock evaluation criteria."""
    return "The answer should be a single word representing a city name."


@pytest.fixture
def mock_agent_descriptions():
    """Provide mock agent descriptions for routing tests."""
    return [
        {
            "name": "geography_agent",
            "description": "Answers questions about geography, countries, and cities",
            "func": lambda x: "Geography response"
        },
        {
            "name": "math_agent",
            "description": "Solves mathematical problems and equations",
            "func": lambda x: "Math response"
        }
    ]

