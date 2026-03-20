"""
OS-APOW: Open Source Agentic Process Orchestration Workflow

A headless agentic orchestration platform implementing four pillars:
- The Ear (Work Event Notifier): FastAPI webhook ingestion
- The State (Work Queue): GitHub Issues as state machine
- The Brain (Sentinel Orchestrator): Polling, task claiming, lifecycle
- The Hands (Opencode Worker): DevContainer-based code execution
"""

__version__ = "0.1.0"
__author__ = "OS-APOW Team"

from src.os_apow.models.work_item import TaskType, WorkItem, WorkItemStatus
from src.os_apow.queue.github_queue import GitHubQueue, ITaskQueue

__all__ = [
    "WorkItem",
    "TaskType",
    "WorkItemStatus",
    "GitHubQueue",
    "ITaskQueue",
]
