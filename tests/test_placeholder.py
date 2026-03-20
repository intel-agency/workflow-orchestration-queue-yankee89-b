"""
Placeholder Test

Basic tests to verify the project structure and imports work correctly.
"""

import pytest


class TestProjectStructure:
    """Tests to verify project structure is correctly set up."""

    def test_import_models(self):
        """Test that models can be imported."""
        from src.os_apow.models.work_item import TaskType, WorkItemStatus

        assert TaskType.PLAN == "PLAN"
        assert TaskType.IMPLEMENT == "IMPLEMENT"
        assert TaskType.BUGFIX == "BUGFIX"

        assert WorkItemStatus.QUEUED == "agent:queued"
        assert WorkItemStatus.IN_PROGRESS == "agent:in-progress"

    def test_import_config(self):
        """Test that config can be imported."""
        from src.os_apow.config import Config

        config = Config()
        assert config.sentinel.poll_interval == 60
        assert config.notifier.port == 8000

    def test_work_item_model(self):
        """Test that WorkItem model works correctly."""
        from src.os_apow.models.work_item import TaskType, WorkItem, WorkItemStatus

        item = WorkItem(
            id="12345",
            issue_number=42,
            source_url="https://github.com/org/repo/issues/42",
            context_body="Test body",
            target_repo_slug="org/repo",
            task_type=TaskType.IMPLEMENT,
            status=WorkItemStatus.QUEUED,
            node_id="node_123",
        )

        assert item.id == "12345"
        assert item.issue_number == 42
        assert item.task_type == TaskType.IMPLEMENT

    def test_secret_scrubber(self):
        """Test that secret scrubber works correctly."""
        from src.os_apow.models.work_item import scrub_secrets

        # Token must be 36+ chars after ghp_ to match the pattern
        text_with_secret = "Here is a token: ghp_123456789012345678901234567890123456"
        scrubbed = scrub_secrets(text_with_secret)

        assert "ghp_" not in scrubbed
        assert "***REDACTED***" in scrubbed


class TestConfig:
    """Tests for configuration management."""

    def test_default_config(self):
        """Test default configuration values."""
        from src.os_apow.config import Config

        config = Config()

        assert config.sentinel.poll_interval == 60
        assert config.sentinel.max_backoff == 960
        assert config.sentinel.heartbeat_interval == 300
        assert config.sentinel.subprocess_timeout == 5700

    def test_config_validation(self):
        """Test configuration validation."""
        from src.os_apow.config import Config, GitHubConfig

        # Test with explicit empty token
        config = Config(github=GitHubConfig(token=""))
        errors = config.validate()

        # GITHUB_TOKEN should be required
        assert "GITHUB_TOKEN is required" in errors


class TestQueueInterface:
    """Tests for the queue interface."""

    @pytest.mark.asyncio
    async def test_queue_interface_exists(self):
        """Test that ITaskQueue interface can be imported."""
        from src.os_apow.queue.github_queue import ITaskQueue

        # Verify it's an abstract class
        assert hasattr(ITaskQueue, "add_to_queue")
        assert hasattr(ITaskQueue, "fetch_queued_tasks")
        assert hasattr(ITaskQueue, "update_status")
