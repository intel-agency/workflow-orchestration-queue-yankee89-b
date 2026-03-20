# ADR-001: GitHub Issues as Work Queue

## Status

Accepted

## Context

OS-APOW needs a persistent, observable work queue to manage agentic tasks. The queue must support:

- Task lifecycle tracking (queued, in-progress, success, error)
- Concurrent access from multiple sentinels
- Human visibility and intervention
- Integration with existing development workflows

Options considered:
1. **Message Queue (RabbitMQ, SQS)** - Traditional queue with strong guarantees
2. **Database-backed Queue** - Custom implementation with full control
3. **GitHub Issues** - Leverage existing GitHub workflow and UI
4. **Linear/Jira** - Third-party project management tools

## Decision

We will use **GitHub Issues** as the work queue backing store.

### Implementation Details

- **Labels as State**: GitHub issue labels represent work item status
  - `agent:queued` - Task is waiting to be processed
  - `agent:in-progress` - Task is being worked on
  - `agent:success` - Task completed successfully
  - `agent:error` - Task failed with recoverable error
  - `agent:infra-failure` - Infrastructure-level failure

- **Comments as Logs**: Task progress, heartbeats, and results are posted as issue comments

- **Assignees for Locking**: The assign-then-verify pattern provides distributed locking

## Consequences

### Positive

- **Zero Infrastructure**: No additional services to deploy or maintain
- **Native Observability**: All task state visible in GitHub UI
- **Human-in-the-Loop**: Developers can intervene, comment, or close issues
- **Integration**: Works seamlessly with existing GitHub workflows
- **Audit Trail**: Full history of task lifecycle in issue timeline

### Negative

- **Rate Limits**: GitHub API rate limits may constrain throughput
- **Polling Latency**: Poll-based discovery vs. push notifications
- **Vendor Lock-in**: Tight coupling to GitHub (mitigated by ITaskQueue interface)

### Mitigations

- Implement jittered exponential backoff for rate limit handling
- Future phases may add webhook-based task discovery
- ITaskQueue interface allows swapping queue backends
