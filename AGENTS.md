# AGENTS.md

Project instructions for coding agents working on **OS-APOW**.

## Project Overview

**OS-APOW** (Open Source Agentic Process Orchestration Workflow) is a headless agentic orchestration platform that transforms GitHub Issues into executable workflows. Written in Python 3.12+ with FastAPI, it uses GitHub Issues as a work queue and executes tasks via DevContainers.

### Four Pillars Architecture

| Pillar     | Component             | Purpose                                        |
|------------|-----------------------|------------------------------------------------|
| **Ear**    | Notifier              | FastAPI webhook ingestion, HMAC validation     |
| **State**  | Queue                 | GitHub Issues as state machine (labels)        |
| **Brain**  | Sentinel Orchestrator | Polling, task claiming, lifecycle management   |
| **Hands**  | Worker                | DevContainer-based code execution via opencode |

### Tech Stack

- **Language:** Python 3.12+
- **Framework:** FastAPI + Uvicorn
- **HTTP Client:** httpx (async)
- **Validation:** Pydantic v2 + pydantic-settings
- **Package Manager:** uv
- **Testing:** pytest + pytest-asyncio + pytest-cov
- **Linting:** ruff
- **Type Checking:** mypy (strict)
- **Containers:** Docker + Docker Compose (profile-based)

## Setup Commands

```bash
# Install dependencies (includes dev tools)
uv sync --extra dev

# Install production only
uv sync

# Run the notifier (webhook receiver)
uv run os-apow notifier

# Run the sentinel (orchestrator)
uv run os-apow sentinel

# Run via module
uv run python -m src.os_apow.main notifier
uv run python -m src.os_apow.main sentinel

# Build Docker image
docker build -f docker/Dockerfile -t os-apow .

# Run with docker-compose
docker compose -f docker/docker-compose.yml --profile notifier up
```

## Project Structure

```
src/os_apow/
  __init__.py                # Package root with re-exports
  main.py                    # CLI entry point (argparse: sentinel/notifier)
  config.py                  # Dataclass-based configuration
  api/                       # FastAPI routers
    __init__.py
    health.py                # Health check endpoints
    webhook.py               # Webhook ingestion router
  config/                    # Pydantic settings
    __init__.py
    settings.py              # BaseSettings (env-based config)
  models/
    __init__.py
    work_item.py             # WorkItem, TaskType, WorkItemStatus, scrub_secrets()
  notifier/
    __init__.py
    service.py               # FastAPI webhook receiver app
  queue/
    __init__.py
    github_queue.py          # ITaskQueue ABC + GitHubQueue implementation
  sentinel/
    __init__.py
    orchestrator.py          # Sentinel polling loop + task lifecycle
  services/                  # Service facades
    __init__.py
    sentinel.py              # Sentinel service facade
    queue.py                 # Queue service facade
    worker.py                # Worker service facade
  worker/
    __init__.py              # Worker placeholder
tests/
  conftest.py                # Shared fixtures
  test_placeholder.py        # Basic import smoke tests
  test_api/
    test_health.py           # Health endpoint tests
    test_webhook.py          # Webhook endpoint tests
  test_models/
    test_work_item.py        # WorkItem model tests
  test_services/
    test_sentinel.py         # Sentinel service tests
    test_queue.py            # Queue service tests
    test_worker.py           # Worker service tests
  unit/                      # Unit tests (expanding)
  integration/               # Integration tests (expanding)
docs/
  adr/                       # Architecture Decision Records
  architecture/
    001-github-issues-as-queue.md
  api/
docker/
  Dockerfile                 # Multi-stage production build
  docker-compose.yml         # Profile-based compose (notifier/sentinel)
```

## Code Style

- **Python 3.12+** with full type annotations required
- **Line length:** 100 characters (enforced by ruff formatter)
- **Import sorting:** isort via ruff (first-party: `src.os_apow`)
- **Linting rules (ruff):** E, W, F, I, B, C4, UP, ARG, SIM
  - E501 ignored (handled by formatter)
  - B008 ignored (FastAPI dependency defaults)
  - ARG001 ignored (FastAPI dependency arguments)
- **Type checking:** mypy strict mode with `pydantic.mypy` plugin
  - `disallow_untyped_defs = true` (relaxed in `tests/`)
- **Formatting:** `uv run ruff format src/ tests/`
- **No secrets/tokens** hardcoded anywhere; all credential output passes through `scrub_secrets()`

