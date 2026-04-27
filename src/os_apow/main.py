"""
OS-APOW Main Entry Point

Provides entry points for running different components:
- Sentinel orchestrator
- Work event notifier
- Combined mode (for development)
"""

import asyncio
import logging
import sys

from src.os_apow.config import get_config

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("OS-APOW")


def run_notifier():
    """Run the FastAPI webhook notifier service."""
    import uvicorn

    from src.os_apow.notifier.service import app

    config = get_config()

    # Validate configuration
    errors = config.validate()
    if not config.notifier.webhook_secret:
        errors.append("WEBHOOK_SECRET is required for notifier")

    if errors:
        for error in errors:
            logger.error(f"Configuration error: {error}")
        sys.exit(1)

    logger.info(
        f"Starting OS-APOW Notifier on {config.notifier.host}:{config.notifier.port}"
    )
    uvicorn.run(
        app,
        host=config.notifier.host,
        port=config.notifier.port,
        reload=config.debug,
    )


async def run_sentinel():
    """Run the sentinel orchestrator."""
    from src.os_apow.config import get_config
    from src.os_apow.queue.github_queue import GitHubQueue
    from src.os_apow.sentinel.orchestrator import Sentinel

    config = get_config()

    # Validate configuration
    errors = config.validate()
    required = ["GITHUB_ORG", "GITHUB_REPO"]
    for var in required:
        if not getattr(config.github, var.lower(), None):
            errors.append(f"{var} is required for sentinel")

    if errors:
        for error in errors:
            logger.error(f"Configuration error: {error}")
        sys.exit(1)

    if not config.github.bot_login:
        logger.warning(
            "SENTINEL_BOT_LOGIN is not set — assign-then-verify locking is disabled. "
            "Set it to the GitHub login of the bot account for concurrency safety."
        )

    gh_queue = GitHubQueue(
        token=config.github.token,
        org=config.github.org,
        repo=config.github.repo,
    )
    sentinel = Sentinel(gh_queue, config.sentinel)

    try:
        await sentinel.run_forever()
    finally:
        await gh_queue.close()
        logger.info("Sentinel shut down.")


def main():
    """Main entry point with component selection."""
    import argparse

    parser = argparse.ArgumentParser(
        description="OS-APOW Agentic Orchestration Platform"
    )
    parser.add_argument(
        "component",
        choices=["sentinel", "notifier"],
        help="Component to run",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )

    args = parser.parse_args()

    if args.debug:
        logging.getLogger("OS-APOW").setLevel(logging.DEBUG)

    if args.component == "sentinel":
        try:
            asyncio.run(run_sentinel())
        except KeyboardInterrupt:
            logger.info("Sentinel shutting down gracefully.")
    elif args.component == "notifier":
        run_notifier()


if __name__ == "__main__":
    main()
