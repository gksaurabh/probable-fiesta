from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl

class Verdict(str, Enum):
    PURSUE = "PURSUE"
    PIVOT = "PIVOT"
    KILL = "KILL"

class Question(BaseModel):
    id: str = Field(..., description="Unique identifier for the question")
    text: str = Field(..., description="The question text")
    guidance: Optional[str] = Field(None, description="Context or suggested answer to help the user")

class Interview(BaseModel):
    questions: List[Question] = Field(default_factory=list, description="Questions asked by the agent")
    answers: Dict[str, str] = Field(default_factory=dict, description="User answers keyed by question ID")

class Meta(BaseModel):
    run_id: str = Field(..., description="Unique identifier for the analysis run")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of report creation")
    model: str = Field(..., description="Model used for the analysis")
    version: str = Field("0.1", description="Schema version")

class Idea(BaseModel):
    title: str = Field(..., description="Title of the idea")
    one_liner: str = Field(..., description="One-sentence summary of the idea")
    expanded_summary: str = Field(..., description="Detailed summary of the idea")
    assumptions: List[str] = Field(default_factory=list, description="Key assumptions made about the idea")

class Audience(BaseModel):
    primary_users: List[str] = Field(default_factory=list, description="List of primary user segments")
    jobs_to_be_done: List[str] = Field(default_factory=list, description="List of jobs to be done for the users")
    personas: List[Dict[str, Any]] = Field(default_factory=list, description="Detailed user personas")

class Market(BaseModel):
    demand_signals: List[str] = Field(default_factory=list, description="Signals indicating market demand")
    competitors: List[str] = Field(default_factory=list, description="List of key competitors")
    positioning: str = Field(..., description="Market positioning statement")

class Risks(BaseModel):
    top_risks: List[str] = Field(default_factory=list, description="Top identified risks")
    mitigations: List[str] = Field(default_factory=list, description="Proposed mitigation strategies")

class Execution(BaseModel):
    mvp_scope: List[str] = Field(default_factory=list, description="Features in scope for the MVP")
    two_week_plan: List[str] = Field(default_factory=list, description="Action plan for the first two weeks")
    two_month_plan: List[str] = Field(default_factory=list, description="Action plan for the first two months")

class ScoreDetail(BaseModel):
    score: float = Field(..., ge=0.0, le=10.0, description="Score between 0 and 10")
    reasoning: str = Field(..., description="Explanation for the score")

class Scores(BaseModel):
    market_demand: ScoreDetail = Field(...)
    competitive_advantage: ScoreDetail = Field(...)
    technical_feasibility: ScoreDetail = Field(...)
    business_viability: ScoreDetail = Field(...)

class Recommendation(BaseModel):
    verdict: Verdict = Field(...)
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0 and 1")
    scores: Optional[Scores] = Field(None, description="Weighted scores for the 4 pillars")
    rationale: str = Field(..., description="Explanation for the recommendation")

class Source(BaseModel):
    title: str = Field(..., description="Title of the source")
    url: str = Field(..., description="URL of the source")
    snippet: Optional[str] = Field(None, description="Relevant snippet from the source")

class AnswerEvaluation(BaseModel):
    question_id: str = Field(..., description="ID of the question being evaluated")
    question_text: str = Field(..., description="The original question text")
    answer_text: str = Field(..., description="The user's answer")
    analysis: str = Field(..., description="Analysis of the answer")
    suggestions: List[str] = Field(default_factory=list, description="Suggestions for improvement")
    concerns: List[str] = Field(default_factory=list, description="Concerns or risks identified")

class InterviewEvaluation(BaseModel):
    evaluations: List[AnswerEvaluation] = Field(default_factory=list, description="Evaluations for each question")
    summary: str = Field(..., description="Overall summary of the interview findings")

class ClarityReport(BaseModel):
    meta: Meta
    idea: Idea
    audience: Audience
    market: Market
    risks: Risks
    execution: Execution
    recommendation: Recommendation
    interview_evaluation: Optional[InterviewEvaluation] = Field(None, description="Evaluation of the user interview")
    sources: List[Source] = Field(default_factory=list, description="List of sources used in the analysis")

class AgentArtifact(BaseModel):
    agent_name: str = Field(..., description="Name of the agent")
    started_at: datetime = Field(..., description="Start timestamp of the agent execution")
    finished_at: datetime = Field(..., description="Finish timestamp of the agent execution")
    input_summary: str = Field(..., description="Summary of the input provided to the agent")
    output_markdown: str = Field(..., description="Raw markdown output from the agent")
    output_json: Optional[Dict[str, Any]] = Field(None, description="Structured JSON output from the agent")
