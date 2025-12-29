import json
import traceback
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from src.prompts.agent_prompts import AgentPrompts
from src.contracts.clarity_report import (
    ClarityReport, AgentArtifact, Meta, Idea, Audience, Market, Risks, Execution, Recommendation, Source,
    Interview, Question, InterviewEvaluation
)
from src.storage.runs import (
    create_run, append_event, save_artifact, save_report, get_run, save_interview, get_interview, update_run_status
)

# --- Agent Definitions ---

class InterviewEvaluatorAgent:
    def __init__(self):
        self.agent = Agent(
            name="InterviewEvaluatorAgent",
            model=OpenAIChat(id="gpt-4o-mini", temperature=0.0),
            instructions=AgentPrompts.INTERVIEW_EVALUATOR_AGENT_INSTRUCTIONS,
            output_schema=InterviewEvaluation,
        )

    def run(self, interview: Interview) -> InterviewEvaluation:
        # Format interview for the agent
        interview_text = "Questions and Answers:\n"
        for q in interview.questions:
            ans = interview.answers.get(q.id, "No answer provided")
            interview_text += f"Q: {q.text}\nA: {ans}\n\n"
            
        response = self.agent.run(f"Evaluate this interview:\n{interview_text}")
        if response.content is None:
            raise ValueError("InterviewEvaluatorAgent returned None")
        return response.content

class InterviewerAgent:
    def __init__(self):
        self.agent = Agent(
            name="InterviewerAgent",
            model=OpenAIChat(id="gpt-4o", temperature=0.0),
            instructions=AgentPrompts.INTERVIEWER_AGENT_INSTRUCTIONS,
            # We expect a JSON with "questions" list
        )

    def run(self, idea_text: str) -> List[Dict[str, Any]]:
        response = self.agent.run(f"Analyze this idea and generate questions: {idea_text}")
        content = response.content
        if content is None:
            raise ValueError("InterviewerAgent returned None")
        
        if isinstance(content, str):
            # Clean up markdown code blocks if present
            cleaned_content = content.replace("```json", "").replace("```", "").strip()
            try:
                data = json.loads(cleaned_content)
                return data.get("questions", [])
            except json.JSONDecodeError:
                # Fallback: try to split by newlines if not JSON (legacy fallback, might fail with new format)
                # If JSON fails, we might just return text as questions with no guidance
                return [{"text": line.strip("- ").strip(), "guidance": None} for line in content.split("\n") if "?" in line]
        return []

class PlannerAgent:
    def __init__(self):
        self.agent = Agent(
            name="PlannerAgent",
            model=OpenAIChat(id="gpt-4o", temperature=0.0),
            instructions=AgentPrompts.PLANNER_AGENT_INSTRUCTIONS,
            output_schema=Idea,
        )

    def run(self, idea_text: str) -> Idea:
        response = self.agent.run(f"Analyze this idea: {idea_text}")
        if response.content is None:
            raise ValueError("PlannerAgent returned None")
        return response.content

class MarketAgent:
    def __init__(self):
        self.agent = Agent(
            name="MarketAgent",
            model=OpenAIChat(id="gpt-4o", temperature=0.0),
            instructions=AgentPrompts.MARKET_AGENT_INSTRUCTIONS,
            # We need a combined model for response, or we can parse a dict.
            # For simplicity in this MVP pipeline, let's ask for a dict and parse it into Audience and Market models.
            # Or define a wrapper model. Let's use a dict for flexibility here and validate later.
            # Actually, agno supports Pydantic models. Let's define a wrapper.
        )

    def run(self, idea_context: str) -> Dict[str, Any]:
        # We expect JSON output as defined in instructions.
        response = self.agent.run(f"Analyze market for: {idea_context}")
        # Assuming the agent returns a dict-like structure or we parse the content if it's a string.
        # If response_model is not set, content is a string (or Message).
        # Let's try to parse the JSON from the string if not using response_model.
        # But using response_model is safer.
        # Let's define a temporary Pydantic model for the combined output if needed, 
        # or just rely on the LLM to return valid JSON string and parse it.
        # For "simple, deterministic", let's try to force JSON mode.
        content = response.content
        if content is None:
             raise ValueError("MarketAgent returned None")
        
        if isinstance(content, str):
            # Clean up markdown code blocks if present
            cleaned_content = content.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned_content)
        return content

