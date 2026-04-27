"""
Tests for OS-APOW WorkItem Model
"""

import pytest

from src.os_apow.models.work_item import TaskType, WorkItem, WorkItemStatus, scrub_secrets


class TestTaskType:
    """Tests for TaskType enum."""

    def test_task_types_exist(self):
        """Test all expected task types exist."""
        assert TaskType.PLAN == "PLAN"
        assert TaskType.IMPLEMENT == "IMPLEMENT"
        assert TaskType.BUGFIX == "BUGFIX"

    def test_task_type_from_string(self):
        """Test TaskType can be created from string."""
        assert TaskType("PLAN") == TaskType.PLAN
        assert TaskType("IMPLEMENT") == TaskType.IMPLEMENT


class TestWorkItemStatus:
    """Tests for WorkItemStatus enum."""

    def test_statuses_exist(self):
        """Test all expected statuses exist."""
        assert WorkItemStatus.QUEUED == "agent:queued"
        assert WorkItemStatus.IN_PROGRESS == "agent:in-progress"
        assert WorkItemStatus.RECONCILING == "agent:reconciling"
        assert WorkItemStatus.SUCCESS == "agent:success"
        assert WorkItemStatus.ERROR == "agent:error"
        assert WorkItemStatus.INFRA_FAILURE == "agent:infra-failure"
        assert WorkItemStatus.STALLED_BUDGET == "agent:stalled-budget"


class TestWorkItem:
    """Tests for WorkItem model."""

    def test_create_work_item(self, sample_work_item):
        """Test WorkItem creation with valid data."""
        assert sample_work_item.id == "12345"
        assert sample_work_item.issue_number == 42
        assert sample_work_item.task_type == TaskType.IMPLEMENT
        assert sample_work_item.status == WorkItemStatus.QUEUED

    def test_work_item_required_fields(self):
        """Test WorkItem requires all fields."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            WorkItem()

    def test_work_item_serialization(self, sample_work_item):
        """Test WorkItem can be serialized to dict."""
        data = sample_work_item.model_dump()
        assert data["id"] == "12345"
        assert data["issue_number"] == 42
        assert data["task_type"] == "IMPLEMENT"

    def test_work_item_from_dict(self):
        """Test WorkItem can be created from dict."""
        data = {
            "id": "999",
            "issue_number": 1,
            "source_url": "https://github.com/org/repo/issues/1",
            "context_body": "body",
            "target_repo_slug": "org/repo",
            "task_type": "PLAN",
            "status": "agent:queued",
            "node_id": "node_1",
        }
        item = WorkItem(**data)
        assert item.task_type == TaskType.PLAN


class TestSecretScrubber:
    """Tests for the credential scrubber."""

    def test_scrub_github_pat(self):
        """Test GitHub PAT scrubbing."""
        text = "token: ghp_123456789012345678901234567890123456"
        result = scrub_secrets(text)
        assert "ghp_" not in result
        assert "***REDACTED***" in result

    def test_scrub_bearer_token(self):
        """Test Bearer token scrubbing."""
        text = "Authorization: Bearer abc123def456ghi789jkl012mno345pqr678stu901vwx234yz="
        result = scrub_secrets(text)
        assert "Bearer" not in result or "***REDACTED***" in result

    def test_scrub_openai_key(self):
        """Test OpenAI-style key scrubbing."""
        text = "api-key: sk-123456789012345678901234"
        result = scrub_secrets(text)
        assert "sk-" not in result

    def test_scrub_clean_text_unchanged(self):
        """Test clean text passes through unchanged."""
        text = "This is a normal log message with no secrets."
        result = scrub_secrets(text)
        assert result == text

    def test_custom_replacement(self):
        """Test custom replacement string."""
        text = "ghp_123456789012345678901234567890123456"
        result = scrub_secrets(text, replacement="[HIDDEN]")
        assert "[HIDDEN]" in result
