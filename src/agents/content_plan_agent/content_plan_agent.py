import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.hackernews import HackerNewsTools
from agno.tools.newspaper4k import Newspaper4kTools
from agno.tools.googlesearch import GoogleSearchTools
from src.prompts.agent_prompts import AgentPrompts

class ContentPlanAgent():
    def __init__(self):
        self.agent = Agent(
            name="Content Plan Agent",
            model=OpenAIChat(id="gpt-4o", temperature=0.7),  # Higher temperature for creativity
            tools=[HackerNewsTools(), Newspaper4kTools(), GoogleSearchTools()],
            instructions=AgentPrompts.CONTENT_PLAN_AGENT_INSTRUCTIONS,
            markdown=True,
        )

    def run(self, topic: str, audience_insights: str = "", channel_strategy: str = "", brand_messaging: str = "", stream: bool = False):
        context = f"Product/Idea: {topic}"
        if audience_insights:
            context += f"\n\nAudience Insights: {audience_insights}"
        if channel_strategy:
            context += f"\n\nChannel Strategy: {channel_strategy}"
        if brand_messaging:
            context += f"\n\nBrand Messaging: {brand_messaging}"
        
        return self.agent.run(f"Create a comprehensive content strategy and calendar for: {context}", stream=stream)
    
if __name__ == "__main__":
    content_plan_agent = ContentPlanAgent()
    try:
        response = content_plan_agent.run("AI-powered project management tool", stream=False)
        if response is not None:
            # Access the content attribute from the RunOutput object
            print(getattr(response, 'content', str(response)))

    except Exception as e:
        print(f"Error occurred in ContentPlanAgent: {e}")