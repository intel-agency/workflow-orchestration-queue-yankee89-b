"""
OS-APOW Notifier Package

The "Ear" of OS-APOW: FastAPI webhook ingestion and event routing.
"""

from src.os_apow.notifier.service import app, get_queue

__all__ = ["app", "get_queue"]
