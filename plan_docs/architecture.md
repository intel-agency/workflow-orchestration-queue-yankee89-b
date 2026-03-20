# OS-APOW Architecture

**Project:** workflow-orchestration-queue (OS-APOW)  
**Last Updated:** 2026-03-20  
**Status:** Planning Phase

---

## Executive Summary

OS-APOW transforms "Interactive AI Coding" into "Headless Agentic Orchestration." Instead of requiring a human to manually trigger and guide AI coding sessions, this system uses a persistent background service that autonomously detects, claims, and executes tasks from GitHub Issues.

**Key Innovation:** Standard project management artifacts (GitHub Issues) become "Execution Orders" that are fulfilled without human intervention.

---

## System Architecture: Four Pillars

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           OS-APOW SYSTEM ARCHITECTURE                        │
└─────────────────────────────────────────────────────────────────────────────┘

     ┌──────────────┐
     │   GitHub     │
     │   Events     │
     └──────┬───────┘
            │ Webhook
            ▼
┌───────────────────────┐
│   THE EAR             │  FastAPI Webhook Receiver
│   Work Event Notifier │  • HMAC signature validation
│                       │  • Event parsing & triage
│   notifier_service.py │  • Queue initialization
└───────────┬───────────┘
            │ WorkItem
            ▼
┌───────────────────────┐
│   THE STATE           │  GitHub Issues as Database
│   Work Queue          │  • agent:queued
│                       │  • agent:in-progress
│   Labels & Issues     │  • agent:success / agent:error
└───────────┬───────────┘
            │ Polling
            ▼
┌───────────────────────┐
│   THE BRAIN           │  Async Python Service
│   Sentinel Orchestrator│  • 60s polling loop
│                       │  • Assign-then-verify locking
│   orchestrator_       │  • Heartbeat posting
│   sentinel.py         │  • Shell bridge dispatch
└───────────┬───────────┘
            │ Shell Commands
            ▼
┌───────────────────────┐
│   THE HANDS           │  DevContainer Environment
│   Opencode Worker     │  • LLM-driven code generation
│                       │  • Test execution
│   devcontainer-       │  • PR creation
│   opencode.sh         │
└───────────────────────┘
```

---

## Component Details

### 1. The Ear (Work Event Notifier)

**File:** `src/notifier_service.py`

**Technology:** FastAPI, Pydantic, HMAC

**Responsibilities:**
- Secure webhook endpoint at `/webhooks/github`
- Cryptographic signature verification (X-Hub-Signature-256)
- Event parsing and WorkItem manifest generation
- Automatic label application (`agent:queued`)

**Security Model:**
```
Incoming Request → Verify HMAC → Parse Payload → Create WorkItem → Add to Queue
                        ↓
                   401 Unauthorized (if invalid)
```

---

### 2. The State (Work Queue)

**Implementation:** GitHub Issues + Labels

**Philosophy:** "Markdown as a Database"

**State Machine:**

```
                    ┌─────────────┐
                    │ agent:queued│
                    └──────┬──────┘
                           │ Sentinel claims
                           ▼
                 ┌──────────────────┐
                 │agent:in-progress │◄───── Heartbeat every 5 min
                 └────────┬─────────┘
                          │
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
    ┌───────────┐  ┌───────────┐  ┌─────────────────┐
    │agent:     │  │agent:     │  │agent:infra-     │
    │success    │  │error      │  │failure          │
    └───────────┘  └───────────┘  └─────────────────┘
```

**Concurrency Control:** GitHub Assignees as distributed lock
- Assign-then-verify pattern prevents race conditions
- Multiple Sentinel instances can run safely

---

### 3. The Brain (Sentinel Orchestrator)

**File:** `src/orchestrator_sentinel.py`

**Technology:** Python async, httpx, signal handling

**Core Loop:**
```python
while not shutdown_requested:
    tasks = fetch_queued_tasks()       # GitHub API
    for task in tasks:
        if claim_task(task):           # Assign-then-verify
            process_task(task)         # Shell bridge
            break
    sleep(POLL_INTERVAL)
