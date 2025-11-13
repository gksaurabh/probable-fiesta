
import os
import sys

from agno.team import Team
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from src.prompts.agent_prompts import AgentPrompts
from src.agents.audience_insight_agent.audience_insight_agent import AudienceInsightAgent
from src.agents.competitor_scan_agent.competitor_scan_agent import CompetitorScanAgent
from src.agents.uvp_agent.uvp_agent import UVPAgent
from src.agents.channel_strategy_agent.channel_strategy_agent import ChannelStrategyAgent


class StatergyLeadTeam():
    def __init__(self):
        audience_insight_agent = AudienceInsightAgent()
        competitor_scan_agent = CompetitorScanAgent()
        uvp_agent = UVPAgent()
        channel_strategy_agent = ChannelStrategyAgent()
        self.team = Team(
            name="Statergy Lead Team",
            members=[audience_insight_agent.agent, competitor_scan_agent.agent, uvp_agent.agent, channel_strategy_agent.agent],
            model=OpenAIChat(id="gpt-4o"),
            instructions=AgentPrompts.STATERGY_LEAD_TEAM_INSTRUCTIONS,
            tools=[ReasoningTools(add_instructions=True), DuckDuckGoTools()],
            reasoning=True,
            show_members_responses=True,
            share_member_interactions=True,
            delegate_task_to_all_members=True,
            get_member_information_tool=True,
            stream_intermediate_steps=True,
            store_member_responses=True,
            markdown=True
        )
    
    def run(self, topic: str, stream: bool = False):
        return self.team.run(f"Based on the reports from all agents, provide a comprehensive and balanced final assessment on the topic: {topic}", stream=stream)
    
if __name__ == "__main__":
    statergy_lead_team = StatergyLeadTeam()
    try:
        # response = statergy_lead_team.run("The future of renewable energy", stream=False)
        # if response is not None:
        #     # Access the content attribute from the RunOutput object
        #     print(getattr(response, 'content', str(response)))

        statergy_lead_team.team.print_response("i am thinking of creating a b2b app that helps with agent orchestration in a distributed system", stream=True)

    except Exception as e:
        print(f"Error occurred in StatergyLeadTeam: {e}")