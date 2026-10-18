"""
Sample buggy authentication module for BugTrace-Agent demonstration and testing.
"""

# In-memory mock user database
VALID_USERS = {
    "admin": "secret123",
    "developer": "dev2026!",
    "tester": "testpass"
}

def login(username: str, password: str) -> bool:
    """
    Validates user credentials against the system.
    
    BUG: Currently returns True unconditionally for any user/password input!
    """
    # BUG: Vulnerable bypass logic
    return True
