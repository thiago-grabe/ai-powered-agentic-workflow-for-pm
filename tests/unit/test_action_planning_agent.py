"""
Unit tests for ActionPlanningAgent.
All OpenAI API calls are mocked.
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'phase_1'))

from workflow_agents.base_agents import ActionPlanningAgent


class TestActionPlanningAgent:
    """Test cases for ActionPlanningAgent."""
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_initialization(self, mock_openai, mock_openai_api_key, sample_knowledge):
        """Test that ActionPlanningAgent initializes correctly."""
        agent = ActionPlanningAgent(mock_openai_api_key, sample_knowledge)
        assert agent.openai_api_key == mock_openai_api_key
        assert agent.knowledge == sample_knowledge
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_extract_steps_returns_list(self, mock_openai, mock_openai_api_key, sample_knowledge):
        """Test that extract_steps_from_prompt returns a list of steps."""
        # Setup mock
        mock_client = MagicMock()
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "1. First step\n2. Second step\n3. Third step"
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client
        
        agent = ActionPlanningAgent(mock_openai_api_key, sample_knowledge)
        steps = agent.extract_steps_from_prompt("How do I complete this task?")
        
        assert isinstance(steps, list)
        assert len(steps) == 3
        assert "First step" in steps[0]
        assert "Second step" in steps[1]
        assert "Third step" in steps[2]
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_extract_steps_uses_knowledge(self, mock_openai, mock_openai_api_key):
        """Test that extract_steps_from_prompt uses provided knowledge."""
        knowledge = "Step 1: Do A\nStep 2: Do B\nStep 3: Do C"
        
        # Setup mock
        mock_client = MagicMock()
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "1. Do A\n2. Do B\n3. Do C"
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client
        
        agent = ActionPlanningAgent(mock_openai_api_key, knowledge)
        steps = agent.extract_steps_from_prompt("Extract the steps")
        
        # Verify knowledge was included in system prompt
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        system_message = call_kwargs['messages'][0]['content']
        assert knowledge in system_message
        assert "action planning agent" in system_message.lower()
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_extract_steps_cleans_output(self, mock_openai, mock_openai_api_key, sample_knowledge):
        """Test that extract_steps_from_prompt cleans the output."""
        # Setup mock with messy output
        mock_client = MagicMock()
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "1. First step\n\n2. Second step\n\n\n3. Third step\n\n"
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client
        
        agent = ActionPlanningAgent(mock_openai_api_key, sample_knowledge)
        steps = agent.extract_steps_from_prompt("Extract steps")
        
        # Should remove empty lines
        assert all(len(step.strip()) > 0 for step in steps)
        # Should not have empty strings
        assert "" not in steps

