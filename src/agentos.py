from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

from src.agents.forecaster.forecaster_agent import ForecasterAgent
from src.agents.historian.historian_agent import HistorianAgent 
from src.agents.optimist.optimist_agent import OptimistAgent
from src.agents.pessimist.pessimist_agent import PessimistAgent
from src.teams.judge.judge_team import JudgeTeam

forecaster_agent = ForecasterAgent().agent
historian_agent = HistorianAgent().agent
optimist_agent = OptimistAgent().agent
pessimist_agent = PessimistAgent().agent
judge_team = JudgeTeam().team

agent_os = AgentOS(agents=[forecaster_agent, historian_agent, optimist_agent, pessimist_agent], teams=[judge_team])
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve("agentos:app", reload=True)