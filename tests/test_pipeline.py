import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.agents.pipeline import run_analysis, PlannerAgent, MarketAgent, RiskAgent, ExecutionAgent, JudgeAgent
from src.contracts.clarity_report import Idea, Audience, Market, Risks, Execution, Recommendation, Verdict, Scores, ScoreDetail, InterviewEvaluation, AnswerEvaluation

# Mock Data
MOCK_IDEA_TEXT = "A platform for connecting remote workers with co-working spaces."
MOCK_RUN_ID = "test-run-id"

MOCK_IDEA_OBJ = Idea(
    title="RemoteWorkConnect",
    one_liner="Airbnb for co-working spaces",
    expanded_summary="A platform that allows remote workers to find and book desks.",
    assumptions=["Remote work will continue to grow"]
)

MOCK_MARKET_DICT = {
    "audience": {
        "primary_users": ["Remote Workers", "Digital Nomads"],
        "jobs_to_be_done": ["Find desk", "Book meeting room"],
        "personas": []
    },
    "market": {
        "demand_signals": ["Increasing remote job postings"],
        "competitors": ["WeWork", "Regus"],
        "positioning": "Flexible and affordable"
    }
}

MOCK_RISKS_OBJ = Risks(
    top_risks=["Low supply", "Low demand"],
    mitigations=["Partnerships", "Marketing"]
)

MOCK_EXECUTION_OBJ = Execution(
    mvp_scope=["Search", "Booking"],
    two_week_plan=["Design", "Dev"],
    two_month_plan=["Launch", "Scale"]
)

MOCK_RECOMMENDATION_OBJ = Recommendation(
    verdict=Verdict.PURSUE,
    confidence=0.85,
    scores=Scores(
        market_demand=ScoreDetail(score=8, reasoning="High demand"),
        competitive_advantage=ScoreDetail(score=7, reasoning="Good advantage"),
        technical_feasibility=ScoreDetail(score=9, reasoning="Easy to build"),
        business_viability=ScoreDetail(score=8, reasoning="Profitable")
    ),
    rationale="Strong market demand"
)

MOCK_INTERVIEW_EVALUATION = InterviewEvaluation(
    evaluations=[
        AnswerEvaluation(
            question_id="1",
            question_text="What is your idea?",
            answer_text="A platform...",
            analysis="Good idea",
            suggestions=[],
            concerns=[]
        )
    ],
    summary="Overall good interview"
)

@pytest.fixture
def mock_storage():
    with patch("src.agents.pipeline.append_event") as mock_append, \
         patch("src.agents.pipeline.save_artifact") as mock_save_artifact, \
         patch("src.agents.pipeline.save_report") as mock_save_report, \
         patch("src.agents.pipeline.save_interview") as mock_save_interview, \
         patch("src.agents.pipeline.get_run") as mock_get_run, \
         patch("src.agents.pipeline.get_interview") as mock_get_interview, \
         patch("src.agents.pipeline.update_run_status") as mock_update_run_status:
        yield {
            "append_event": mock_append,
            "save_artifact": mock_save_artifact,
            "save_report": mock_save_report,
            "save_interview": mock_save_interview,
            "get_run": mock_get_run,
            "get_interview": mock_get_interview,
            "update_run_status": mock_update_run_status
        }

@pytest.fixture
def mock_agents():
    with patch("src.agents.pipeline.PlannerAgent") as MockPlanner, \
         patch("src.agents.pipeline.MarketAgent") as MockMarket, \
         patch("src.agents.pipeline.RiskAgent") as MockRisk, \
         patch("src.agents.pipeline.ExecutionAgent") as MockExecution, \
         patch("src.agents.pipeline.JudgeAgent") as MockJudge, \
         patch("src.agents.pipeline.InterviewerAgent") as MockInterviewer, \
         patch("src.agents.pipeline.InterviewEvaluatorAgent") as MockInterviewEvaluator:
        
        # Setup Planner
        planner_instance = MockPlanner.return_value
        planner_instance.run.return_value = MOCK_IDEA_OBJ
        
        # Setup Market
        market_instance = MockMarket.return_value
        market_instance.run.return_value = MOCK_MARKET_DICT
        
        # Setup Risk
        risk_instance = MockRisk.return_value
        risk_instance.run.return_value = MOCK_RISKS_OBJ
        
        # Setup Execution
        execution_instance = MockExecution.return_value
        execution_instance.run.return_value = MOCK_EXECUTION_OBJ
        
        # Setup Judge
        judge_instance = MockJudge.return_value
        judge_instance.run.return_value = MOCK_RECOMMENDATION_OBJ

        # Setup Interviewer
        interviewer_instance = MockInterviewer.return_value
        interviewer_instance.run.return_value = [] # No questions, proceed directly

        # Setup Interview Evaluator
        interview_evaluator_instance = MockInterviewEvaluator.return_value
        interview_evaluator_instance.run.return_value = MOCK_INTERVIEW_EVALUATION
        
        yield {
            "planner": planner_instance,
            "market": market_instance,
            "risk": risk_instance,
            "execution": execution_instance,
            "judge": judge_instance,
            "interviewer": interviewer_instance,
            "interview_evaluator": interview_evaluator_instance
        }

def test_run_analysis_success(mock_storage, mock_agents):
    # Simulate no existing interview, so it runs fresh
    mock_storage["get_interview"].return_value = None

    # Run the pipeline
    report = run_analysis(MOCK_RUN_ID, MOCK_IDEA_TEXT)
    
    # Verify Report
    assert report is not None
    assert report.meta.run_id == MOCK_RUN_ID
    assert report.idea == MOCK_IDEA_OBJ
    assert report.recommendation == MOCK_RECOMMENDATION_OBJ
    
    # Verify Agent Calls
    mock_agents["planner"].run.assert_called_once_with(MOCK_IDEA_TEXT)
    mock_agents["market"].run.assert_called_once_with(MOCK_IDEA_OBJ.expanded_summary)
    mock_agents["risk"].run.assert_called_once()
    mock_agents["execution"].run.assert_called_once()
    mock_agents["judge"].run.assert_called_once()
    
    # Verify Storage Calls
    # 5 agents + 1 final report = 6 artifacts? No, 5 artifacts.
    assert mock_storage["save_artifact"].call_count == 5
    mock_storage["save_report"].assert_called_once()
    
    # Verify Events
    # Start + 5*(Start+Finish) + Complete = 1 + 10 + 1 = 12 events
    assert mock_storage["append_event"].call_count >= 12
    
    # Check specific event types
    calls = mock_storage["append_event"].call_args_list
    assert calls[0][0][1]["type"] == "RUN_STARTED"
    assert calls[-1][0][1]["type"] == "RUN_COMPLETED"

def test_run_analysis_failure(mock_storage, mock_agents):
    # Simulate an error in Planner Agent
    mock_agents["planner"].run.side_effect = Exception("Planner failed")
    
    report = run_analysis(MOCK_RUN_ID, MOCK_IDEA_TEXT)
    
    assert report is None
    
    # Verify Failure Event
    failure_call = mock_storage["append_event"].call_args_list[-1]
    assert failure_call[0][1]["type"] == "RUN_FAILED"
    assert "Planner failed" in failure_call[0][1]["error"]

