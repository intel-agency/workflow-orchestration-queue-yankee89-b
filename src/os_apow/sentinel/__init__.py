"""
OS-APOW Sentinel Package

The "Brain" of OS-APOW: polling, task claiming, and lifecycle management.
"""

from src.os_apow.sentinel.orchestrator import Sentinel

__all__ = ["Sentinel"]
