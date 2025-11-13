import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.hackernews import HackerNewsTools
from agno.tools.newspaper4k import Newspaper4kTools
from agno.tools.googlesearch import GoogleSearchTools
from src.prompts.agent_prompts import AgentPrompts

class AudienceInsightAgent():
    def __init__(self):
        self.agent = Agent(
            name="Audience Insight Agent",
            model=OpenAIChat(id="gpt-4o", temperature=0.5),
            tools=[HackerNewsTools(), Newspaper4kTools(), GoogleSearchTools()],
            instructions=AgentPrompts.AUDIENCE_INSIGHT_AGENT_INSTRUCTIONS,
            markdown=True,
        )

    def run(self, topic: str, stream: bool = False):
        return self.agent.run(f"Write a detailed report on the topic: {topic}", stream=stream)
    
if __name__ == "__main__":
    audience_insight_agent = AudienceInsightAgent()
    try:
        response = audience_insight_agent.run("renewable energy", stream=False)
        if response is not None:
            # Access the content attribute from the RunOutput object
            print(getattr(response, 'content', str(response)))

    except Exception as e:
        print(f"Error occurred in AudienceInsightAgent: {e}")