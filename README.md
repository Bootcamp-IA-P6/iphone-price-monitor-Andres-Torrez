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

## 🧱 Project Structure

```
scraper/        → scraping logic and pipeline
data/           → csv/json/parquet historical data
reports/        → generated HTML dashboard
assets/         → downloaded product images and docs
tests/          → pytest tests
.github/        → CI and automation
```

---

## ⚙️ Requirements

- Python 3.12+
- uv (package and environment manager)

Install uv:
https://docs.astral.sh/uv/

---

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
