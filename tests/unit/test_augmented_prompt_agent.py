"""
Unit tests for AugmentedPromptAgent.
All OpenAI API calls are mocked.
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'phase_1'))

from workflow_agents.base_agents import AugmentedPromptAgent


class TestAugmentedPromptAgent:
    """Test cases for AugmentedPromptAgent."""
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_initialization(self, mock_openai, mock_openai_api_key, sample_persona):
        """Test that AugmentedPromptAgent initializes correctly."""
        agent = AugmentedPromptAgent(mock_openai_api_key, sample_persona)
        assert agent.openai_api_key == mock_openai_api_key
        assert agent.persona == sample_persona
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_respond_uses_persona(self, mock_openai, mock_openai_api_key, sample_persona, sample_prompt):
        """Test that respond method uses the persona in system prompt."""
        # Setup mock
        mock_client = MagicMock()
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Dear students, Paris is the capital."
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client
        
        agent = AugmentedPromptAgent(mock_openai_api_key, sample_persona)
        response = agent.respond(sample_prompt)
        
        # Verify system prompt includes persona
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        messages = call_kwargs['messages']
        assert len(messages) == 2
        assert messages[0]['role'] == 'system'
        assert sample_persona in messages[0]['content']
        assert 'Forget all previous context' in messages[0]['content']
        assert messages[1]['role'] == 'user'
        assert messages[1]['content'] == sample_prompt
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_respond_returns_string(self, mock_openai, mock_openai_api_key, sample_persona, sample_prompt):
        """Test that respond method returns a string."""
        # Setup mock
        mock_client = MagicMock()
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Response with persona"
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client
        
        agent = AugmentedPromptAgent(mock_openai_api_key, sample_persona)
        response = agent.respond(sample_prompt)
        
        assert isinstance(response, str)
        assert response == "Response with persona"

