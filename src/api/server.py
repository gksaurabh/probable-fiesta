import json
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, RedirectResponse
from pydantic import BaseModel, Field

load_dotenv()

from src.storage.runs import create_run, get_run, list_runs, _get_run_dir, save_interview, get_interview, update_run_status
from src.agents.pipeline import run_analysis
from src.contracts.clarity_report import ClarityReport
from src.renderers.report_to_markdown import render_report_md

app = FastAPI(
    title="ClarityAI API",
    description="API for running AI-powered market analysis on startup ideas.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IdeaInput(BaseModel):
    idea: str = Field(..., examples=["A platform for connecting remote workers with co-working spaces."], description="The startup idea to analyze.")

class RunResponse(BaseModel):
    run_id: str = Field(..., examples=["123e4567-e89b-12d3-a456-426614174000"], description="The unique identifier for the analysis run.")

class FeedbackInput(BaseModel):
    answers: Dict[str, str] = Field(..., description="Map of question IDs to answers.")

@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "Welcome to ClarityAI API",
        "docs": "http://127.0.0.1:8000/docs",
        "redoc": "http://127.0.0.1:8000/redoc"
    }

@app.post("/analysis/run", response_model=RunResponse, tags=["Analysis"], summary="Start a new analysis")
async def start_analysis(input_data: IdeaInput, background_tasks: BackgroundTasks):
    """
    Starts the analysis pipeline for a given idea.
    
    - **idea**: A short description of the startup idea.
    """
    run_id = create_run(input_data.idea)
    
    # Run analysis in background
    background_tasks.add_task(run_analysis, run_id, input_data.idea)
    
    return {"run_id": run_id}

@app.get("/analysis/{run_id}", tags=["Analysis"], summary="Get analysis status")
async def get_analysis_status(run_id: str):
    """
    Retrieves the status, artifacts, and report for a specific run.
    """
    run_data = get_run(run_id)
    if not run_data:
        raise HTTPException(status_code=404, detail="Run not found")
    
    # If report exists, load it
    if run_data.get("has_report"):
        run_dir = _get_run_dir(run_id)
        report_path = run_dir / "report.json"
        if report_path.exists():
            with open(report_path, "r") as f:
                try:
                    run_data["report"] = json.load(f)
                except json.JSONDecodeError:
                    run_data["report"] = None
    
    return run_data

@app.get("/analysis", tags=["Analysis"], summary="List recent analyses")
async def list_analyses():
    """
    Lists recent runs.
    """
    return list_runs()

@app.get("/analysis/{run_id}/export.md", response_class=PlainTextResponse, tags=["Export"], summary="Export analysis as Markdown")
async def export_analysis_markdown(run_id: str):
    """
    Exports the final report as Markdown.
    """
    run_data = get_run(run_id)
    if not run_data:
        raise HTTPException(status_code=404, detail="Run not found")
    
    if not run_data.get("has_report"):
        raise HTTPException(status_code=400, detail="Report not yet generated")
    
    run_dir = _get_run_dir(run_id)
    report_path = run_dir / "report.json"
    
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Report file missing")
        
    try:
        with open(report_path, "r") as f:
            report_dict = json.load(f)
            report = ClarityReport(**report_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading report: {str(e)}")
    
    return render_report_md(report)

@app.post("/analysis/{run_id}/feedback", tags=["Analysis"], summary="Submit answers to interview questions")
async def submit_feedback(run_id: str, input_data: FeedbackInput, background_tasks: BackgroundTasks):
    """
    Submits answers to the interview questions and resumes the analysis.
    """
    run_data = get_run(run_id)
    if not run_data:
        raise HTTPException(status_code=404, detail="Run not found")
    
    interview = get_interview(run_id)
    if not interview:
        raise HTTPException(status_code=400, detail="No interview found for this run")
    
    # Update answers
    interview.answers = input_data.answers
    save_interview(run_id, interview)
    
    # Update status and resume
    update_run_status(run_id, "RUNNING")
    
    # Retrieve original idea
    idea_text = run_data.get("idea_text")
    if not idea_text:
         raise HTTPException(status_code=500, detail="Could not retrieve original idea")

    # Resume analysis in background
    background_tasks.add_task(run_analysis, run_id, idea_text)
    
    return {"status": "resumed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
