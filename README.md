# 📱 iPhone Price Monitor

> A production‑style scraping system that tracks price evolution, stores historical data, caches media locally, and generates an interactive dashboard.

This project demonstrates how real‑world data pipelines are designed, structured, and evolved.

---

## ✨ Why this project matters

Most scraping examples online are just single scripts.

This repository shows how to build something closer to what companies expect:

- modular architecture  
- source adapter pattern  
- reproducible environments  
- historical storage  
- media caching  
- reporting layer  
- automated validation  
- extensibility for future sources  

---

## 🎯 Objective

Monitor price changes for:

- iPhone 15  
- iPhone 16  
- iPhone 17  

Store snapshots over time and visualize trends in an HTML dashboard.

Scraping‑safe catalog (controlled environment):  
https://andres-torrez.github.io/iphone-catalog/

---

## 🖼 Example Output

After running the pipeline, an HTML report is generated with:

- current price per model  
- variation vs previous snapshot  
- timeline chart  
- local product images  
- link to the source page  

*(Add screenshots in `assets/docs/` and reference them here.)*

---

## 🧱 System Architecture

```
CLI
↓
Source Adapter
↓
Normalization
↓
Deduplication
↓
Storage (CSV / JSON)
↓
Media Cache
↓
HTML Report
```

Each component is isolated and replaceable.

---

## 🧩 Tech Stack

- Python  
- uv (dependency & environment management)  
- httpx  
- selectolax  
- pydantic  
- jinja2  
- pytest  
- ruff  
- Chart.js  

---

## 📂 Repository layout

```text
scraper/
  sources/        # website adapters
  pipeline/       # transformations
  storage/        # persistence
  media/          # image downloads
  report/         # dashboard generation

data/             # historical outputs
assets/           # images & docs
reports/          # generated site
tests/            # validations
```

---

## 🚀 Quick Start

```bash
uv sync
uv pip install -e .
uv run python -m scraper.cli run
```

Open:

```
reports/index.html
```

---

## 📚 Step-by-step build

The project is intentionally constructed in milestones.

You can reproduce the entire system from scratch.

```
docs/
├── 01_setup.md
├── 02_source_adapter.md
├── 03_pipeline.md
├── 04_media.md
├── 05_report.md
```

---

## 🧪 Quality checks

```bash
uv run pytest
uv run ruff check .
```

---

## 📈 What recruiters usually like in this repo

- separation of concerns  
- evolution through commits  
- honest troubleshooting documentation  
- deterministic outputs  
- CLI interface  
- test coverage  
- clean dependency management  
- clear path to Docker & CI  

---

## 🔮 Future ideas

- additional data stores  
- notifications / alerts  
- public API  
- cloud execution  
- more visual analytics  

---

## 👨‍💻 Author

Built as a professional portfolio project to demonstrate practical software engineering in scraping and data pipelines.
