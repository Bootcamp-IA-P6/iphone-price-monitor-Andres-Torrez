<<<<<<< HEAD
# 📱 iPhone Price Monitor

A modular, documented and reproducible web scraping project that monitors iPhone prices over time and generates a visual HTML dashboard.

This project is designed as a **portfolio-quality example** of:
- Clean project architecture
- Modular scraping design
- Data persistence
- Automated reporting
- Dockerization and scheduling
- Professional documentation

---

## 🎯 Goal

Monitor price changes for iPhone models (15, 16, 17) from a controlled source website and build a historical dataset with visual reporting.

Source website (scraping-safe):
https://andres-torrez.github.io/iphone-catalog/

---

## 🗂️ Project Structure

```
iphone-price-monitor/
│
├── scraper/                     # Core application
│   ├── cli.py                   # Entry point (commands)
│   ├── config.py                # Global configuration
│   ├── models.py                # Data models (Pydantic)
│   ├── http_client.py          # HTTP utilities
│   │
│   ├── sources/                # Website adapters (scrapers)
│   │   ├── base.py
│   │   └── github_pages_catalog.py
│   │
│   ├── pipeline/               # Data processing pipeline
│   │   ├── run.py
│   │   ├── normalize.py
│   │   └── dedupe.py
│   │
│   ├── storage/                # Data persistence
│   │   ├── csv_store.py
│   │   └── json_store.py
│   │
│   ├── media/                  # Image download logic
│   │   └── images.py
│   │
│   └── report/                 # HTML generation
│       ├── render.py
│       └── templates/
│           └── index.html.j2
│
├── data/
│   ├── raw/                    # Raw responses (optional)
│   └── processed/              # CSV / JSON history
│
├── reports/                    # Generated HTML dashboard
│
├── assets/
│   ├── images/                 # Downloaded product images
│   └── docs/                   # Screenshots and diagrams
│
├── tests/                      # Pytest tests
│
├── .github/workflows/          # CI and scheduled runs
│
├── pyproject.toml              # Project definition (uv)
└── README.md
```


---

## ⚙️ Requirements

- Python 3.12+
- uv (package and environment manager)

Install uv:
https://docs.astral.sh/uv/

---

## 🐍 Virtual Environment with uv (no manual activation)

This project uses **uv** instead of pip and venv.

You do **not** activate a virtual environment manually.

uv automatically creates and manages an isolated environment for the project.

### First time setup

```bash
uv init
uv python pin 3.12
uv add httpx selectolax pydantic jinja2
uv add --dev pytest ruff
```

### Running commands

Always use:

```bash
uv run <command>
```

Examples:

```bash
uv run python -m scraper.cli healthcheck
uv run ruff check .
uv run pytest
```

uv ensures all commands run inside the project environment automatically.


## 🚀 Installation

```bash
uv init
uv add httpx selectolax pydantic jinja2
uv add --dev pytest ruff
```

---

## ▶️ Run the pipeline

```bash
uv run python -m scraper.cli run
```

This will:

1. Scrape product data
2. Store historical data in CSV and JSON
3. Download product images
4. Generate an HTML dashboard

---

## 📊 Outputs

After running, you will find:

- `data/processed/prices.csv`
- `data/processed/prices.json`
- `reports/index.html`
- `assets/images/*.png`

---

## 🧠 Architecture

The scraper is built using a **source adapter pattern**:

```
sources → normalize → store → report
```

This allows adding new websites without modifying the pipeline.

---

## 🗺️ Roadmap

See the GitHub Project board for step-by-step development progress.

---

## 🐳 Docker & Automation (later steps)

The project will be dockerized and scheduled via cron or GitHub Actions.
=======
>>>>>>> 0af7798 (chore: scaffold project structure with uv)
