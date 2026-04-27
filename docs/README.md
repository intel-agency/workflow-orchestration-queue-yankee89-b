# OS-APOW Documentation

Welcome to the OS-APOW (Open Source Agentic Process Orchestration Workflow) documentation.

## Overview

OS-APOW is a headless agentic orchestration platform built on four pillars:

| Pillar | Component | Purpose |
|--------|-----------|---------|
| The Ear | Work Event Notifier | FastAPI webhook ingestion |
| The State | Work Queue | GitHub Issues as state machine |
| The Brain | Sentinel Orchestrator | Polling, task claiming, lifecycle |
| The Hands | Opencode Worker | DevContainer-based code execution |

## Documentation Structure

- **[Architecture](./architecture/)** - System architecture and design decisions
- **[API](./api/)** - API documentation for the Notifier service
- **[Development](./development.md)** - Development setup and guidelines

## Quick Start

1. Copy `.env.example` to `.env` and fill in your values
2. Install dependencies: `uv sync`
3. Run the notifier: `uv run os-apow notifier`
4. Run the sentinel: `uv run os-apow sentinel`

## Architecture Decision Records (ADRs)

See the [architecture](./architecture/) directory for design decisions.
