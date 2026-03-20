# OS-APOW

**Open Source Agentic Process Orchestration Workflow**

A headless agentic orchestration platform that transforms GitHub Issues into executable workflows.

## Overview

OS-APOW implements a four-pillar architecture for autonomous code execution:

| Pillar | Component | Purpose |
|--------|-----------|---------|
| **The Ear** | Work Event Notifier | FastAPI webhook ingestion |
| **The State** | Work Queue | GitHub Issues as state machine |
| **The Brain** | Sentinel Orchestrator | Polling, task claiming, lifecycle |
| **The Hands** | Opencode Worker | DevContainer-based code execution |

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- Docker (for worker execution)
- GitHub Personal Access Token

### Installation

```bash
# Clone the repository
git clone https://github.com/intel-agency/workflow-orchestration-queue-yankee89-b.git
cd workflow-orchestration-queue-yankee89-b

# Install dependencies
uv sync

# Copy environment template
cp .env.example .env
# Edit .env with your values
```

### Running Components

```bash
# Run the notifier (webhook receiver)
uv run os-apow notifier

# Run the sentinel (orchestrator)
uv run os-apow sentinel

# Or use the module directly
uv run python -m src.os_apow.main notifier
```

### Docker

```bash
# Build the image
docker build -f docker/Dockerfile -t os-apow .

# Run with docker-compose
docker compose -f docker/docker-compose.yml --profile notifier up
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_TOKEN` | Yes | GitHub Personal Access Token |
| `GITHUB_ORG` | Sentinel | GitHub organization name |
| `GITHUB_REPO` | Sentinel | GitHub repository name |
| `WEBHOOK_SECRET` | Notifier | GitHub webhook secret |
| `SENTINEL_BOT_LOGIN` | Optional | Bot account for distributed locking |
| `DEBUG` | Optional | Enable debug logging |

## Architecture

### Work Item Lifecycle

```
┌─────────┐    ┌─────────────┐    ┌──────────┐    ┌─────────┐
│ Queued  │───▶│ In-Progress │───▶│ Success  │    │  Error  │
└─────────┘    └─────────────┘    └──────────┘    └─────────┘
     │                │
     │                ▼
     │         ┌──────────────┐
     │         │ Infra-Failure│
     │         └──────────────┘
     │
     ▼
agent:queued ──▶ agent:in-progress ──▶ agent:success / agent:error
```

### Components

#### Notifier (The Ear)

FastAPI webhook receiver that:
- Validates GitHub webhook signatures
- Maps events to work item types
- Adds items to the work queue

#### Sentinel (The Brain)

Long-running orchestrator that:
- Polls for queued work items
- Claims tasks using assign-then-verify locking
- Manages worker lifecycle
- Posts heartbeat updates

#### Worker (The Hands)

DevContainer-based execution that:
- Runs opencode CLI for agent tasks
- Executes workflows based on task type
- Reports results back to GitHub

## Development

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/os_apow

# Run specific test file
uv run pytest tests/test_placeholder.py -v
```

### Code Quality

```bash
# Lint with ruff
uv run ruff check src/ tests/

# Format
uv run ruff format src/ tests/

# Type check
uv run mypy src/
```

### Project Structure

```
├── src/os_apow/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── config.py            # Configuration
│   ├── models/
│   │   └── work_item.py     # Data models
│   ├── queue/
│   │   └── github_queue.py  # GitHub queue implementation
│   ├── sentinel/
│   │   └── orchestrator.py  # Sentinel orchestrator
│   ├── notifier/
│   │   └── service.py       # FastAPI webhook service
│   └── worker/
│       └── __init__.py      # Worker placeholder
├── tests/
│   ├── conftest.py
│   └── test_placeholder.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/
│   ├── README.md
│   ├── architecture/
│   └── api/
├── pyproject.toml
└── .env.example
```

## Documentation

- [Architecture Documentation](docs/architecture/)
- [API Documentation](docs/api/)
- [ADR-001: GitHub Issues as Work Queue](docs/architecture/001-github-issues-as-queue.md)

## License

MIT License - see [LICENSE](LICENSE) for details.
