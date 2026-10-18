"""
Unit and Integration Tests for BugTrace-Agent FastAPI endpoints.
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Verify health endpoint returns 200 and online status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["service"] == "BugTrace-Agent"
    assert "active_provider" in data

def test_start_run_validation_error():
    """Missing fields should trigger validation error."""
    response = client.post("/start_run", json={})
    assert response.status_code == 422

def test_end_to_end_agent_workflow():
    """
    Tests the complete autonomous loop:
    1. Ingest bug report (/start_run)
    2. Check status (/status/{id})
    3. Verify runs listing (/runs)
    4. Approve fix (/approve/{id})
    """
    issue_id = "TEST-BUG-999"
    payload = {
        "issue_id": issue_id,
        "description": "Login function in auth.py always returns true regardless of credentials"
    }

    # 1. Trigger agent run
    res_start = client.post("/start_run", json=payload)
    assert res_start.status_code == 200
    data_start = res_start.json()
    assert data_start["success"] is True
    assert data_start["issue_id"] == issue_id
    assert "Awaiting HITL approval" in data_start["message"]

    # 2. Check status endpoint
    res_status = client.get(f"/status/{issue_id}")
    assert res_status.status_code == 200
    data_status = res_status.json()
    assert data_status["issue_id"] == issue_id
    assert data_status["status"] == "awaiting_approval"
    assert data_status["proposed_fix"] is not None
    assert len(data_status["logs"]) > 0

    # 3. Check runs list
    res_runs = client.get("/runs")
    assert res_runs.status_code == 200
    data_runs = res_runs.json()
    assert data_runs["count"] >= 1
    issue_ids = [r["issue_id"] for r in data_runs["runs"]]
    assert issue_id in issue_ids

    # 4. Human-in-the-Loop Approval
    res_approve = client.post(f"/approve/{issue_id}")
    assert res_approve.status_code == 200
    data_approve = res_approve.json()
    assert data_approve["success"] is True
    assert "pushed" in data_approve["message"].lower()

    # 5. Verify status updated to completed
    res_final_status = client.get(f"/status/{issue_id}")
    assert res_final_status.json()["status"] == "completed"

def test_approve_nonexistent_issue():
    """Approving an unknown issue should return 404."""
    response = client.post("/approve/UNKNOWN-ISSUE-404")
    assert response.status_code == 404
