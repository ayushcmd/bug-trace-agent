"""
Session and State Memory Store for BugTrace-Agent.
Maintains history, execution logs, diffs, and HITL approval states.
"""
import time
from typing import Dict, Any, Optional, List

class SessionMemory:
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    def init_session(self, issue_id: str, description: str) -> Dict[str, Any]:
        """Initializes a new tracking session for an issue."""
        session = {
            "issue_id": issue_id,
            "description": description,
            "status": "running",
            "provider": "unknown",
            "relevant_files": [],
            "proposed_fix": None,
            "test_output": None,
            "logs": [f"Session initialized at {time.strftime('%Y-%m-%d %H:%M:%S')}"],
            "created_at": time.time(),
            "updated_at": time.time(),
        }
        self._store[issue_id] = session
        return session

    def get_session(self, issue_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves session state by issue_id."""
        return self._store.get(issue_id)

    def update_session(self, issue_id: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Updates specific fields in a session."""
        session = self._store.get(issue_id)
        if not session:
            return None
        
        for k, v in kwargs.items():
            if k == "logs" and isinstance(v, str):
                session["logs"].append(v)
            else:
                session[k] = v
        session["updated_at"] = time.time()
        return session

    def list_sessions(self) -> List[Dict[str, Any]]:
        """Returns a summary list of all tracked sessions."""
        return [
            {
                "issue_id": s["issue_id"],
                "description": s["description"],
                "status": s["status"],
                "provider": s.get("provider", "unknown"),
                "created_at": s["created_at"],
                "updated_at": s["updated_at"]
            }
            for s in self._store.values()
        ]

# Global singleton session memory instance
session_memory = SessionMemory()
