# 📱 iPhone Price Monitor

Sistema modular para scrapear precios de iPhones, normalizar datos, evitar duplicados, generar reportes HTML y mantener un histórico limpio y automatizable.

---

## 🚀 Paso 1 — Inicializar proyecto con `uv`

### 1.3 Fijar versión de Python (recomendado)

Ejemplo usando Python 3.12:

```bash
uv python pin 3.12
```

### 1.4 Instalar dependencias

```bash
uv add httpx selectolax pydantic jinja2
uv add --dev pytest ruff
```

---

## 📁 Paso 2 — Crear estructura de carpetas

Arquitectura modular y escalable:

```bash
mkdir -p scraper/sources scraper/storage scraper/report/templates scraper/pipeline scraper/media
mkdir -p data/raw data/processed reports assets/images assets/docs tests .github/workflows
```

Archivos base:

```bash
touch scraper/__init__.py scraper/cli.py scraper/config.py scraper/models.py scraper/http_client.py
touch scraper/sources/__init__.py scraper/sources/base.py scraper/sources/github_pages_catalog.py
touch scraper/storage/__init__.py scraper/storage/csv_store.py scraper/storage/json_store.py
touch scraper/report/__init__.py scraper/report/render.py scraper/report/templates/index.html.j2
touch scraper/pipeline/__init__.py scraper/pipeline/run.py scraper/pipeline/normalize.py scraper/pipeline/dedupe.py
touch scraper/media/__init__.py scraper/media/images.py
touch tests/test_normalize.py tests/test_dedupe.py
touch .gitignore
```

---

## 🧪 Paso 3 — Implementar y probar el CLI

Archivo principal: `scraper/cli.py`

```python
from __future__ import annotations

import argparse
from datetime import UTC, datetime


def cmd_healthcheck() -> None:
    now = datetime.now(UTC).isoformat()
    print(f"[ok] scraper CLI is working | utc={now}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="scraper",
        description="iPhone Price Monitor CLI",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("healthcheck", help="Validate the CLI runs")

    args = parser.parse_args()

    if args.command == "healthcheck":
        cmd_healthcheck()
    else:
        raise SystemExit("Unknown command")


if __name__ == "__main__":
    main()
```

### Probar el CLI

```bash
uv run python -m scraper.cli healthcheck
```

Salida esperada:

```
[ok] scraper CLI is working | utc=2026-02-05T...
```

---

## 🧹 Paso 4 — Lint con Ruff

```bash
uv run ruff check .
```

---

## ▶️ Flujo completo del comando `run`

Cuando implementemos `scraper run`, el pipeline seguirá este orden:

```
cli.py
  ↓
pipeline/run.py
  ↓
sources/...               (scraping)
  ↓
pipeline/normalize.py     (limpieza y normalización)
  ↓
pipeline/dedupe.py        (evitar duplicados)
  ↓
storage/csv_store.py      (guardar CSV)
storage/json_store.py     (guardar JSON)
  ↓
media/images.py           (descargar imágenes)
  ↓
report/render.py          (generar HTML)
  ↓
reports/index.html
```

---

## 📂 Salida del sistema

| Resultado             | Carpeta                       |
|----------------------|-------------------------------|
| CSV histórico        | `data/processed/prices.csv`   |
| JSON histórico       | `data/processed/prices.json`  |
| Imágenes descargadas | `assets/images/`              |
| HTML final           | `reports/index.html`          |

---

## ✅ Progreso actual

- Scaffold del proyecto con `uv`
- Estructura modular creada
- CLI `healthcheck` funcionando
- Ruff configurado en `pyproject.toml`
- README documentando todo el setup

---

## 🧩 Próximo paso — `feat(scraper)`

Implementar scraper real para:

- iPhone 15  
- iPhone 16  
- iPhone 17  

Fuente:

https://andres-torrez.github.io/iphone-catalog/

Y comenzar a generar histórico.
