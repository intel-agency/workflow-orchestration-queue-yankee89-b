"""
OS-APOW Health Check API Router

Health check and root endpoints for the OS-APOW API.
"""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "online", "system": "OS-APOW"}


@router.get("/")
def root() -> dict[str, str]:
    """Root endpoint with API info."""
    return {
        "name": "OS-APOW",
        "version": "0.1.0",
        "description": "Open Source Agentic Process Orchestration Workflow",
        "docs": "/docs",
    }
