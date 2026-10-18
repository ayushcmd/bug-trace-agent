"""
Test suite for sample_target.auth module.
"""
from sample_target.auth import login

def test_valid_admin_login():
    """Valid credentials should succeed."""
    assert login("admin", "secret123") is True

def test_invalid_password():
    """Wrong password should fail."""
    assert login("admin", "wrongpassword") is False

def test_nonexistent_user():
    """Unknown user should fail."""
    assert login("ghost_user", "somepassword") is False

def test_empty_credentials():
    """Empty credentials should fail."""
    assert login("", "") is False
