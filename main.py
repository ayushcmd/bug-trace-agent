"""
Root main.py entrypoint (re-exports app from app.main for backward compatibility).
"""
import uvicorn
from app.main import app, BugReport
from app.config import settings

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)