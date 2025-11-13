import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.hackernews import HackerNewsTools
from agno.tools.newspaper4k import Newspaper4kTools
from agno.tools.googlesearch import GoogleSearchTools
from src.prompts.agent_prompts import AgentPrompts

class ChannelStrategyAgent():
    def __init__(self):
        self.agent = Agent(
            name="Channel Strategy Agent",
            model=OpenAIChat(id="gpt-4o", temperature=0.5),
            tools=[HackerNewsTools(), Newspaper4kTools(), GoogleSearchTools()],
            instructions=AgentPrompts.CHANNEL_STRATEGY_AGENT_INSTRUCTIONS,
            markdown=True,
        )

    def run(self, topic: str, audience_profiles: str = "", budget_constraints: str = "", stream: bool = False):
        context = f"Product/Idea: {topic}"
        if audience_profiles:
            context += f"\n\nTarget Audience: {audience_profiles}"
        if budget_constraints:
            context += f"\n\nBudget Constraints: {budget_constraints}"
        
        return self.agent.run(f"Develop a channel strategy for: {context}", stream=stream)
    
if __name__ == "__main__":
    channel_strategy_agent = ChannelStrategyAgent()
    try:
        response = channel_strategy_agent.run("AI-powered project management tool", stream=False)
        if response is not None:
            # Access the content attribute from the RunOutput object
            print(getattr(response, 'content', str(response)))

    except Exception as e:
        print(f"Error occurred in ChannelStrategyAgent: {e}")