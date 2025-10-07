"""
Unit tests for DirectPromptAgent.
All OpenAI API calls are mocked.
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'phase_1'))

from workflow_agents.base_agents import DirectPromptAgent


class TestDirectPromptAgent:
    """Test cases for DirectPromptAgent."""
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_initialization(self, mock_openai, mock_openai_api_key):
        """Test that DirectPromptAgent initializes correctly."""
        agent = DirectPromptAgent(mock_openai_api_key)
        assert agent.openai_api_key == mock_openai_api_key
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_respond_returns_string(self, mock_openai, mock_openai_api_key, sample_prompt):
        """Test that respond method returns a string."""
        # Setup mock
        mock_client = MagicMock()
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Paris"
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client
        
        agent = DirectPromptAgent(mock_openai_api_key)
        response = agent.respond(sample_prompt)
        
        assert isinstance(response, str)
        assert response == "Paris"
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_respond_calls_openai_with_correct_params(self, mock_openai, mock_openai_api_key, sample_prompt):
        """Test that respond method calls OpenAI API with correct parameters."""
        # Setup mock
        mock_client = MagicMock()
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Paris"
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client
        
        agent = DirectPromptAgent(mock_openai_api_key)
        agent.respond(sample_prompt)
        
        # Verify OpenAI was instantiated with Vocareum base URL
        mock_openai.assert_called_once_with(
            base_url="https://openai.vocareum.com/v1",
            api_key=mock_openai_api_key
        )
        
        # Verify chat completion was called
        mock_client.chat.completions.create.assert_called_once()
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        assert call_kwargs['model'] == 'gpt-3.5-turbo'
        assert call_kwargs['temperature'] == 0
        assert len(call_kwargs['messages']) == 1
        assert call_kwargs['messages'][0]['role'] == 'user'
        assert call_kwargs['messages'][0]['content'] == sample_prompt
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_respond_without_system_prompt(self, mock_openai, mock_openai_api_key, sample_prompt):
        """Test that DirectPromptAgent does not use a system prompt."""
        # Setup mock
        mock_client = MagicMock()
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Paris"
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client
        
        agent = DirectPromptAgent(mock_openai_api_key)
        agent.respond(sample_prompt)
        
        # Verify no system message
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        messages = call_kwargs['messages']
        assert all(msg['role'] != 'system' for msg in messages)