## Testing Instructions

```bash
# Run all tests with coverage
uv run pytest

# Run specific test file
uv run pytest tests/test_models/test_work_item.py -v

# Run with verbose output
uv run pytest -v

# Run only unit tests
uv run pytest tests/unit/ tests/test_models/ tests/test_api/ tests/test_services/

# Run only integration tests
uv run pytest tests/integration/ -m integration

# Skip slow tests
uv run pytest -m "not slow"
```

### Test Configuration (pyproject.toml)

- **Runner:** pytest 8.0+ with `pytest-asyncio` (`asyncio_mode = "auto"`)
- **Coverage:** branch coverage on `src/os_apow`, reported with missing lines
- **Markers:** `slow`, `integration`
- **Fixtures:** shared fixtures in `tests/conftest.py`
- **Current status:** 35 tests passing

## Architecture Notes

### Work Item Lifecycle

```
agent:queued ──▶ agent:in-progress ──▶ agent:success / agent:error / agent:infra-failure
```

Labels on GitHub Issues drive the state machine. The Sentinel polls for `agent:queued` issues and transitions them through the lifecycle.

### Distributed Locking (Assign-Then-Verify)

Multiple Sentinel instances can run safely:
1. Assign `SENTINEL_BOT_LOGIN` to the issue via GitHub API
2. Re-fetch issue to verify assignment stuck
3. Only then update labels and proceed
4. If verification fails, another sentinel won the race — abort gracefully

### Provider-Agnostic Queue Interface

All queue interactions go through `ITaskQueue` ABC (`src/os_apow/queue/github_queue.py`). The current implementation is `GitHubQueue`, but the interface supports swapping to Linear, Jira, or SQL-backed queues without changing the Sentinel.

### Secret Scrubbing

All output posted to GitHub passes through `scrub_secrets()` in `src/os_apow/models/work_item.py`. Strips: `ghp_*`, `ghs_*`, `gho_*`, `github_pat_*`, Bearer tokens, `sk-*`, ZhipuAI keys.

### Heartbeat Pattern

Long-running tasks post heartbeat comments every 5 minutes (configurable via `HEARTBEAT_INTERVAL`) to keep observers informed.

### Shell-Bridge Execution

The Sentinel dispatches to workers exclusively via shell scripts (`devcontainer-opencode.sh`), keeping the Python logic layer separate from the Docker infrastructure layer.

## Environment Variables

| Variable             | Required | Component   | Purpose                          |
|----------------------|----------|-------------|----------------------------------|
| `GITHUB_TOKEN`       | Yes      | All         | GitHub API authentication        |
| `GITHUB_ORG`         | Sentinel | Sentinel    | Target organization              |
| `GITHUB_REPO`        | Sentinel | Sentinel    | Target repository                |
| `WEBHOOK_SECRET`     | Notifier | Notifier    | HMAC webhook signature           |
| `SENTINEL_BOT_LOGIN` | Optional | Sentinel    | Bot account for distributed lock |
| `DEBUG`              | Optional | All         | Enable debug logging             |

Copy `.env.example` to `.env` and fill in values.

## PR and Commit Guidelines

- **Conventional commits:** `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`, `ci:`
- **PR format:** Include summary of changes, testing performed, and any remaining risks
- **Keep changes minimal and targeted** — one concern per PR
- **All tests must pass** before merge (`uv run pytest`)
- **Lint must be clean** before merge (`uv run ruff check src/ tests/`)
- **Type check must pass** before merge (`uv run mypy src/`)

## Common Pitfalls

- **Dev dependencies not installed:** Use `uv sync --extra dev` (not just `uv sync`) to get pytest, ruff, mypy
- **Environment variables missing:** Copy `.env.example` to `.env` and set `GITHUB_TOKEN` at minimum
- **Docker not running:** Worker execution requires Docker; sentinel and notifier can run without it for testing
- **Import path:** The package is `src.os_apow` (not `os_apow` directly); use `uv run` which handles the path
- **Test async:** All async tests use `pytest-asyncio` with `auto` mode — no need for `@pytest.mark.asyncio`
- **Coverage exclusions:** `__main__.py`, `pragma: no cover`, and `TYPE_CHECKING` blocks are excluded from coverage
- **plan_docs/ directory:** Contains external-generated documents; exclude from linting
