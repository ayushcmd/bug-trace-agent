"""
Centralized Configuration for BugTrace-Agent.
Loads environment variables from .env with fallback defaults.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
load_dotenv(dotenv_path=BASE_DIR / ".env")

class Settings:
    PROJECT_NAME: str = "BugTrace-Agent"
    VERSION: str = "2.0.0"
    DESCRIPTION: str = "Autonomous bug detection, RAG retrieval, automated testing, and Human-in-the-Loop approval"
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8080))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # AI Credentials
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "")
    GCP_LOCATION: str = os.getenv("GCP_LOCATION", "us-central1")
    
    # Operational Modes: "gemini_api", "vertex_ai", or "demo"
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "false").lower() in ("true", "1", "yes")

    @classmethod
    def get_active_provider(cls) -> str:
        """Determines the active AI provider based on configured credentials."""
        if cls.DEMO_MODE:
            return "demo"
        if cls.GEMINI_API_KEY:
            return "gemini_api"
        if cls.GCP_PROJECT_ID and os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            return "vertex_ai"
        # Auto-fallback to demo mode if no cloud credentials exist, ensuring the app runs out-of-the-box
        return "demo"

settings = Settings()
