# OS-APOW Technology Stack

**Project:** workflow-orchestration-queue (OS-APOW)  
**Last Updated:** 2026-03-20  
**Status:** Planning Phase

---

## Overview

OS-APOW is a headless agentic orchestration platform built on Python 3.12+ with modern async patterns. The technology choices prioritize developer experience, operational reliability, and security.

---

## Core Technologies

### Language & Runtime

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.12+ | Primary language for orchestrator, webhook receiver, and system logic |
| **PowerShell Core (pwsh)** | Latest | Cross-platform shell scripts for auth synchronization and CLI operations |
| **Bash** | Latest | Shell bridge scripts for DevContainer orchestration |

### Web Framework & Server

| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | Latest | High-performance async web framework for webhook receiver |
| **Uvicorn** | Latest | ASGI server for production deployment |
| **Pydantic** | Latest | Data validation, settings management, schema definitions |

### HTTP & API

| Technology | Version | Purpose |
|------------|---------|---------|
| **httpx** | Latest | Async HTTP client for GitHub REST API calls |

### Package Management

| Technology | Version | Purpose |
|------------|---------|---------|
| **uv** | Latest | Rust-based Python package installer and resolver |
| **pyproject.toml** | — | Project configuration and dependency specification |

---

## Containerization & Infrastructure

### Container Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Docker** | Latest | Container runtime for worker isolation |
| **DevContainers** | Latest | Reproducible development environment |
| **Docker Compose** | Latest | Multi-container orchestration |

### DevContainer Features

| Feature | Purpose |
|---------|---------|
| Node.js | JavaScript runtime for MCP server packages |
| Python | Primary development runtime |
| GitHub CLI | Repository operations and authentication |

---

## Agent & LLM Stack

### Agent Runtime

| Technology | Version | Purpose |
|------------|---------|---------|
| **opencode CLI** | 1.2.24 | AI agent runtime for task execution |
| **ZhipuAI GLM** | Latest | Primary LLM model (zai-coding-plan/glm-5) |
| **Kimi (Moonshot)** | Latest | Alternative LLM model |

### MCP Servers

| Server | Purpose |
|--------|---------|
| `@modelcontextprotocol/server-sequential-thinking` | Structured problem-solving |
| `@modelcontextprotocol/server-memory` | Knowledge graph persistence |

---

## Data & State Management

### Queue Implementation

| Technology | Purpose |
|------------|---------|
| **GitHub Issues** | Primary work queue (Markdown-as-Database) |
| **GitHub Labels** | State machine indicators |
| **GitHub Milestones** | Phase tracking |

### Data Models

| Component | Location | Purpose |
|-----------|----------|---------|
| `WorkItem` | `src/models/work_item.py` | Unified task model |
| `TaskType` | `src/models/work_item.py` | Task classification enum |
| `WorkItemStatus` | `src/models/work_item.py` | State machine enum |
| `ITaskQueue` | `src/queue/github_queue.py` | Provider-agnostic queue interface |

---

## Security Stack

### Authentication

| Component | Purpose |
|-----------|---------|
| **GitHub App Installation Token** | API authentication (5,000 req/hr) |
| **HMAC SHA256** | Webhook signature verification |
| **Ephemeral Credentials** | In-memory token injection to workers |

### Credential Protection

| Component | Location | Purpose |
|-----------|----------|---------|
| `scrub_secrets()` | `src/models/work_item.py` | Regex-based credential sanitization |

### Secret Patterns Protected

- GitHub PATs: `ghp_*`, `ghs_*`, `gho_*`, `github_pat_*`
- Bearer tokens
- OpenAI-style keys: `sk-*`
- ZhipuAI keys

---

## Logging & Observability

### Logging Stack

| Technology | Purpose |
|------------|---------|
| **Python logging** | Structured console logging |
| **stdout** | Container-captured logs (`docker logs`) |

### Telemetry

| Component | Purpose |
|-----------|---------|
| **Heartbeat Comments** | 5-minute status updates on GitHub issues |
| **Status Labels** | Real-time state visibility |
| **Issue Comments** | Execution logs and error reports |

---

## Development Tools

### CLI Tools

| Tool | Purpose |
|------|---------|
| **gh** | GitHub CLI for API operations |
| **git** | Version control |
| **opencode** | Agent execution |

### Scripts

| Script | Purpose |
|--------|---------|
| `devcontainer-opencode.sh` | Shell bridge for worker lifecycle |
| `gh-auth.ps1` | GitHub authentication helper |
| `common-auth.ps1` | Shared auth initialization |
| `update-remote-indices.ps1` | Vector index synchronization |

---

## GitHub Integration

### Repository Structure

| Component | Purpose |
|-----------|---------|
| **main** | Production-ready release branch |
| **develop** | Integration and testing branch |

### GitHub Features Used

| Feature | Purpose |
|---------|---------|
| **Issues** | Work queue items |
| **Labels** | State machine states |
| **Milestones** | Phase tracking |
| **Assignees** | Distributed locking |
| **Comments** | Telemetry and logs |
| **Pull Requests** | Code delivery |

---

## Version Constraints Summary

```
python >= 3.12
fastapi >= 0.100.0
uvicorn >= 0.23.0
pydantic >= 2.0.0
httpx >= 0.24.0
uv >= 0.1.0
```

---

## Dependency Management

All dependencies are managed via `pyproject.toml` and locked with `uv.lock` for reproducible builds.

```bash
# Install dependencies
uv sync

# Run services
uv run python src/orchestrator_sentinel.py
uv run uvicorn src.notifier_service:app --host 0.0.0.0 --port 8000
```
