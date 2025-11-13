import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.hackernews import HackerNewsTools
from agno.tools.newspaper4k import Newspaper4kTools
from agno.tools.googlesearch import GoogleSearchTools
from src.prompts.agent_prompts import AgentPrompts

class CompetitorScanAgent():
    def __init__(self):
        self.agent = Agent(
            name="Competitor Scan Agent",
            model=OpenAIChat(id="gpt-4o", temperature=0.5),
            tools=[HackerNewsTools(), Newspaper4kTools(), GoogleSearchTools()],
            instructions=AgentPrompts.COMPETITOR_SCAN_AGENT_INSTRUCTIONS,
            markdown=True,
        )

    def run(self, topic: str, stream: bool = False):
        return self.agent.run(f"Analyze the competitive landscape for: {topic}", stream=stream)
    
if __name__ == "__main__":
    competitor_scan_agent = CompetitorScanAgent()
    try:
        response = competitor_scan_agent.run("AI-powered project management tool", stream=False)
        if response is not None:
            # Access the content attribute from the RunOutput object
            print(getattr(response, 'content', str(response)))

    except Exception as e:
        print(f"Error occurred in CompetitorScanAgent: {e}")