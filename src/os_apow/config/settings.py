"""
OS-APOW Settings Management

Pydantic-based settings class that reads configuration from environment variables.
Provides type-safe configuration with validation and defaults.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """OS-APOW application settings.

    Reads configuration from environment variables with type validation
    and sensible defaults for local development.
    """

    # Required settings
    github_token: str = ""
    github_repository: str = ""

    # Optional settings
    webhook_secret: str = ""

    # Operational defaults
    poll_interval_seconds: int = 30
    log_level: str = "INFO"

    # Derived settings
    github_org: str = ""
    github_repo: str = ""

    model_config = {
        "env_prefix": "",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore",
    }

    def model_post_init(self, __context: object) -> None:
        """Parse GITHUB_REPOSITORY into org/repo components."""
        if self.github_repository and "/" in self.github_repository:
            parts = self.github_repository.split("/", 1)
            self.github_org = parts[0]
            self.github_repo = parts[1]
