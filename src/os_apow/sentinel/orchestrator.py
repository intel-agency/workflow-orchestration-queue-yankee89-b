"""
OS-APOW Sentinel Orchestrator

Implementation of Phase 1: Story 2 & 3.

This script acts as the 'Brain' of the OS-APOW system. It:
1. Polls a GitHub repo for issues labeled 'agent:queued'.
2. Claims the task using assign-then-verify distributed locking.
3. Manages the worker lifecycle via shell bridge scripts.
4. Posts heartbeat comments during long-running tasks.
5. Reports progress and results back to GitHub.
"""

import asyncio
import logging
import random
import signal
import subprocess
import uuid

import httpx

from src.os_apow.config import SentinelConfig
from src.os_apow.models.work_item import TaskType, WorkItem, WorkItemStatus
from src.os_apow.queue.github_queue import GitHubQueue

logger = logging.getLogger("OS-APOW-Sentinel")


class Sentinel:
    """The Brain of OS-APOW - orchestrates task execution lifecycle."""

    def __init__(self, queue: GitHubQueue, config: SentinelConfig | None = None):
        self.queue = queue
        self.config = config or SentinelConfig()
        self._current_backoff = self.config.poll_interval
        self._shutdown_requested = False
        self.sentinel_id = f"sentinel-{uuid.uuid4().hex[:8]}"

        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)

    def _handle_signal(self, signum, frame):
        """Set shutdown flag on SIGTERM/SIGINT so the current task can finish."""
        sig_name = signal.Signals(signum).name
        logger.info(f"Received {sig_name} — will shut down after current task finishes")
        self._shutdown_requested = True

    async def run_shell_command(
        self, args: list[str], timeout: int | None = None
    ) -> subprocess.CompletedProcess:
        """Invokes the local shell bridge (devcontainer-opencode.sh).

        Args:
            args: Command and arguments.
            timeout: Maximum seconds to wait. None = no limit.
        """
        try:
            logger.info(f"Executing Bridge: {' '.join(args)}")
            process = await asyncio.create_subprocess_exec(
                *args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout,
                )
            except TimeoutError:
                logger.warning(f"Shell command timed out after {timeout}s — killing")
                process.kill()
                stdout, stderr = await process.communicate()
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=-1,
                    stdout=stdout.decode().strip() if stdout else "",
                    stderr=f"TIMEOUT after {timeout}s\n"
                    + (stderr.decode().strip() if stderr else ""),
                )

            return subprocess.CompletedProcess(
                args=args,
                returncode=process.returncode or 0,
                stdout=stdout.decode().strip() if stdout else "",
                stderr=stderr.decode().strip() if stderr else "",
            )
        except Exception as e:
            logger.error(f"Critical shell execution error: {str(e)}")
            raise

    # --- Heartbeat coroutine (R-1) ---

    async def _heartbeat_loop(self, item: WorkItem, start_time: float):
        """Post periodic heartbeat comments while a task is running."""
        while True:
            await asyncio.sleep(self.config.heartbeat_interval)
            elapsed = int(asyncio.get_event_loop().time() - start_time)
            await self.queue.post_heartbeat(item, self.sentinel_id, elapsed)

    async def process_task(self, item: WorkItem):
        """Process a single work item through the execution lifecycle."""
        logger.info(f"Processing Task #{item.issue_number}...")
        start_time = asyncio.get_event_loop().time()

        # Launch heartbeat as a background task (R-1)
        heartbeat_task = asyncio.create_task(self._heartbeat_loop(item, start_time))

        try:
            # Step 1: Initialize Infrastructure
            res_up = await self.run_shell_command(
                [self.config.shell_bridge_path, "up"], timeout=300
            )
            if res_up.returncode != 0:
                err = f"❌ **Infrastructure Failure** during `up` stage:\n```\n{res_up.stderr}\n```"
                await self.queue.update_status(item, WorkItemStatus.INFRA_FAILURE, err)
                return

            # Step 2: Start Opencode Server
            res_start = await self.run_shell_command(
                [self.config.shell_bridge_path, "start"], timeout=120
            )
            if res_start.returncode != 0:
                err = f"❌ **Infrastructure Failure** starting `opencode-server`:\n```\n{res_start.stderr}\n```"
                await self.queue.update_status(item, WorkItemStatus.INFRA_FAILURE, err)
                return

            # Step 3: Trigger Agent Workflow
            workflow_map = {
                TaskType.PLAN: "create-app-plan.md",
                TaskType.IMPLEMENT: "perform-task.md",
                TaskType.BUGFIX: "recover-from-error.md",
            }
            workflow = workflow_map.get(item.task_type, "perform-task.md")
            instruction = f"Execute workflow {workflow} for context: {item.source_url}"

            # Primary bridge call with subprocess timeout safety net (R-8)
            res_prompt = await self.run_shell_command(
                [self.config.shell_bridge_path, "prompt", instruction],
                timeout=self.config.subprocess_timeout,
            )

            # Step 4: Handle Completion
            if res_prompt.returncode == 0:
                success_msg = (
                    f"✅ **Workflow Complete**\n"
                    f"Sentinel successfully executed `{workflow}`. "
                    f"Please review Pull Requests."
                )
                await self.queue.update_status(
                    item, WorkItemStatus.SUCCESS, success_msg
                )
            else:
                log_tail = (
                    res_prompt.stderr[-1500:]
                    if res_prompt.stderr
                    else "No error output captured."
                )
                fail_msg = f"❌ **Execution Error** during `{workflow}`:\n```\n...{log_tail}\n```"
                await self.queue.update_status(item, WorkItemStatus.ERROR, fail_msg)

        except Exception as e:
            logger.exception(f"Internal Sentinel Error on Task #{item.issue_number}")
            await self.queue.update_status(
                item,
                WorkItemStatus.INFRA_FAILURE,
                f"🚨 Sentinel encountered an unhandled exception: {str(e)}",
            )
        finally:
            heartbeat_task.cancel()
            try:
                await heartbeat_task
            except asyncio.CancelledError:
                pass

            # Environment reset between tasks — stop container but keep for fast restart
            logger.info("Resetting environment (stop)")
            await self.run_shell_command(
                [self.config.shell_bridge_path, "stop"], timeout=60
            )

    async def run_forever(self):
        """Main polling loop - runs until shutdown is requested."""
        logger.info(
            f"Sentinel {self.sentinel_id} entering polling loop (interval: {self.config.poll_interval}s)"
        )

        while not self._shutdown_requested:
            try:
                tasks = await self.queue.fetch_queued_tasks()
                if tasks:
                    logger.info(f"Found {len(tasks)} queued task(s).")
                    for task in tasks:
                        if self._shutdown_requested:
                            break
                        if await self.queue.claim_task(
                            task, self.sentinel_id, self.config.bot_login
                        ):
                            await self.process_task(task)
                            break

                # Reset backoff on successful poll (I-3)
                self._current_backoff = self.config.poll_interval

            except httpx.HTTPStatusError as exc:
                status = exc.response.status_code
                if status in (403, 429):
                    # Jittered exponential backoff (I-3)
                    jitter = random.uniform(0, self._current_backoff * 0.1)
                    wait = min(self._current_backoff + jitter, self.config.max_backoff)
                    logger.warning(f"Rate limited ({status}) — backing off {wait:.0f}s")
                    self._current_backoff = min(
                        self._current_backoff * 2, self.config.max_backoff
                    )
                    await asyncio.sleep(wait)
                    continue
                else:
                    logger.error(f"GitHub API error: {exc}")
            except Exception as e:
                logger.error(f"Polling cycle error: {str(e)}")

            await asyncio.sleep(self._current_backoff)

        logger.info("Shutdown flag set — exiting polling loop")
