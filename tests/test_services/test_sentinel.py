"""
Tests for OS-APOW Sentinel Service
"""

from src.os_apow.config import SentinelConfig


class TestSentinelService:
    """Tests for the Sentinel service facade."""

    def test_sentinel_service_imports(self):
        """Test that the SentinelService can be imported."""
        from src.os_apow.services.sentinel import SentinelService

        assert SentinelService is not None

    def test_sentinel_service_creation(self):
        """Test creating a SentinelService instance."""
        from src.os_apow.queue.github_queue import GitHubQueue
        from src.os_apow.services.sentinel import SentinelService

        queue = GitHubQueue(token="test_token", org="test_org", repo="test_repo")
        service = SentinelService(queue)
        assert service.sentinel_id.startswith("sentinel-")

    def test_sentinel_config_defaults(self):
        """Test sentinel configuration defaults."""
        config = SentinelConfig()
        assert config.poll_interval == 60
        assert config.max_backoff == 960
        assert config.heartbeat_interval == 300
        assert config.subprocess_timeout == 5700
