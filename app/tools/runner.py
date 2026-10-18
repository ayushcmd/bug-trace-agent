"""
Execution Sandbox / Test Runner Tool: Executes automated pytest suite to verify fixes.
"""
import sys
import subprocess
from pathlib import Path
from typing import Dict, Any

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def run_tests(test_target: str = "sample_target/test_auth.py") -> str:
    """
    Executes pytest against the specified test file or test suite.
    
    Returns:
        Formatted summary indicating PASS or FAIL with stdout output.
    """
    print(f"[Test Runner] Running pytest on: {test_target}")
    
    target_path = BASE_DIR / test_target
    if not target_path.exists():
        # Fallback to sample_target/test_auth.py if target doesn't exist
        target_path = BASE_DIR / "sample_target" / "test_auth.py"
        
    cmd = [sys.executable, "-m", "pytest", str(target_path), "-v", "--tb=short"]
    
    try:
        result = subprocess.run(
            cmd,
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return f"SUCCESS: All automated tests passed!\n\n{result.stdout}"
        else:
            return f"FAILURE: Tests failed with returncode {result.returncode}.\n\n{result.stdout}\n{result.stderr}"
            
    except subprocess.TimeoutExpired:
        return "ERROR: Test execution timed out after 30 seconds."
    except Exception as e:
        return f"ERROR: Failed to execute pytest: {str(e)}"

test_tool_declaration = {
    "name": "run_tests",
    "description": "Runs automated pytest unit tests to verify whether the bug fix works as expected.",
    "parameters": {
        "type": "object",
        "properties": {
            "test_target": {
                "type": "string",
                "description": "Path to test file to execute. Defaults to sample_target/test_auth.py"
            }
        }
    }
}
