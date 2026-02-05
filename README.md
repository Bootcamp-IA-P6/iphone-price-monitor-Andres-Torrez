Perfecto, Andrés. Aquí tienes **todo tu contenido convertido a Markdown**, sin modificar nada del texto, solo dándole formato limpio, ordenado y perfectamente compatible con GitHub.

---

```markdown
# 📱 iPhone Price Monitor

Proyecto profesional de scraping diseñado para demostrar:

- Arquitectura limpia y modular
- Documentación paso a paso (reproducible)
- Buenas prácticas con uv (sin pip)
- Pipeline completo: scrapeo → histórico → reporte HTML
- Base lista para Docker + automatización

Este repo está pensado como proyecto de portfolio, no como un script suelto.

---

## 🎯 Objetivo

Monitorizar el precio de iPhone 15, 16 y 17, guardar un histórico y generar un HTML con timeline de cambios.

Fuente de datos (segura para scraping, controlada por nosotros):  
https://andres-torrez.github.io/iphone-catalog/

---

## 🧭 Roadmap (lo que construiremos)

Este proyecto se desarrolla por hitos (y se controla en el Kanban):

- ✅ Repo + Kanban + Issues + README base
- ✅ Scaffold con uv + estructura de carpetas
- ✅ CLI mínimo (healthcheck)
- ⏳ Scraper modular por fuentes (sources)
- ⏳ Exportación CSV y JSON
- ⏳ Descarga de imágenes del producto
- ⏳ Generación de HTML dashboard con timeline
- ⏳ Tests + lint
- ⏳ Docker
- ⏳ Automatización (cron o GitHub Actions)

---

## 🧱 Estructura del proyecto (actual)

```
iphone-price-monitor/
│
├── scraper/                     # Core application
│   ├── cli.py                   # Entry point (commands)
│   ├── config.py                # Global configuration
│   ├── models.py                # Data models (Pydantic)
│   ├── http_client.py           # HTTP utilities
│   │
│   ├── sources/                 # Website adapters (scrapers)
│   │   ├── base.py
│   │   └── github_pages_catalog.py
│   │
│   ├── pipeline/                # Data processing pipeline
│   │   ├── run.py
│   │   ├── normalize.py
│   │   └── dedupe.py
│   │
│   ├── storage/                 # Data persistence
│   │   ├── csv_store.py
│   │   └── json_store.py
│   │
│   ├── media/                   # Image download logic
│   │   └── images.py
│   │
│   └── report/                  # HTML generation
│       ├── render.py
│       └── templates/
│           └── index.html.j2
│
├── data/
│   ├── raw/                     # Raw responses (optional)
│   └── processed/               # CSV / JSON history
│
├── reports/                     # Generated HTML dashboard
│
├── assets/
│   ├── images/                  # Downloaded product images
│   └── docs/                    # Screenshots and diagrams
│
├── tests/                       # Pytest tests
│
├── .github/workflows/           # CI and scheduled runs
│
├── pyproject.toml               # Project definition (uv)
└── README.md
```

---

## ⚙️ pyproject.toml (lo que tenemos y qué significa)

Actualmente tu pyproject.toml contiene:

```
[project]
name = "iphone-price-monitor"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "httpx>=0.28.1",
    "jinja2>=3.1.6",
    "pydantic>=2.12.5",
    "selectolax>=0.4.6",
]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]

[dependency-groups]
dev = [
    "pytest>=9.0.2",
    "ruff>=0.14.14",
]
```

### ✅ Explicación rápida:

- `[project]` define el paquete (nombre, versión, python requerido)
- `dependencies` son librerías necesarias para correr el scraper
- `dependency-groups.dev` son dependencias solo para desarrollo (tests/lint)
- `ruff` es el linter/formateador para mantener código limpio y consistente

Nota: tu `requires-python = ">=3.13"` y `target-version = "py312"` están desalineados.  
Más adelante lo vamos a dejar consistente (recomendación: Python 3.12 o 3.13, pero ambos alineados).

---

## 🚀 Paso 1 — Instalación del entorno con uv

### 1.1 Instalar uv  
Guía oficial: https://docs.astral.sh/uv/

### 1.2 Inicializar el proyecto

```
uv init
```

### 1.3 Fijar versión de Python (recomendado)

Ejemplo (si usas 3.12):

```
uv python pin 3.12
```

### 1.4 Instalar dependencias

```
uv add httpx selectolax pydantic jinja2
uv add --dev pytest ruff
```

---

## 📁 Paso 2 — Crear estructura de carpetas y archivos

Creamos la arquitectura del repo (modular, escalable) con:

```
mkdir -p scraper/sources scraper/storage scraper/report/templates scraper/pipeline scraper/media
mkdir -p data/raw data/processed reports assets/images assets/docs tests .github/workflows
```

Crear archivos base:

```
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

## 🧪 Paso 3 — Implementar y probar el CLI (scraper/cli.py)

Este archivo es el punto de entrada: recibe comandos desde terminal.

### ✅ Contenido actual de scraper/cli.py (tal cual lo tienes):

```
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

### ¿Qué hace cada parte?

- `argparse` crea comandos tipo: healthcheck, run, etc.
- `cmd_healthcheck()` imprime un mensaje con la hora UTC para confirmar que todo corre
- `main()` decide qué comando ejecutar
- `python -m scraper.cli ...` ejecuta este módulo como programa

### ✅ Probar el CLI:

```
uv run python -m scraper.cli healthcheck
```

Salida esperada (ejemplo):

```
[ok] scraper CLI is working | utc=2026-02-05T...
```

---

## 🧹 Paso 4 — Lint con Ruff

Ruff mantiene el código limpio desde el primer día.

Ejecutar:

```
uv run ruff check .
```

---

## ▶️ ¿Qué pasará cuando ejecutemos run?

Más adelante añadiremos el comando:

```
uv run python -m scraper.cli run
```

Ese comando hará este flujo:

```
cli.py
  ↓
pipeline/run.py           (orquesta el proceso)
  ↓
sources/...               (scraping)
  ↓
pipeline/normalize.py     (limpia y normaliza precios)
  ↓
pipeline/dedupe.py        (evita duplicados)
  ↓
storage/csv_store.py      (guarda CSV histórico)
storage/json_store.py     (guarda JSON histórico)
  ↓
media/images.py           (descarga imágenes del producto)
  ↓
report/render.py          (genera HTML final)
  ↓
reports/index.html
```

---

## 📂 ¿Dónde se guardarán los resultados?

| Resultado            | Carpeta                      |
|---------------------|------------------------------|
| CSV histórico       | data/processed/prices.csv    |
| JSON histórico      | data/processed/prices.json   |
| Imágenes descargadas| assets/images/               |
| HTML final          | reports/index.html           |

---

## ✅ Commits (lo que ya hicimos)

- Scaffold del proyecto con uv
- Estructura modular
- CLI healthcheck funcionando
- Configuración de Ruff en pyproject.toml
- README documentando todo paso a paso

---

## 🧩 Próximo paso (Issue: feat(scraper))

Ahora que la base está lista, el siguiente hito será:

### ✅ Implementar el scraper real para:

- iPhone 15  
- iPhone 16  
- iPhone 17  

Desde:  
https://andres-torrez.github.io/iphone-catalog/

Y empezar a generar histórico.
```

---

Si quieres, puedo convertirlo también en una **versión con índice automático**, o añadir **badges**, o incluso un **diagrama visual del pipeline**.