```

**Key Features:**
- **Polling-First Resiliency:** Recovers state on restart
- **Jittered Exponential Backoff:** Handles rate limits (403/429)
- **Heartbeat Coroutine:** Posts status every 5 minutes
- **Graceful Shutdown:** SIGTERM/SIGINT handling
- **Connection Pooling:** Single httpx.AsyncClient instance

**Task Processing Flow:**
```
1. devcontainer-opencode.sh up      → Initialize infrastructure
2. devcontainer-opencode.sh start   → Start opencode server
3. devcontainer-opencode.sh prompt  → Execute agent workflow
4. devcontainer-opencode.sh stop    → Reset environment
```

---

### 4. The Hands (Opencode Worker)

**Entry Point:** `scripts/devcontainer-opencode.sh`

**Environment:** Docker DevContainer with:
- .NET SDK 10 (for future expansion)
- Node.js 24 LTS
- Python 3.12+
- Bun, uv
- opencode CLI
- gh CLI

**Workflow Execution:**
```
Prompt → opencode run → LLM reasoning → Code generation → Tests → PR
```

**Resource Constraints:**
- CPU: 2 cores
- Memory: 4GB RAM
- Network: Isolated bridge network

---

## Key Architectural Decisions (ADRs)

### ADR 07: Shell-Bridge Execution

**Decision:** Orchestrator interacts with worker exclusively via `devcontainer-opencode.sh`

**Rationale:**
- Guarantees environment parity with human developers
- Avoids "Configuration Drift"
- Shell scripts handle complex Docker logic
- Python layer stays focused on logic/state

**Consequence:** Clear separation of Logic Layer (Python) and Infra Layer (Shell)

---

### ADR 08: Polling-First Resiliency

**Decision:** Polling is primary discovery; webhooks are optimization

**Rationale:**
- Webhooks are "fire and forget" — events lost if server down
- Polling enables "State Reconciliation" on every restart
- Self-healing against server downtime and network partitions

**Consequence:** System resilient to outages; webhooks add speed but not necessity

---

### ADR 09: Provider-Agnostic Interface

**Decision:** All queue interactions via `ITaskQueue` interface

**Rationale:**
- Phase 1 is GitHub, but architecture supports swapping
- Linear, Jira, or SQL queues can replace GitHub without Orchestrator changes

**Interface Methods:**
```python
class ITaskQueue(ABC):
    async def add_to_queue(item: WorkItem) -> bool
    async def fetch_queued_tasks() -> List[WorkItem]
    async def update_status(item, status, comment)
```

---

## Data Flow: Happy Path

```
1. User opens Issue with [Application Plan] title
           │
           ▼
2. GitHub sends webhook to Notifier
           │
           ▼
3. Notifier validates signature, creates WorkItem
           │
           ▼
4. Notifier applies agent:queued label
           │
           ▼
5. Sentinel polls, discovers queued issue
           │
           ▼
6. Sentinel claims via assign-then-verify
           │
           ▼
7. Sentinel runs devcontainer-opencode.sh up/start/prompt
           │
           ▼
8. Worker executes workflow, creates PR
           │
           ▼
9. Sentinel labels agent:success, posts completion comment
```

---

## Security Architecture

### Network Isolation

```
┌─────────────────────────────────────────────┐
│                 Host Server                  │
│  ┌────────────────────────────────────────┐ │
│  │         Sentinel Orchestrator          │ │
│  │            (Python async)              │ │
│  └───────────────────┬────────────────────┘ │
│                      │ Shell bridge          │
│  ┌───────────────────▼────────────────────┐ │
│  │        Isolated Docker Network          │ │
│  │  ┌────────────────────────────────────┐ │ │
│  │  │      Worker DevContainer           │ │ │
│  │  │   • No host network access         │ │ │
│  │  │   • No peer container access       │ │ │
│  │  │   • Internet access for packages   │ │ │
│  │  └────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

### Credential Flow

```
Sentinel generates token → Injects as env var → Worker uses → Destroyed on exit
                                │
                                └─ Never written to disk
```

### Credential Scrubbing

All output posted to GitHub passes through `scrub_secrets()`:
- GitHub PATs (ghp_*, ghs_*, gho_*, github_pat_*)
- Bearer tokens
- API keys (sk-*, ZhipuAI keys)

---

## Project Structure

```
workflow-orchestration-queue/
├── pyproject.toml               # uv dependencies and metadata
├── uv.lock                      # Deterministic lockfile
├── src/
│   ├── notifier_service.py      # FastAPI webhook receiver
│   ├── orchestrator_sentinel.py # Background polling service
│   ├── models/
│   │   ├── work_item.py         # Unified WorkItem, TaskType, scrub_secrets()
│   │   └── github_events.py     # Webhook payload schemas
│   └── queue/
│       └── github_queue.py      # ITaskQueue + GitHubQueue implementation
├── scripts/
│   ├── devcontainer-opencode.sh # Shell bridge for worker lifecycle
│   ├── gh-auth.ps1              # GitHub auth helper
│   └── update-remote-indices.ps1
├── local_ai_instruction_modules/ # Markdown workflow prompts
│   ├── create-app-plan.md
│   ├── perform-task.md
│   └── analyze-bug.md
└── docs/                        # Architecture and user documentation
```

---

## Self-Bootstrapping Lifecycle

```
Stage 0: Manual clone of template repository
    │
    ▼
Stage 1: Run devcontainer-opencode.sh up
    │
    ▼
Stage 2: Execute project-setup workflow
    │
    ▼
Stage 3: Start Sentinel service
    │
    ▼
Stage 4: AI builds remaining features autonomously
```

---

## Risk Mitigations

| Risk | Mitigation |
|------|------------|
| GitHub API Rate Limiting | GitHub App tokens (5,000 req/hr), backoff strategy |
| LLM Looping/Hallucination | Max steps timeout, cost guardrails |
| Concurrency Collisions | Assign-then-verify locking pattern |
| Container Drift | Stop container between tasks |
| Security Injection | HMAC validation, credential scrubbing |

---

## References

- **Development Plan:** `plan_docs/OS-APOW Development Plan v4.2.md`
- **Architecture Guide:** `plan_docs/OS-APOW Architecture Guide v3.2.md`
- **Implementation Spec:** `plan_docs/OS-APOW Implementation Specification v1.2.md`
- **Plan Review:** `plan_docs/OS-APOW Plan Review.md`
- **Simplification Report:** `plan_docs/OS-APOW Simplification Report v1.md`
