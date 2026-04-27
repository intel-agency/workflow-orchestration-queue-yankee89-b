"""
Tests for OS-APOW Queue Service
"""

from unittest.mock import AsyncMock

import pytest


class TestQueueService:
    """Tests for the Queue service facade."""

    def test_queue_service_imports(self):
        """Test that the QueueService can be imported."""
        from src.os_apow.services.queue import QueueService

        assert QueueService is not None

    def test_queue_service_creation(self):
        """Test creating a QueueService instance."""
        from src.os_apow.queue.github_queue import GitHubQueue
        from src.os_apow.services.queue import QueueService

        queue = GitHubQueue(token="test_token", org="test_org", repo="test_repo")
        service = QueueService(queue)
        assert service is not None

    @pytest.mark.asyncio
    async def test_queue_service_add_to_queue(self, sample_work_item):
        """Test adding a work item through the service."""
        from src.os_apow.services.queue import QueueService

        mock_queue = AsyncMock()
        mock_queue.add_to_queue.return_value = True

        service = QueueService(mock_queue)
        result = await service.add_to_queue(sample_work_item)
        assert result is True
        mock_queue.add_to_queue.assert_called_once_with(sample_work_item)
