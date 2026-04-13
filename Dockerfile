# OS-APOW Dockerfile
# Single-stage build for the OS-APOW Python application

FROM python:3.12-slim

# Install uv for fast package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml ./

# Copy source code (required for editable install)
COPY src/ ./src/

# Install the package in editable mode
RUN uv pip install --system --no-cache -e .

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

# Copy application code with correct ownership
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser pyproject.toml ./

# Switch to non-root user
USER appuser

# Expose default port for notifier
EXPOSE 8000

# Health check using Python stdlib (no curl dependency)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]

# Default command (can be overridden)
CMD ["uvicorn", "src.os_apow.notifier.service:app", "--host", "0.0.0.0", "--port", "8000"]
