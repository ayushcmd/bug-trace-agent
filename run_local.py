#!/usr/bin/env python3
"""
Local development server launcher for BugTrace-Agent.
"""
import sys
import uvicorn
from app.config import settings

def main():
    print("=" * 60)
    print(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f"Active Provider: {settings.get_active_provider().upper()}")
    print(f"Environment:     {settings.ENVIRONMENT}")
    print(f"Listening on:    http://{settings.HOST}:{settings.PORT}")
    print(f"Swagger Docs:    http://localhost:{settings.PORT}/docs")
    print("=" * 60 + "\n")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=False
    )

if __name__ == "__main__":
    main()
