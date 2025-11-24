"""
CODITECT REST API

FastAPI-based REST API for programmatic command execution.

Provides:
- REST endpoints for command execution
- JWT authentication and API key management
- Rate limiting and quota enforcement
- WebSocket streaming for real-time results
- Python SDK for easy integration

Example:
    >>> from api import create_app
    >>> app = create_app()
    >>> # Run with: uvicorn api.main:app --reload
"""

from .main import create_app, app

__all__ = ["create_app", "app"]

__version__ = "1.0.0"
