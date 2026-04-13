#!/bin/bash
set -e

echo "Setting up OS-APOW development environment..."

# Check for uv
if ! command -v uv &> /dev/null; then
    echo "Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# Install dependencies
echo "Installing Python dependencies with uv..."
uv sync

# Copy .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "IMPORTANT: Edit .env with your actual values before running the application."
fi

echo ""
echo "Development environment ready."
echo ""
echo "Available commands:"
echo "  uv run os-apow notifier    # Start the webhook receiver"
echo "  uv run os-apow sentinel    # Start the orchestrator"
echo "  uv run pytest              # Run tests"
echo "  uv run ruff check src/     # Lint"
echo "  uv run mypy src/           # Type check"
