#!/usr/bin/env bash
set -euo pipefail

# Move to repository root
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

echo "[info] running pipeline..."

uv sync
uv pip install -e .

uv run pytest -q
uv run python -m scraper.cli run

echo "[ok] done"
