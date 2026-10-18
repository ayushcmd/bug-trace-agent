"""
Root tools.py (re-exports from app.tools for backward compatibility).
"""
from app.tools.rag import retrieve_relevant_files, rag_tool_declaration
from app.tools.runner import run_tests, test_tool_declaration

# Backward compatibility with vertexai declarations if needed
try:
    from vertexai.generative_models import FunctionDeclaration
    rag_tool = FunctionDeclaration(**rag_tool_declaration)
    test_tool = FunctionDeclaration(**test_tool_declaration)
except Exception:
    rag_tool = rag_tool_declaration
    test_tool = test_tool_declaration

__all__ = ["retrieve_relevant_files", "run_tests", "rag_tool", "test_tool"]
