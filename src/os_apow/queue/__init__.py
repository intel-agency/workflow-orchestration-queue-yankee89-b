"""
OS-APOW Queue Package

Abstract interface and concrete implementations for work queue backends.
"""

from src.os_apow.queue.github_queue import GitHubQueue, ITaskQueue

__all__ = [
    "ITaskQueue",
    "GitHubQueue",
]
