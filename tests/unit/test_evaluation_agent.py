"""
Unit tests for EvaluationAgent.
All OpenAI API calls are mocked.
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'phase_1'))

from workflow_agents.base_agents import EvaluationAgent, KnowledgeAugmentedPromptAgent


class TestEvaluationAgent:
    """Test cases for EvaluationAgent."""
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_initialization(self, mock_openai, mock_openai_api_key, sample_persona, mock_evaluation_criteria):
        """Test that EvaluationAgent initializes correctly."""
        # Create a mock worker agent
        mock_worker = MagicMock()
        
        agent = EvaluationAgent(
            mock_openai_api_key,
            sample_persona,
            mock_evaluation_criteria,
            mock_worker,
            max_interactions=5
        )
        
        assert agent.openai_api_key == mock_openai_api_key
        assert agent.persona == sample_persona
        assert agent.evaluation_criteria == mock_evaluation_criteria
        assert agent.agent_to_evaluate == mock_worker
        assert agent.max_interactions == 5
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_evaluate_accepts_good_response(self, mock_openai, mock_openai_api_key, sample_persona, mock_evaluation_criteria, sample_prompt):
        """Test that evaluation accepts a response that meets criteria."""
        # Setup mock worker agent
        mock_worker = MagicMock()
        mock_worker.respond.return_value = "Paris"
        
        # Setup mock OpenAI client
        mock_client = MagicMock()
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Yes, the answer meets the criteria."
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client
        
        agent = EvaluationAgent(
            mock_openai_api_key,
            sample_persona,
            mock_evaluation_criteria,
            mock_worker,
            max_interactions=3
        )
        
        result = agent.evaluate(sample_prompt)
        
        assert 'final_response' in result
        assert 'evaluation' in result
        assert 'iterations' in result
        assert result['final_response'] == "Paris"
        assert result['iterations'] == 1
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_evaluate_iterates_on_bad_response(self, mock_openai, mock_openai_api_key, sample_persona, mock_evaluation_criteria, sample_prompt):
        """Test that evaluation iterates when response doesn't meet criteria."""
        # Setup mock worker agent
        mock_worker = MagicMock()
        mock_worker.respond.side_effect = [
            "The capital of France is a beautiful city",  # First attempt - too verbose
            "Paris"  # Second attempt - correct
        ]
        
        # Setup mock OpenAI client
        mock_client = MagicMock()
        evaluation_responses = [
            "No, the answer should be a single word.",
            "Yes, the answer meets the criteria."
        ]
        instruction_response = "Please provide only the city name, nothing else."
        
        responses = []
        for eval_resp in evaluation_responses:
            mock_comp = MagicMock()
            mock_comp.choices[0].message.content = eval_resp
            responses.append(mock_comp)
        
        # Add instruction response
        mock_inst = MagicMock()
        mock_inst.choices[0].message.content = instruction_response
        responses.insert(1, mock_inst)
        
        mock_client.chat.completions.create.side_effect = responses
        mock_openai.return_value = mock_client
        
        agent = EvaluationAgent(
            mock_openai_api_key,
            sample_persona,
            mock_evaluation_criteria,
            mock_worker,
            max_interactions=3
        )
        
        result = agent.evaluate(sample_prompt)
        
        assert result['iterations'] == 2
        assert mock_worker.respond.call_count == 2
    
    @patch('workflow_agents.base_agents.OpenAI')
    def test_evaluate_stops_at_max_iterations(self, mock_openai, mock_openai_api_key, sample_persona, mock_evaluation_criteria, sample_prompt):
        """Test that evaluation stops at max iterations."""
        # Setup mock worker agent that always gives bad responses
        mock_worker = MagicMock()
        mock_worker.respond.return_value = "A verbose answer that doesn't meet criteria"
        
        # Setup mock OpenAI client that always rejects
        mock_client = MagicMock()
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "No, the answer doesn't meet criteria."
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client
        
        max_iter = 2
        agent = EvaluationAgent(
            mock_openai_api_key,
            sample_persona,
            mock_evaluation_criteria,
            mock_worker,
            max_interactions=max_iter
        )
        
        result = agent.evaluate(sample_prompt)
        
        assert result['iterations'] == max_iter
        assert mock_worker.respond.call_count == max_iter

