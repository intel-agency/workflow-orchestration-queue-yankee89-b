"""
OS-APOW Worker Service (The Hands)

Service facade for the Opencode worker bridge.
Manages DevContainer-based code execution.
"""

import logging
import subprocess

logger = logging.getLogger("OS-APOW.WorkerService")


class WorkerService:
    """Service facade for the Opencode worker.

    Provides a simplified API for managing worker lifecycle:
    - Infrastructure setup (container up)
    - Opencode server start/stop
    - Workflow prompt execution
    """

    def __init__(self, shell_bridge_path: str = "./scripts/devcontainer-opencode.sh"):
        self.shell_bridge_path = shell_bridge_path

    def execute_command(
        self, args: list[str], timeout: int | None = None
    ) -> subprocess.CompletedProcess[str]:
        """Execute a command through the shell bridge.

        Args:
            args: Command and arguments to execute.
            timeout: Maximum seconds to wait. None = no limit.

        Returns:
            CompletedProcess with stdout, stderr, and returncode.
        """
        import subprocess

        cmd = [self.shell_bridge_path, *args]
        logger.info(f"Executing: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            logger.info(f"Command completed with returncode {result.returncode}")
            return result
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out after {timeout}s")
            raise
        except Exception as e:
            logger.error(f"Command execution error: {e}")
            raise
