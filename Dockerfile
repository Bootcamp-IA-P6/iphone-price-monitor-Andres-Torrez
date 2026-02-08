FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files first (better cache)
COPY pyproject.toml README.md ./

# ✅ Copy the package source BEFORE uv sync (so the project can be built)
COPY scraper ./scraper

# Install dependencies
RUN uv sync

# Copy project source
COPY . .

# Install project in editable mode
RUN uv pip install -e .

# Default command: run scraper + report
CMD ["uv", "run", "python", "-m", "scraper.cli", "run"]