class RiskAgent:
    def __init__(self):
        self.agent = Agent(
            name="RiskAgent",
            model=OpenAIChat(id="gpt-4o", temperature=0.0),
            instructions=AgentPrompts.RISK_AGENT_INSTRUCTIONS,
            output_schema=Risks,
        )

    def run(self, idea_context: str, market_context: str) -> Risks:
        response = self.agent.run(f"Analyze risks for: {idea_context}\n\nMarket Context: {market_context}")
        if response.content is None:
            raise ValueError("RiskAgent returned None")
        return response.content

class ExecutionAgent:
    def __init__(self):
        self.agent = Agent(
            name="ExecutionAgent",
            model=OpenAIChat(id="gpt-4o", temperature=0.0),
            instructions=AgentPrompts.EXECUTION_AGENT_INSTRUCTIONS,
            output_schema=Execution,
        )

    def run(self, idea_context: str, risks_context: str) -> Execution:
        response = self.agent.run(f"Create execution plan for: {idea_context}\n\nRisks: {risks_context}")
        if response.content is None:
            raise ValueError("ExecutionAgent returned None")
        return response.content

class JudgeAgent:
    def __init__(self):
        self.agent = Agent(
            name="JudgeAgent",
            model=OpenAIChat(id="gpt-4o-mini", temperature=0.0),
            instructions=AgentPrompts.JUDGE_AGENT_INSTRUCTIONS,
            output_schema=Recommendation,
        )

    def run(self, summary_context: str) -> Recommendation:
        response = self.agent.run(f"Final verdict based on: {summary_context}")
        if response.content is None:
            raise ValueError("JudgeAgent returned None")
        return response.content

# --- Pipeline Orchestration ---

