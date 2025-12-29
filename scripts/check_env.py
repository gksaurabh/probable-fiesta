import os
import sys
from agno.agent import Agent
from agno.models.openai import OpenAIChat

def check_env():
    print("Checking environment...")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY is not set.")
        return False
    
    print("OPENAI_API_KEY is set.")
    
    try:
        print("Testing OpenAI connection...")
        agent = Agent(model=OpenAIChat(id="gpt-4o-mini"))
        response = agent.run("Hello, are you working?")
        print(f"Agent response: {response.content}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to run agent: {e}")
        return False

if __name__ == "__main__":
    success = check_env()
    sys.exit(0 if success else 1)
