"""
RAG Tool: Searches repository codebase for files relevant to a reported bug.
"""
import os
from pathlib import Path
from typing import Dict, Any

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def retrieve_relevant_files(issue_description: str) -> Dict[str, Any]:
    """
    Simulates semantic & keyword search across the codebase.
    Locates relevant source files matching the issue description.
    """
    print(f"[RAG Tool] Searching codebase for issue: {issue_description}")
    
    # Check sample_target directory first
    sample_auth = BASE_DIR / "sample_target" / "auth.py"
    desc_lower = issue_description.lower()
    
    if ("login" in desc_lower or "auth" in desc_lower or "credential" in desc_lower) and sample_auth.exists():
        with open(sample_auth, "r", encoding="utf-8") as f:
            content = f.read()
        return {
            "file": "sample_target/auth.py",
            "content": content,
            "status": "found"
        }
    
    # Fallback default simulated file
    return {
        "file": "sample_target/auth.py",
        "content": (
            "def login(username, password):\n"
            "    # BUG: Returns True regardless of credentials\n"
            "    return True\n"
        ),
        "status": "mock_fallback"
    }

rag_tool_declaration = {
    "name": "retrieve_relevant_files",
    "description": "Finds relevant repository files and their contents based on the bug report.",
    "parameters": {
        "type": "object",
        "properties": {
            "issue_description": {
                "type": "string",
                "description": "Description of the bug to search relevant code for."
            }
        },
        "required": ["issue_description"]
    }
}
