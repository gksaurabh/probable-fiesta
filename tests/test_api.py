import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
import json

# Import the app
from src.api.server import app

client = TestClient(app)

# Mock data
MOCK_RUN_ID = "test-run-id"
MOCK_IDEA = "A test idea"

@pytest.fixture
def mock_storage():
    with patch("src.api.server.create_run") as mock_create, \
         patch("src.api.server.get_run") as mock_get, \
         patch("src.api.server.list_runs") as mock_list, \
         patch("src.api.server._get_run_dir") as mock_dir, \
         patch("src.api.server.run_analysis") as mock_run_analysis:
        yield {
            "create": mock_create,
            "get": mock_get,
            "list": mock_list,
            "dir": mock_dir,
            "run_analysis": mock_run_analysis
        }

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to ClarityAI API",
        "docs": "http://127.0.0.1:8000/docs",
        "redoc": "http://127.0.0.1:8000/redoc"
    }

def test_start_analysis(mock_storage):
    mock_storage["create"].return_value = MOCK_RUN_ID
    
    response = client.post("/analysis/run", json={"idea": MOCK_IDEA})
    
    assert response.status_code == 200
    assert response.json() == {"run_id": MOCK_RUN_ID}
    mock_storage["create"].assert_called_once_with(MOCK_IDEA)

def test_get_analysis_status_found(mock_storage):
    mock_data = {"run_id": MOCK_RUN_ID, "status": "completed", "has_report": False}
    mock_storage["get"].return_value = mock_data
    
    response = client.get(f"/analysis/{MOCK_RUN_ID}")
    
    assert response.status_code == 200
    assert response.json() == mock_data
    mock_storage["get"].assert_called_once_with(MOCK_RUN_ID)

def test_get_analysis_status_not_found(mock_storage):
    mock_storage["get"].return_value = None
    
    response = client.get("/analysis/non-existent")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Run not found"

def test_list_analyses(mock_storage):
    mock_list = [{"run_id": "1"}, {"run_id": "2"}]
    mock_storage["list"].return_value = mock_list
    
    response = client.get("/analysis")
    
    assert response.status_code == 200
    assert response.json() == mock_list

def test_export_analysis_markdown(mock_storage):
    # Mock run data
    mock_storage["get"].return_value = {"run_id": MOCK_RUN_ID, "has_report": True}
    
    # Mock report file content
    mock_report = {
        "meta": {
            "run_id": MOCK_RUN_ID,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "model": "gpt-4",
            "version": "0.1"
        },
        "idea": {
            "title": "Test Idea",
            "one_liner": "A test one liner",
            "expanded_summary": "Expanded summary",
            "assumptions": ["Assumption 1"]
        },
        "audience": {
            "primary_users": ["User 1"],
            "jobs_to_be_done": ["Job 1"],
            "personas": []
        },
        "market": {
            "demand_signals": ["Signal 1"],
            "competitors": ["Comp 1"],
            "positioning": "Positioning"
        },
        "risks": {
            "top_risks": ["Risk 1"],
            "mitigations": ["Mitigation 1"]
        },
        "execution": {
            "mvp_scope": ["Feature 1"],
            "two_week_plan": ["Task 1"],
            "two_month_plan": ["Goal 1"]
        },
        "recommendation": {
            "verdict": "PURSUE",
            "confidence": 0.9,
            "rationale": "Good idea"
        },
        "sources": []
    }
    
    # Mock file operations
    with patch("builtins.open", new_callable=MagicMock) as mock_open:
        # Setup mock file handle
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Setup json.load to return our mock report
        with patch("json.load", return_value=mock_report):
            # We also need to mock path.exists()
            mock_path = MagicMock()
            mock_path.exists.return_value = True
            mock_storage["dir"].return_value = MagicMock()
            mock_storage["dir"].return_value.__truediv__.return_value = mock_path
            
            response = client.get(f"/analysis/{MOCK_RUN_ID}/export.md")
            
            assert response.status_code == 200
            assert "# Test Idea" in response.text
            assert "Verdict: 🟢 PURSUE" in response.text
