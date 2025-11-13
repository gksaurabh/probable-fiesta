from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

from src.agents.audience_insight_agent import AudienceInsightAgent
from src.agents.competitor_scan_agent import CompetitorScanAgent
from src.agents.uvp_agent import UVPAgent
from src.agents.channel_strategy_agent import ChannelStrategyAgent
from src.teams.statergy_lead_orchestrator import StatergyLeadTeam

audience_insight_agent = AudienceInsightAgent().agent
competitor_scan_agent = CompetitorScanAgent().agent
uvp_agent = UVPAgent().agent
channel_strategy_agent = ChannelStrategyAgent().agent
statergy_lead_team = StatergyLeadTeam().team

agent_os = AgentOS(agents=[audience_insight_agent, competitor_scan_agent, uvp_agent, channel_strategy_agent], teams=[statergy_lead_team])
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve("agentos:app", reload=True)