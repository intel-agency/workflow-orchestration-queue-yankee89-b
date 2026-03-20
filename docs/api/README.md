# API Documentation

## Overview

The OS-APOW Notifier exposes a FastAPI-based webhook receiver for processing GitHub events.

## Endpoints

### `GET /`

Root endpoint returning API information.

**Response:**
```json
{
  "name": "OS-APOW Event Notifier",
  "version": "0.1.0",
  "docs": "/docs"
}
```

### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "online",
  "system": "OS-APOW Notifier"
}
```

### `POST /webhooks/github`

Handle GitHub webhook events.

**Headers:**
- `X-GitHub-Event`: Event type (e.g., "issues")
- `X-Hub-Signature-256`: HMAC signature for payload verification

**Supported Events:**

#### Issues - Opened

When an issue is opened with:
- Title containing `[Application Plan]`, or
- Label `agent:plan`

Creates a `PLAN` type work item and adds `agent:queued` label.

**Response (accepted):**
```json
{
  "status": "accepted",
  "item_id": "12345"
}
```

**Response (ignored):**
```json
{
  "status": "ignored",
  "reason": "No actionable OS-APOW event mapping found"
}
```

## Authentication

All webhook requests must include a valid `X-Hub-Signature-256` header containing an HMAC-SHA256 signature of the request body using the `WEBHOOK_SECRET`.

## Interactive Documentation

When running the notifier, interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
