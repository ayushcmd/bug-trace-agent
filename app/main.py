"""
FastAPI application entrypoint for BugTrace-Agent.
Provides REST API endpoints for bug ingestion, status monitoring, run history, and HITL approval.
"""
import logging
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field

from app.config import settings
from app.engine.memory import session_memory
from app.engine.agent import start_agent_run, approve_and_push

# Configure application logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# --- Request / Response Models ---
class BugReport(BaseModel):
    issue_id: str = Field(..., examples=["BUG-101"], description="Unique identifier for the bug ticket")
    description: str = Field(..., examples=["Login function always returns true regardless of credentials"], description="Detailed bug report")

class RunResponse(BaseModel):
    success: bool
    issue_id: str
    message: str
    provider: Optional[str] = None

class StatusResponse(BaseModel):
    issue_id: str
    description: str
    status: str
    provider: str
    relevant_files: List[str]
    proposed_fix: Optional[str]
    test_output: Optional[str]
    logs: List[str]
    created_at: float
    updated_at: float

# --- Routes ---
@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint providing runtime state and active provider info."""
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "active_provider": settings.get_active_provider(),
        "environment": settings.ENVIRONMENT
    }

@app.post("/start_run", response_model=RunResponse, tags=["Agent Workflow"])
def start_run(report: BugReport):
    """
    Initiates the autonomous bug fixing workflow:
    1. RAG codebase retrieval
    2. AI reasoning / fix formulation
    3. Pytest automated test loop
    4. HITL approval staging
    """
    issue_id = report.issue_id.strip()
    description = report.description.strip()
    
    if not issue_id:
        raise HTTPException(status_code=400, detail="issue_id cannot be empty")
    if not description:
        raise HTTPException(status_code=400, detail="description cannot be empty")
        
    logger.info(f"Received start_run request for issue: {issue_id}")
    try:
        status_message = start_agent_run(issue_id, description)
        session = session_memory.get_session(issue_id)
        provider = session.get("provider") if session else settings.get_active_provider()
        
        return RunResponse(
            success=True,
            issue_id=issue_id,
            message=status_message,
            provider=provider
        )
    except Exception as e:
        logger.error(f"Error executing agent run for {issue_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal agent error: {str(e)}")

@app.get("/status/{issue_id}", response_model=StatusResponse, tags=["Inspection & Tracking"])
def get_issue_status(issue_id: str = Path(..., description="Issue identifier")):
    """Retrieves real-time execution status, logs, code diff, and test output for a bug fix."""
    session = session_memory.get_session(issue_id.strip())
    if not session:
        raise HTTPException(status_code=404, detail=f"Issue '{issue_id}' not found in active memory.")
    return session

@app.get("/runs", tags=["Inspection & Tracking"])
def list_runs():
    """Lists all active and completed bug-fixing runs."""
    return {
        "count": len(session_memory.list_sessions()),
        "runs": session_memory.list_sessions()
    }

@app.post("/approve/{issue_id}", tags=["HITL Approval"])
def approve(issue_id: str = Path(..., description="Issue identifier to approve")):
    """
    Human-in-the-Loop approval gate.
    Verifies that the agent's proposed fix passed all tests and triggers PR merge.
    """
    clean_id = issue_id.strip()
    if not clean_id:
        raise HTTPException(status_code=400, detail="issue_id cannot be empty")
        
    logger.info(f"Processing HITL approval for: {clean_id}")
    status_message = approve_and_push(clean_id)
    
    if "not found" in status_message.lower() or "not ready" in status_message.lower():
        raise HTTPException(status_code=404, detail=status_message)
        
    return {
        "success": True,
        "issue_id": clean_id,
        "message": status_message
    }
