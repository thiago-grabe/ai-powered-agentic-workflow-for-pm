# Test Suite

This directory contains comprehensive tests for the AI-Powered Agentic Workflow project.

## Test Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── unit/                    # Unit tests with mocked APIs
│   ├── test_direct_prompt_agent.py
│   ├── test_augmented_prompt_agent.py
│   ├── test_knowledge_augmented_prompt_agent.py
│   ├── test_evaluation_agent.py
│   ├── test_routing_agent.py
│   └── test_action_planning_agent.py
└── README.md               # This file
```

## Running Tests

### Option 1: Run Pytest (Mocked - No API Calls)

Run all unit tests with mocked OpenAI API calls:

```bash
# From project root
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_direct_prompt_agent.py

# Run specific test
pytest tests/unit/test_direct_prompt_agent.py::TestDirectPromptAgent::test_initialization

# Run with coverage (if pytest-cov installed)
pytest --cov=src --cov-report=html
```

### Option 2: Run Integration Tests (Actual API Calls)

Run the test scripts with actual OpenAI API calls:

```bash
# From project root
./run_all_tests.sh

# Or run individual test scripts from src/phase_1/
cd src/phase_1
python direct_prompt_agent.py
python augmented_prompt_agent.py
# ... etc
```

## Test Types

### Unit Tests (tests/unit/)
- **Mocked**: All OpenAI API calls are mocked
- **Fast**: Run in seconds
- **No Cost**: No API credits used
- **Purpose**: Verify code logic and structure

### Integration Tests (src/phase_1/*.py)
- **Real API**: Actual OpenAI API calls
- **Slower**: Takes minutes due to API latency
- **Costs Credits**: Uses OpenAI API credits
- **Purpose**: Verify end-to-end functionality

## Mocking Strategy

All unit tests mock the OpenAI client to:
1. Avoid API costs during testing
2. Speed up test execution
3. Allow testing without API key
4. Provide deterministic test results

Example mock setup:
```python
@patch('workflow_agents.base_agents.OpenAI')
def test_something(mock_openai):
    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = "Mocked response"
    mock_client.chat.completions.create.return_value = mock_completion
    mock_openai.return_value = mock_client
    # ... rest of test
```

## Test Fixtures

Common fixtures are defined in `conftest.py`:
- `mock_openai_api_key`: Mock API key
- `mock_openai_client`: Mocked OpenAI client
- `sample_persona`: Sample persona for testing
- `sample_knowledge`: Sample knowledge for testing
- `sample_prompt`: Sample prompt for testing
- `mock_evaluation_criteria`: Sample evaluation criteria
- `mock_agent_descriptions`: Sample agent descriptions for routing

## Adding New Tests

1. Create a new test file in `tests/unit/`
2. Follow the naming convention: `test_<module_name>.py`
3. Use the `TestClassName` pattern for test classes
4. Mock all OpenAI API calls
5. Use fixtures from `conftest.py` when applicable

Example:
```python
import pytest
from unittest.mock import patch, MagicMock

class TestMyNewAgent:
    @patch('workflow_agents.base_agents.OpenAI')
    def test_initialization(self, mock_openai, mock_openai_api_key):
        agent = MyNewAgent(mock_openai_api_key)
        assert agent.openai_api_key == mock_openai_api_key
```

## Continuous Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest -v
```

## Requirements

Install test dependencies:
```bash
pip install -r requirements.txt
```

Or with uv:
```bash
uv pip install -r requirements.txt
```

## Test Coverage

To generate coverage reports (requires pytest-cov):
```bash
pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

## Troubleshooting

### Import Errors
If you get import errors, make sure you're running pytest from the project root:
```bash
cd /Users/73983/ws/grabe/ai-powered-agentic-workflow-for-pm
pytest
```

### Mocking Issues
If mocks aren't working, verify the patch path matches the actual import location in your code.

### Slow Tests
If tests are slow, ensure you're using mocked tests (unit tests) not integration tests.

## Best Practices

1. **Keep tests isolated**: Each test should be independent
2. **Mock external dependencies**: Don't make real API calls in unit tests
3. **Test edge cases**: Include tests for error conditions
4. **Use descriptive names**: Test names should describe what they test
5. **Keep tests simple**: One assertion per test when possible
6. **Use fixtures**: Reuse common setup code via fixtures

