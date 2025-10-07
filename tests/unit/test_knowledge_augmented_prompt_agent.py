"""
Unit tests for KnowledgeAugmentedPromptAgent.
All OpenAI API calls are mocked.
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'phase_1'))

from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent


class TestKnowledgeAugmentedPromptAgent:
    """Test cases for KnowledgeAugmentedPromptAgent."""
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_initialization(self, mock_openai, mock_openai_api_key, sample_persona, sample_knowledge):
        """Test that KnowledgeAugmentedPromptAgent initializes correctly."""
        agent = KnowledgeAugmentedPromptAgent(mock_openai_api_key, sample_persona, sample_knowledge)
        assert agent.openai_api_key == mock_openai_api_key
        assert agent.persona == sample_persona
        assert agent.knowledge == sample_knowledge
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_respond_uses_knowledge(self, mock_openai, mock_openai_api_key, sample_persona, sample_knowledge, sample_prompt):
        """Test that respond method uses the provided knowledge."""
        # Setup mock
        mock_client = MagicMock()
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Paris"
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client
        
        agent = KnowledgeAugmentedPromptAgent(mock_openai_api_key, sample_persona, sample_knowledge)
        response = agent.respond(sample_prompt)
        
        # Verify system prompt includes knowledge
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        messages = call_kwargs['messages']
        assert len(messages) == 2
        assert messages[0]['role'] == 'system'
        assert sample_persona in messages[0]['content']
        assert sample_knowledge in messages[0]['content']
        assert 'Use only the following knowledge' in messages[0]['content']
        assert messages[1]['role'] == 'user'
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_respond_restricts_to_provided_knowledge(self, mock_openai, mock_openai_api_key, sample_persona, sample_prompt):
        """Test that agent is instructed to use only provided knowledge."""
        incorrect_knowledge = "The capital of France is London"
        
        # Setup mock
        mock_client = MagicMock()
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "London"  # Using incorrect knowledge
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client
        
        agent = KnowledgeAugmentedPromptAgent(mock_openai_api_key, sample_persona, incorrect_knowledge)
        response = agent.respond(sample_prompt)
        
        # Verify system prompt instructs to use only provided knowledge
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        system_message = call_kwargs['messages'][0]['content']
        assert 'do not use your own knowledge' in system_message.lower()
        assert incorrect_knowledge in system_message

