"""
OS-APOW Queue Service (The State)

Service facade for the GitHub-based work queue.
Delegates to the core implementation in queue.github_queue.
"""

import logging

from src.os_apow.models.work_item import WorkItem, WorkItemStatus
from src.os_apow.queue.github_queue import ITaskQueue

logger = logging.getLogger("OS-APOW.QueueService")


class QueueService:
    """Service facade wrapping the GitHub work queue.

    Provides a simplified API for queue operations with structured logging.
    """

    def __init__(self, queue: ITaskQueue):
        self._queue = queue

    async def add_to_queue(self, item: WorkItem) -> bool:
        """Add a work item to the queue."""
        logger.info(f"Adding work item #{item.issue_number} to queue")
        result = await self._queue.add_to_queue(item)
        if result:
            logger.info(f"Successfully queued #{item.issue_number}")
        else:
            logger.warning(f"Failed to queue #{item.issue_number}")
        return result

    async def fetch_queued_tasks(self) -> list[WorkItem]:
        """Fetch all queued work items."""
        tasks = await self._queue.fetch_queued_tasks()
        logger.info(f"Fetched {len(tasks)} queued tasks")
        return tasks

    async def update_status(
        self, item: WorkItem, status: WorkItemStatus, comment: str | None = None
    ) -> None:
        """Update the status of a work item."""
        logger.info(f"Updating #{item.issue_number} to {status.value}")
        await self._queue.update_status(item, status, comment)
