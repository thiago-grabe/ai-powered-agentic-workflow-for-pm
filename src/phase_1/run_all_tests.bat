@echo off
REM Script to run all Phase 1 agent tests on Windows
REM Make sure you have activated your virtual environment and set up .env before running

echo ======================================================================
echo Running All Phase 1 Agent Tests
echo ======================================================================
echo.
echo Make sure you have:
echo   1. Activated your virtual environment
echo   2. Created a .env file with your OPENAI_API_KEY
echo.
pause

echo.
echo ======================================================================
echo Test 1: DirectPromptAgent
echo ======================================================================
python direct_prompt_agent.py
echo.
pause

echo.
echo ======================================================================
echo Test 2: AugmentedPromptAgent
echo ======================================================================
python augmented_prompt_agent.py
echo.
pause

echo.
echo ======================================================================
echo Test 3: KnowledgeAugmentedPromptAgent
echo ======================================================================
python knowledge_augmented_prompt_agent.py
echo.
pause

echo.
echo ======================================================================
echo Test 4: RAGKnowledgePromptAgent
echo ======================================================================
python rag_knowledge_prompt_agent.py
echo.
pause

echo.
echo ======================================================================
echo Test 5: EvaluationAgent
echo ======================================================================
python evaluation_agent.py
echo.
pause

echo.
echo ======================================================================
echo Test 6: RoutingAgent
echo ======================================================================
python routing_agent.py
echo.
pause

echo.
echo ======================================================================
echo Test 7: ActionPlanningAgent
echo ======================================================================
python action_planning_agent.py
echo.

echo.
echo ======================================================================
echo All Phase 1 Tests Completed!
echo ======================================================================
echo.
echo Please review the outputs and capture screenshots or save to text files
echo for your project submission.
echo.
pause

