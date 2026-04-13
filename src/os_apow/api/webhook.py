"""
OS-APOW Webhook API Router

FastAPI router for GitHub webhook ingestion (The Ear).
Re-exports the webhook endpoint from the notifier service.
"""

from fastapi import APIRouter, Depends, Request

from src.os_apow.models.work_item import TaskType, WorkItem, WorkItemStatus
from src.os_apow.queue.github_queue import GitHubQueue, ITaskQueue

router = APIRouter(prefix="/webhook", tags=["webhook"])


def _get_queue() -> ITaskQueue:
    """Dependency injection for the queue implementation."""
    import os

    return GitHubQueue(token=os.environ.get("GITHUB_TOKEN", ""))


@router.post("/github")
async def handle_github_webhook(
    request: Request,
    queue: ITaskQueue = Depends(_get_queue),
) -> dict[str, str]:
    """Handle incoming GitHub webhook events and create work items."""
    payload = await request.json()
    event_type = request.headers.get("X-GitHub-Event")

    if event_type == "issues" and payload.get("action") == "opened":
        issue = payload["issue"]
        labels = [label["name"] for label in issue.get("labels", [])]

        if "[Application Plan]" in issue["title"] or "agent:plan" in labels:
            work_item = WorkItem(
                id=str(issue["id"]),
                issue_number=issue["number"],
                source_url=issue["html_url"],
                target_repo_slug=payload["repository"]["full_name"],
                task_type=TaskType.PLAN,
                context_body=issue.get("body") or "",
                status=WorkItemStatus.QUEUED,
                node_id=issue["node_id"],
            )
            await queue.add_to_queue(work_item)
            return {"status": "accepted", "item_id": work_item.id}

    return {"status": "ignored", "reason": "No actionable OS-APOW event mapping found"}
