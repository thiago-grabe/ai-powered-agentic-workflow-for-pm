# AI-Powered Agentic Workflow Implementation Guide

## Project Overview

This project implements a sophisticated AI-powered agentic workflow system for technical project management. The system consists of two phases:

- **Phase 1**: Building a library of reusable AI agents
- **Phase 2**: Orchestrating these agents into a comprehensive project management workflow

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- uv (Python package manager) or pip

### Installation

1. **Create a virtual environment using uv:**
   ```bash
   cd /Users/73983/ws/grabe/ai-powered-agentic-workflow-for-pm
   uv venv
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate  # On Windows
   ```

2. **Install dependencies:**
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Configure API Key:**

   Create a `.env` file in both `src/phase_1/` and `src/phase_2/` directories:
   
   ```bash
   # In src/phase_1/.env
   OPENAI_API_KEY=your_openai_api_key_here
   
   # In src/phase_2/.env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   **Important**: Replace `your_openai_api_key_here` with your actual OpenAI API key.

## Phase 1: Agent Library Testing

The Phase 1 implementation includes seven agent classes:

1. **DirectPromptAgent** - Basic LLM interaction
2. **AugmentedPromptAgent** - Persona-based responses
3. **KnowledgeAugmentedPromptAgent** - Knowledge-constrained responses
4. **RAGKnowledgePromptAgent** - Retrieval-augmented generation
5. **EvaluationAgent** - Iterative response evaluation and refinement
6. **RoutingAgent** - Semantic routing to specialized agents
7. **ActionPlanningAgent** - Task decomposition from high-level prompts

### Running Phase 1 Tests

Navigate to the Phase 1 directory:
```bash
cd src/phase_1
```

#### Test Individual Agents:

```bash
# Test DirectPromptAgent
python direct_prompt_agent.py

# Test AugmentedPromptAgent
python augmented_prompt_agent.py

# Test KnowledgeAugmentedPromptAgent
python knowledge_augmented_prompt_agent.py

# Test RAGKnowledgePromptAgent
python rag_knowledge_prompt_agent.py

# Test EvaluationAgent
python evaluation_agent.py

# Test RoutingAgent
python routing_agent.py

# Test ActionPlanningAgent
python action_planning_agent.py
```

### Expected Outputs

Each test script will:
- Print the agent's response to a specific prompt
- Display explanatory information about the agent's behavior
- Demonstrate the unique capabilities of each agent type

**Note**: The RAGKnowledgePromptAgent test will create temporary CSV files for chunks and embeddings. These can be deleted after testing.

## Phase 2: Agentic Workflow

Phase 2 orchestrates multiple agents to create a complete project management workflow.

### Running the Workflow

Navigate to the Phase 2 directory:
```bash
cd src/phase_2
```

Run the workflow:
```bash
python agentic_workflow.py
```

### Workflow Process

The workflow:
1. Accepts a high-level prompt (e.g., "What would the development tasks for this product be?")
2. Uses the **ActionPlanningAgent** to break down the goal into steps
3. Routes each step to the appropriate specialized team using the **RoutingAgent**:
   - **Product Manager Team**: Generates user stories
   - **Program Manager Team**: Defines product features
   - **Development Engineer Team**: Creates engineering tasks
4. Each team uses:
   - A **KnowledgeAugmentedPromptAgent** to generate content
   - An **EvaluationAgent** to ensure quality and format compliance

### Expected Output

The workflow produces a comprehensive development plan for the Email Router product, including:
- User stories following the format: "As a [user], I want [action] so that [benefit]"
- Product features with names, descriptions, functionality, and benefits
- Engineering tasks with IDs, descriptions, acceptance criteria, effort estimates, and dependencies

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your `.env` file is properly configured in the correct directory
   - Verify your OpenAI API key is valid and has sufficient credits

2. **Import Errors**
   - Make sure you're running scripts from the correct directory
   - Verify the virtual environment is activated

3. **Rate Limiting**
   - The workflow makes multiple API calls; if you hit rate limits, wait a few moments and retry
   - Consider adding delays between agent calls if needed

4. **CSV Files from RAG Agent**
   - The RAG agent creates temporary CSV files (chunks-*.csv and embeddings-*.csv)
   - These can be safely deleted after testing

## Project Structure

```
src/
├── phase_1/
│   ├── workflow_agents/
│   │   ├── __init__.py
│   │   └── base_agents.py          # All agent implementations
│   ├── direct_prompt_agent.py       # Test scripts
│   ├── augmented_prompt_agent.py
│   ├── knowledge_augmented_prompt_agent.py
│   ├── rag_knowledge_prompt_agent.py
│   ├── evaluation_agent.py
│   ├── routing_agent.py
│   ├── action_planning_agent.py
│   └── .env                         # Your API key (create this)
│
└── phase_2/
    ├── workflow_agents/
    │   ├── __init__.py
    │   └── base_agents.py          # Copied from phase_1
    ├── agentic_workflow.py          # Main workflow orchestration
    ├── Product-Spec-Email-Router.txt # Product specification
    └── .env                         # Your API key (create this)
```

## Submission Artifacts

For project submission, you should include:

### Phase 1:
- ✅ Completed `workflow_agents/base_agents.py`
- ✅ All seven test scripts
- Screenshots or text files of test outputs

### Phase 2:
- ✅ Completed `agentic_workflow.py`
- ✅ `workflow_agents/base_agents.py` (copied from Phase 1)
- Screenshot or text file of workflow output

## Key Features

### Agent Capabilities

1. **DirectPromptAgent**: Uses LLM's inherent knowledge directly
2. **AugmentedPromptAgent**: Adds persona for contextual responses
3. **KnowledgeAugmentedPromptAgent**: Constrains responses to specific knowledge
4. **RAGKnowledgePromptAgent**: Retrieves relevant information from large documents
5. **EvaluationAgent**: Iteratively improves responses against criteria
6. **RoutingAgent**: Intelligently directs requests to specialized agents
7. **ActionPlanningAgent**: Decomposes complex tasks into steps

### Workflow Design Principles

- **Modularity**: Each agent is self-contained and reusable
- **Composability**: Agents can be combined in various workflows
- **Evaluation**: Built-in quality control through evaluation agents
- **Routing**: Semantic similarity-based intelligent task distribution
- **Iterative Refinement**: Automatic improvement of agent outputs

## Performance Notes

- Phase 1 tests run quickly (a few seconds per agent)
- Phase 2 workflow may take 2-5 minutes due to multiple agent interactions and evaluations
- The EvaluationAgent may iterate multiple times to meet criteria
- API costs will vary based on the number of tokens processed

## Next Steps

After completing this implementation, you can:

1. Experiment with different workflow prompts
2. Add new specialized agents for additional roles
3. Extend evaluation criteria for stricter quality control
4. Implement error handling and logging
5. Create a web interface for the workflow
6. Add persistence for workflow results

## Support

For issues or questions:
- Review the project rubric in `project_overview.md`
- Check the original instructions in the starter code
- Verify all TODO items are completed
- Ensure your API key has sufficient credits

---

**Congratulations on completing the AI-Powered Agentic Workflow for Project Management!**

