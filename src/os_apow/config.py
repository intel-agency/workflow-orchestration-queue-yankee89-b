"""
OS-APOW Configuration

Centralized configuration management using environment variables
with sensible defaults for MVP.
"""

import os
from dataclasses import dataclass, field


@dataclass
class GitHubConfig:
    """GitHub API configuration."""

    token: str = field(default_factory=lambda: os.getenv("GITHUB_TOKEN", ""))
    org: str = field(default_factory=lambda: os.getenv("GITHUB_ORG", ""))
    repo: str = field(default_factory=lambda: os.getenv("GITHUB_REPO", ""))
    bot_login: str = field(default_factory=lambda: os.getenv("SENTINEL_BOT_LOGIN", ""))


@dataclass
class SentinelConfig:
    """Sentinel orchestrator configuration."""

    poll_interval: int = 60  # seconds between polling cycles
    max_backoff: int = 960  # 16 minutes max backoff on rate limits
    heartbeat_interval: int = 300  # 5 min between heartbeat comments
    subprocess_timeout: int = 5700  # 95 min - safety net for worker subprocess
    shell_bridge_path: str = "./scripts/devcontainer-opencode.sh"
    bot_login: str = field(default_factory=lambda: os.getenv("SENTINEL_BOT_LOGIN", ""))


@dataclass
class NotifierConfig:
    """Work event notifier configuration."""

    webhook_secret: str = field(default_factory=lambda: os.getenv("WEBHOOK_SECRET", ""))
    host: str = "0.0.0.0"
    port: int = 8000


@dataclass
class Config:
    """Main configuration container."""

    github: GitHubConfig = field(default_factory=GitHubConfig)
    sentinel: SentinelConfig = field(default_factory=SentinelConfig)
    notifier: NotifierConfig = field(default_factory=NotifierConfig)
    debug: bool = field(
        default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true"
    )

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        return cls()

    def validate(self) -> list[str]:
        """Validate configuration and return list of missing required values."""
        errors = []

        # GitHub token is always required
        if not self.github.token:
            errors.append("GITHUB_TOKEN is required")

        return errors


def get_config() -> Config:
    """Get the global configuration instance."""
    return Config.from_env()