def run_analysis(run_id: str, idea_text: str) -> Optional[ClarityReport]:
    """
    Executes the multi-agent pipeline for a given run_id.
    """
    try:
        # 1. Start Run
        append_event(run_id, {"type": "RUN_STARTED", "status": "RUNNING"})
        
        # --- Interviewer Agent ---
        # Check if we already have an interview (resume mode) or need to start one
        existing_interview = get_interview(run_id)
        
        if not existing_interview:
            append_event(run_id, {"type": "AGENT_STARTED", "agent": "InterviewerAgent"})
            interviewer = InterviewerAgent()
            questions_data = interviewer.run(idea_text)
            
            if questions_data:
                # Create Interview object
                questions = []
                for i, q_data in enumerate(questions_data):
                    # Handle both string (legacy) and dict (new) formats just in case
                    if isinstance(q_data, str):
                        questions.append(Question(id=str(i+1), text=q_data, guidance=None))
                    else:
                        questions.append(Question(
                            id=str(i+1), 
                            text=q_data.get("text", ""), 
                            guidance=q_data.get("guidance")
                        ))
                
                interview = Interview(questions=questions, answers={})
                save_interview(run_id, interview)
                
                append_event(run_id, {"type": "AGENT_FINISHED", "agent": "InterviewerAgent"})
                append_event(run_id, {"type": "WAITING_FOR_INPUT", "status": "WAITING_FOR_INPUT"})
                update_run_status(run_id, "WAITING_FOR_INPUT")
                return None # Stop pipeline to wait for user input
            
            # If no questions, proceed directly (shouldn't happen with current prompt but good fallback)
            append_event(run_id, {"type": "AGENT_FINISHED", "agent": "InterviewerAgent"})

        # If we are here, either we have answers or no questions were asked.
        # If we have an interview but no answers, we should stop (unless resuming logic handles this)
        # But run_analysis is called initially. Resume logic will call a different function or this one with a flag?
        # Let's assume resume_analysis calls this function again.
        
        if existing_interview and not existing_interview.answers:
             # This case happens if we crash and restart, or if called incorrectly.
             # But if we are "resuming", we expect answers.
             # Let's just check if status is WAITING_FOR_INPUT.
             # Actually, let's make a separate resume_analysis function to be clear.
             pass

        # --- Planner Agent ---
        append_event(run_id, {"type": "AGENT_STARTED", "agent": "PlannerAgent"})
        planner = PlannerAgent()
        start_time = datetime.now(timezone.utc)
        
        # Enrich idea with interview answers if available
        planner_input = idea_text
        if existing_interview and existing_interview.answers:
            qa_text = "\n\nAdditional Context from Interview:\n"
            for q in existing_interview.questions:
                ans = existing_interview.answers.get(q.id)
                if ans:
                    qa_text += f"Q: {q.text}\nA: {ans}\n"
            planner_input += qa_text

        idea_obj = planner.run(planner_input)
        end_time = datetime.now(timezone.utc)
        
        planner_artifact = AgentArtifact(
            agent_name="PlannerAgent",
            started_at=start_time,
            finished_at=end_time,
            input_summary=idea_text[:200],
            output_markdown=f"**Title:** {idea_obj.title}\n\n**Summary:** {idea_obj.expanded_summary}",
            output_json=idea_obj.model_dump()
        )
        save_artifact(run_id, planner_artifact)
        append_event(run_id, {"type": "AGENT_FINISHED", "agent": "PlannerAgent"})

        # --- Market Agent ---
        append_event(run_id, {"type": "AGENT_STARTED", "agent": "MarketAgent"})
        market_agent = MarketAgent()
        start_time = datetime.now(timezone.utc)
        # Market agent output is a dict with 'audience' and 'market' keys based on prompt
        # We need to handle the raw response since we didn't use a strict response_model class for the combined dict
        # Ideally we should, but for now let's trust the prompt + json mode or parsing
        # To make it robust, let's use the agent without response_model and parse JSON manually or use a generic dict
        # Re-instantiating with response_format={"type": "json_object"} if supported, or just relying on prompt.
        # Let's assume the run method handles it (we implemented it to return dict).
        market_raw = market_agent.run(idea_obj.expanded_summary)
        end_time = datetime.now(timezone.utc)
        
        # Parse into Pydantic models
        audience_obj = Audience(**market_raw.get("audience", {}))
        market_obj = Market(**market_raw.get("market", {}))
        
        market_artifact = AgentArtifact(
            agent_name="MarketAgent",
            started_at=start_time,
            finished_at=end_time,
            input_summary="Expanded Idea Summary",
            output_markdown=f"**Positioning:** {market_obj.positioning}\n\n**Target Audience:** {', '.join(audience_obj.primary_users)}",
            output_json=market_raw
        )
        save_artifact(run_id, market_artifact)
        append_event(run_id, {"type": "AGENT_FINISHED", "agent": "MarketAgent"})

        # --- Risk Agent ---
        append_event(run_id, {"type": "AGENT_STARTED", "agent": "RiskAgent"})
        risk_agent = RiskAgent()
        start_time = datetime.now(timezone.utc)
        risks_obj = risk_agent.run(idea_obj.expanded_summary, market_obj.positioning)
        end_time = datetime.now(timezone.utc)
        
        risk_artifact = AgentArtifact(
            agent_name="RiskAgent",
            started_at=start_time,
            finished_at=end_time,
            input_summary="Idea + Market Positioning",
            output_markdown=f"**Top Risks:**\n" + "\n".join([f"- {r}" for r in risks_obj.top_risks]),
            output_json=risks_obj.model_dump()
        )
        save_artifact(run_id, risk_artifact)
        append_event(run_id, {"type": "AGENT_FINISHED", "agent": "RiskAgent"})

        # --- Execution Agent ---
        append_event(run_id, {"type": "AGENT_STARTED", "agent": "ExecutionAgent"})
        execution_agent = ExecutionAgent()
        start_time = datetime.now(timezone.utc)
        execution_obj = execution_agent.run(idea_obj.expanded_summary, str(risks_obj.top_risks))
        end_time = datetime.now(timezone.utc)
        
        execution_artifact = AgentArtifact(
            agent_name="ExecutionAgent",
            started_at=start_time,
            finished_at=end_time,
            input_summary="Idea + Risks",
            output_markdown=f"**MVP Scope:**\n" + "\n".join([f"- {s}" for s in execution_obj.mvp_scope]),
            output_json=execution_obj.model_dump()
        )
        save_artifact(run_id, execution_artifact)
        append_event(run_id, {"type": "AGENT_FINISHED", "agent": "ExecutionAgent"})

        # --- Judge Agent ---
        append_event(run_id, {"type": "AGENT_STARTED", "agent": "JudgeAgent"})
        judge_agent = JudgeAgent()
        start_time = datetime.now(timezone.utc)
        
        # Compile context for Judge
        summary_context = (
            f"Idea: {idea_obj.expanded_summary}\n"
            f"Market Positioning: {market_obj.positioning}\n"
            f"Top Risks: {risks_obj.top_risks}\n"
            f"MVP Scope: {execution_obj.mvp_scope}"
        )
        
        recommendation_obj = judge_agent.run(summary_context)
        end_time = datetime.now(timezone.utc)
        
        scores_md = ""
        if recommendation_obj.scores:
            scores_md = "\n\n**Scores:**\n"
            scores_md += f"- Market Demand: {recommendation_obj.scores.market_demand.score}/10 ({recommendation_obj.scores.market_demand.reasoning})\n"
            scores_md += f"- Competitive Advantage: {recommendation_obj.scores.competitive_advantage.score}/10 ({recommendation_obj.scores.competitive_advantage.reasoning})\n"
            scores_md += f"- Technical Feasibility: {recommendation_obj.scores.technical_feasibility.score}/10 ({recommendation_obj.scores.technical_feasibility.reasoning})\n"
            scores_md += f"- Business Viability: {recommendation_obj.scores.business_viability.score}/10 ({recommendation_obj.scores.business_viability.reasoning})\n"
            scores_md += f"\n**Confidence:** {recommendation_obj.confidence}"

        judge_artifact = AgentArtifact(
            agent_name="JudgeAgent",
            started_at=start_time,
            finished_at=end_time,
            input_summary="All Agent Outputs",
            output_markdown=f"**Verdict:** {recommendation_obj.verdict}{scores_md}\n\n**Rationale:** {recommendation_obj.rationale}",
            output_json=recommendation_obj.model_dump()
        )
        save_artifact(run_id, judge_artifact)
        append_event(run_id, {"type": "AGENT_FINISHED", "agent": "JudgeAgent"})

        # --- Interview Evaluator Agent ---
        interview_evaluation = None
        if existing_interview and existing_interview.answers:
            append_event(run_id, {"type": "AGENT_STARTED", "agent": "InterviewEvaluatorAgent"})
            evaluator_agent = InterviewEvaluatorAgent()
            start_time = datetime.now(timezone.utc)
            interview_evaluation = evaluator_agent.run(existing_interview)
            end_time = datetime.now(timezone.utc)
            
            evaluator_artifact = AgentArtifact(
                agent_name="InterviewEvaluatorAgent",
                started_at=start_time,
                finished_at=end_time,
                input_summary="Interview Questions & Answers",
                output_markdown=interview_evaluation.summary,
                output_json=interview_evaluation.model_dump()
            )
            save_artifact(run_id, evaluator_artifact)
            append_event(run_id, {"type": "AGENT_FINISHED", "agent": "InterviewEvaluatorAgent"})

        # --- Final Report Assembly ---
        report = ClarityReport(
            meta=Meta(
                run_id=run_id,
                model="gpt-4o",
                version="0.1"
            ),
            idea=idea_obj,
            audience=audience_obj,
            market=market_obj,
            risks=risks_obj,
            execution=execution_obj,
            recommendation=recommendation_obj,
            interview_evaluation=interview_evaluation,
            sources=[] # Sources could be gathered by agents if we added that capability
        )
        
        save_report(run_id, report)
        append_event(run_id, {"type": "RUN_COMPLETED", "status": "COMPLETED"})
        
        return report

    except Exception as e:
        error_msg = str(e)
        traceback.print_exc()
        append_event(run_id, {"type": "RUN_FAILED", "error": error_msg, "status": "FAILED"})
        return None
