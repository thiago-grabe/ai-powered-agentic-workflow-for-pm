"""
Unit tests for RoutingAgent.
All OpenAI API calls are mocked.
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os
import numpy as np

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'phase_1'))

from workflow_agents.base_agents import RoutingAgent


class TestRoutingAgent:
    """Test cases for RoutingAgent."""
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_initialization(self, mock_openai, mock_openai_api_key):
        """Test that RoutingAgent initializes correctly."""
        agent = RoutingAgent(mock_openai_api_key)
        assert agent.openai_api_key == mock_openai_api_key
        assert agent.agents == []
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_initialization_with_agents(self, mock_openai, mock_openai_api_key, mock_agent_descriptions):
        """Test that RoutingAgent initializes with agents."""
        agent = RoutingAgent(mock_openai_api_key, mock_agent_descriptions)
        assert agent.agents == mock_agent_descriptions
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_get_embedding(self, mock_openai, mock_openai_api_key):
        """Test that get_embedding returns an embedding vector."""
        # Setup mock
        mock_client = MagicMock()
        mock_embedding_response = MagicMock()
        test_embedding = np.random.rand(3072).tolist()
        mock_embedding_response.data[0].embedding = test_embedding
        mock_client.embeddings.create.return_value = mock_embedding_response
        mock_openai.return_value = mock_client
        
        agent = RoutingAgent(mock_openai_api_key)
        embedding = agent.get_embedding("test text")
        
        assert embedding == test_embedding
        mock_client.embeddings.create.assert_called_once()
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_route_selects_best_agent(self, mock_openai, mock_openai_api_key):
        """Test that route selects agent with highest similarity."""
        # Setup mock embeddings
        mock_client = MagicMock()
        
        # Create different embeddings for prompt and agents
        prompt_embedding = np.array([1.0, 0.0, 0.0])
        agent1_embedding = np.array([0.9, 0.1, 0.0])  # High similarity
        agent2_embedding = np.array([0.0, 0.0, 1.0])  # Low similarity
        
        # Mock embeddings.create to return different embeddings based on call order
        embeddings_to_return = [prompt_embedding, agent1_embedding, agent2_embedding]
        embedding_index = [0]
        
        def mock_create_embedding(*args, **kwargs):
            mock_response = MagicMock()
            mock_response.data[0].embedding = embeddings_to_return[embedding_index[0]].tolist()
            embedding_index[0] += 1
            return mock_response
        
        mock_client.embeddings.create.side_effect = mock_create_embedding
        mock_openai.return_value = mock_client
        
        # Create agents
        agent1_called = [False]
        agent2_called = [False]
        
        def agent1_func(x):
            agent1_called[0] = True
            return "Agent 1 response"
        
        def agent2_func(x):
            agent2_called[0] = True
            return "Agent 2 response"
        
        agents = [
            {
                "name": "agent1",
                "description": "Similar to prompt",
                "func": agent1_func
            },
            {
                "name": "agent2",
                "description": "Different from prompt",
                "func": agent2_func
            }
        ]
        
        router = RoutingAgent(mock_openai_api_key, agents)
        result = router.route("test prompt")
        
        # Agent 1 should be selected (higher similarity)
        assert agent1_called[0] == True
        assert agent2_called[0] == False
        assert result == "Agent 1 response"

