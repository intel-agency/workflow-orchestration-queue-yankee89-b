"""
OS-APOW Sentinel Service (The Brain)

Service facade for the Sentinel Orchestrator.
Delegates to the core implementation in sentinel.orchestrator.
"""

import logging

from src.os_apow.config import SentinelConfig
from src.os_apow.models.work_item import WorkItem
from src.os_apow.queue.github_queue import GitHubQueue
from src.os_apow.sentinel.orchestrator import Sentinel

logger = logging.getLogger("OS-APOW.SentinelService")


class SentinelService:
    """Service facade wrapping the Sentinel Orchestrator.

    Provides a simplified API for starting and managing the sentinel
    orchestrator lifecycle.
    """

    def __init__(self, queue: GitHubQueue, config: SentinelConfig | None = None):
        self._sentinel = Sentinel(queue, config)

    async def run_forever(self) -> None:
        """Start the sentinel polling loop (runs until shutdown)."""
        await self._sentinel.run_forever()

    async def process_task(self, item: WorkItem) -> None:
        """Process a single work item through the execution lifecycle."""
        await self._sentinel.process_task(item)

    @property
    def sentinel_id(self) -> str:
        """Return the unique sentinel identifier."""
        return self._sentinel.sentinel_id
