import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.hackernews import HackerNewsTools
from agno.tools.newspaper4k import Newspaper4kTools
from agno.tools.googlesearch import GoogleSearchTools
from src.prompts.agent_prompts import AgentPrompts

class UVPAgent():
    def __init__(self):
        self.agent = Agent(
            name="UVP Agent",
            model=OpenAIChat(id="gpt-4o", temperature=0.5),
            tools=[HackerNewsTools(), Newspaper4kTools(), GoogleSearchTools()],
            instructions=AgentPrompts.UVP_AGENT_INSTRUCTIONS,
            markdown=True,
        )

    def run(self, topic: str, audience_insights: str = "", competitive_analysis: str = "", stream: bool = False):
        context = f"Product/Idea: {topic}"
        if audience_insights:
            context += f"\n\nAudience Insights: {audience_insights}"
        if competitive_analysis:
            context += f"\n\nCompetitive Analysis: {competitive_analysis}"
        
        return self.agent.run(f"Define a unique value proposition for: {context}", stream=stream)
    
if __name__ == "__main__":
    uvp_agent = UVPAgent()
    try:
        response = uvp_agent.run("AI-powered project management tool", stream=False)
        if response is not None:
            # Access the content attribute from the RunOutput object
            print(getattr(response, 'content', str(response)))

    except Exception as e:
        print(f"Error occurred in UVPAgent: {e}")