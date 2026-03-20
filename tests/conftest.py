"""
Pytest Configuration and Fixtures

Provides shared fixtures for testing OS-APOW components.
"""

from unittest.mock import AsyncMock

import pytest


@pytest.fixture
def mock_env(monkeypatch):
    """Fixture to set environment variables for testing."""
    monkeypatch.setenv("GITHUB_TOKEN", "test_token")
    monkeypatch.setenv("GITHUB_ORG", "test_org")
    monkeypatch.setenv("GITHUB_REPO", "test_repo")
    monkeypatch.setenv("WEBHOOK_SECRET", "test_secret")
    monkeypatch.setenv("SENTINEL_BOT_LOGIN", "")


@pytest.fixture
def mock_httpx_client():
    """Fixture providing a mocked httpx AsyncClient."""
    client = AsyncMock()
    client.aclose = AsyncMock()
    return client


@pytest.fixture
def sample_work_item():
    """Fixture providing a sample WorkItem for testing."""
    from src.os_apow.models.work_item import TaskType, WorkItem, WorkItemStatus

    return WorkItem(
        id="12345",
        issue_number=42,
        source_url="https://github.com/test_org/test_repo/issues/42",
        context_body="Test issue body",
        target_repo_slug="test_org/test_repo",
        task_type=TaskType.IMPLEMENT,
        status=WorkItemStatus.QUEUED,
        node_id="test_node_id",
    )


@pytest.fixture
def sample_github_issue():
    """Fixture providing a sample GitHub issue response."""
    return {
        "id": 12345,
        "number": 42,
        "html_url": "https://github.com/test_org/test_repo/issues/42",
        "body": "Test issue body",
        "title": "Test Issue",
        "node_id": "test_node_id",
        "labels": [
            {"name": "agent:queued"},
        ],
        "state": "open",
    }
