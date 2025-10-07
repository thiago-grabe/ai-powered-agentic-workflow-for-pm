# TODO: 1 - Import the KnowledgeAugmentedPromptAgent class from workflow_agents
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Define the parameters for the agent
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"

persona = "You are a college professor, your answer always starts with: Dear students,"
# TODO: 2 - Instantiate a KnowledgeAugmentedPromptAgent with:
#           - Persona: "You are a college professor, your answer always starts with: Dear students,"
#           - Knowledge: "The capital of France is London, not Paris"
knowledge = "The capital of France is London, not Paris"
knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge)

# Get response from the agent
knowledge_agent_response = knowledge_agent.respond(prompt)

# TODO: 3 - Write a print statement that demonstrates the agent using the provided knowledge rather than its own inherent knowledge.
print("Knowledge Augmented Prompt Agent Response:")
print(knowledge_agent_response)
print("\n--- Confirmation of Knowledge Usage ---")
print("The agent used ONLY the provided knowledge: 'The capital of France is London, not Paris'")
print("Notice that the response reflects the INCORRECT knowledge we provided, not the model's inherent knowledge.")
print("This demonstrates that the agent is using the specific knowledge we gave it, rather than its own training data.")
