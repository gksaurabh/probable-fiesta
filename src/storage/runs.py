import os
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path

from src.contracts.clarity_report import ClarityReport, AgentArtifact, Interview

DATA_DIR = Path("data/runs")

def _get_run_dir(run_id: str) -> Path:
    return DATA_DIR / run_id

def _ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def update_run_status(run_id: str, status: str):
    """
    Updates the status of a run.
    """
    run_dir = _get_run_dir(run_id)
    if not run_dir.exists():
        return
    
    run_file = run_dir / "run.json"
    if run_file.exists():
        with open(run_file, "r") as f:
            run_data = json.load(f)
        
        run_data["status"] = status
        run_data["updated_at"] = datetime.utcnow().isoformat()
        
        with open(run_file, "w") as f:
            json.dump(run_data, f, indent=2)

def save_interview(run_id: str, interview: Interview):
    """
    Saves the interview to interview.json.
    """
    run_dir = _get_run_dir(run_id)
    if not run_dir.exists():
        raise ValueError(f"Run {run_id} not found")
    
    with open(run_dir / "interview.json", "w") as f:
        f.write(interview.model_dump_json(indent=2))

def get_interview(run_id: str) -> Optional[Interview]:
    """
    Retrieves the interview for a run.
    """
    run_dir = _get_run_dir(run_id)
    interview_path = run_dir / "interview.json"
    
    if interview_path.exists():
        with open(interview_path, "r") as f:
            return Interview.model_validate_json(f.read())
    return None

def create_run(idea_text: str) -> str:
    """
    Creates a new run directory and run.json.
    Returns the run_id.
    """
    _ensure_data_dir()
    run_id = str(uuid.uuid4())
    run_dir = _get_run_dir(run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "artifacts").mkdir(exist_ok=True)

    run_data = {
        "run_id": run_id,
        "idea_text": idea_text,
        "created_at": datetime.utcnow().isoformat(),
        "status": "STARTED"
    }

    with open(run_dir / "run.json", "w") as f:
        json.dump(run_data, f, indent=2)
    
    # Create empty events file
    (run_dir / "events.jsonl").touch()

    return run_id

def append_event(run_id: str, event: Dict[str, Any]):
    """
    Appends an event to events.jsonl.
    """
    run_dir = _get_run_dir(run_id)
    if not run_dir.exists():
        raise ValueError(f"Run {run_id} not found")
    
    # Add timestamp if not present
    if "timestamp" not in event:
        event["timestamp"] = datetime.utcnow().isoformat()

    # Print to stdout for logging
    print(f"INFO:     Run {run_id} event: {event['type']} {event.get('agent', '')} {event.get('status', '')}")

    with open(run_dir / "events.jsonl", "a") as f:
        f.write(json.dumps(event) + "\n")

def save_artifact(run_id: str, artifact: AgentArtifact):
    """
    Saves an artifact to artifacts/{agent_name}.json.
    """
    run_dir = _get_run_dir(run_id)
    if not run_dir.exists():
        raise ValueError(f"Run {run_id} not found")
    
    artifacts_dir = run_dir / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)
    
    # Sanitize agent name for filename
    filename = f"{artifact.agent_name.lower().replace(' ', '_')}.json"
    
    with open(artifacts_dir / filename, "w") as f:
        f.write(artifact.model_dump_json(indent=2))

def save_report(run_id: str, report: ClarityReport):
    """
    Saves the final report to report.json and updates run status.
    """
    run_dir = _get_run_dir(run_id)
    if not run_dir.exists():
        raise ValueError(f"Run {run_id} not found")
    
    # Save report.json
    with open(run_dir / "report.json", "w") as f:
        f.write(report.model_dump_json(indent=2))
    
    # Update run status
    run_file = run_dir / "run.json"
    if run_file.exists():
        with open(run_file, "r") as f:
            run_data = json.load(f)
        
        run_data["status"] = "COMPLETED"
        run_data["completed_at"] = datetime.utcnow().isoformat()
        
        with open(run_file, "w") as f:
            json.dump(run_data, f, indent=2)

def get_run(run_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves run details, including status, timestamps, and partial outputs (artifacts).
    """
    run_dir = _get_run_dir(run_id)
    if not run_dir.exists():
        return None
    
    # Load run metadata
    run_data = {}
    if (run_dir / "run.json").exists():
        with open(run_dir / "run.json", "r") as f:
            run_data = json.load(f)
            
    # Load artifacts
    artifacts = []
    artifacts_dir = run_dir / "artifacts"
    if artifacts_dir.exists():
        for artifact_file in artifacts_dir.glob("*.json"):
            with open(artifact_file, "r") as f:
                try:
                    artifacts.append(json.load(f))
                except json.JSONDecodeError:
                    pass
    
    run_data["artifacts"] = artifacts
    
    # Load events
    events = []
    events_file = run_dir / "events.jsonl"
    if events_file.exists():
        with open(events_file, "r") as f:
            for line in f:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    run_data["events"] = events

    # Check if report exists
    run_data["has_report"] = (run_dir / "report.json").exists()
    
    # Check if interview exists
    if (run_dir / "interview.json").exists():
        with open(run_dir / "interview.json", "r") as f:
            run_data["interview"] = json.load(f)

    return run_data

def list_runs(limit: int = 50) -> List[Dict[str, Any]]:
    """
    Lists runs, sorted by newest first.
    """
    _ensure_data_dir()
    runs = []
    
    for run_dir in DATA_DIR.iterdir():
        if run_dir.is_dir() and (run_dir / "run.json").exists():
            try:
                with open(run_dir / "run.json", "r") as f:
                    run_data = json.load(f)
                    runs.append(run_data)
            except (json.JSONDecodeError, IOError):
                continue
                
    # Sort by created_at descending
    runs.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    return runs[:limit]
