import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.hackernews import HackerNewsTools
from agno.tools.newspaper4k import Newspaper4kTools
from agno.tools.googlesearch import GoogleSearchTools
from src.prompts.agent_prompts import AgentPrompts

class HumanReviewAgent():
    pass
    
if __name__ == "__main__":
    human_review_agent = HumanReviewAgent()
    try:
        pass

    except Exception as e:
        print(f"Error occurred in HumanReviewAgent: {e}")