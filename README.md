# 🟦 5 — Generate the HTML Dashboard (Chart.js) (Issue #6)

## 🎯 Goal

Convert the processed historical dataset into a **clean, static, portfolio‑ready HTML dashboard**.

The report is:

- **offline‑friendly** (uses cached local images)  
- **static** (no backend required)  
- **easy to share** (open `reports/index.html` in any browser)

This is the most visible artifact of the entire project.

---

## ✅ Prerequisites

Before running this milestone, you should already have:

- Historical data in `data/processed/prices.json` (from milestone **3**)  
- Local images cached in `assets/images/` + `image_path` in the dataset (from milestone **4**)  

---

## ⚙️ Expected output

After running the pipeline, you should have:

- `reports/index.html`  
- `reports/styles.css` (copied next to the HTML for a self‑contained report)

And the dashboard should display:

- current price per model  
- delta vs previous snapshot  
- local product images  
- a price history chart (Chart.js)  
- last updated timestamp  

---

## 📦 What the dashboard includes

### **Header**
- Title  
- Subtitle  
- “Last updated” timestamp (computed from snapshots)

### **Model cards**
Each card displays:

- local cached product image  
- product title  
- current price  
- delta (↑ / ↓ / –)  
- link to product page  
- model identifier  

### **Price history chart**
- one dataset per model  
- shared timeline with unique timestamps  
- human‑readable axis labels  
- smooth, clean chart layout  

---

## 📂 Files added or modified in this milestone

### `scraper/report/render.py`

**Responsibility:**

- load `prices.json`  
- group snapshots by model  
- sort snapshots chronologically  
- compute deltas (current − previous)  
- compute the latest timestamp (“Last updated”)  
- render the Jinja2 template into `reports/index.html`  
- copy `styles.css` into `reports/`  

```python
from __future__ import annotations

import json
from pathlib import Path
from collections import defaultdict

from jinja2 import Environment, FileSystemLoader, select_autoescape


def load_prices(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def prepare_context(rows: list[dict]) -> dict:
    """
    Context for template:
    - by_model: model -> snapshots sorted by timestamp
    - latest: model -> latest snapshot enriched with delta vs previous
    - last_updated: max timestamp across all rows
    """
    by_model: dict[str, list[dict]] = defaultdict(list)

    for r in rows:
        by_model[r.get("model", "unknown")].append(r)

    for model in by_model:
        by_model[model].sort(key=lambda x: x.get("timestamp", ""))

    # header "Last update"
    last_updated = ""
    if rows:
        last_updated = max(r.get("timestamp", "") for r in rows)

    # latest per model + delta
    latest: dict[str, dict] = {}
    for model, items in by_model.items():
        if not items:
            continue

        current = items[-1]
        prev = items[-2] if len(items) > 1 else None

        delta = None
        if prev:
            try:
                delta = round(float(current["price_eur"]) - float(prev["price_eur"]), 2)
            except Exception:
                delta = None

        latest[model] = {**current, "delta": delta}

    return {"by_model": dict(by_model), "latest": latest, "last_updated": last_updated}


def render_report(prices_json: Path, out_html: Path, templates_dir: Path) -> None:
    rows = load_prices(prices_json)
    ctx = prepare_context(rows)

    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(["html"]),
    )

    tpl = env.get_template("index.html.j2")
    html = tpl.render(**ctx)

    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(html, encoding="utf-8")

    # Copy CSS next to the HTML output so the report is self-contained
    css_src = templates_dir / "styles.css"
    css_dst = out_html.parent / "styles.css"
    if css_src.exists():
        css_dst.write_text(css_src.read_text(encoding="utf-8"), encoding="utf-8")
```

---

### `scraper/report/templates/index.html.j2`

**Responsibility:**

- defines the HTML structure (header, cards, chart)  
- renders cards per model  
- shows deltas with up/down/flat indicators  
- injects datasets into Chart.js  
- includes a Windows path normalization fix (`\` → `/`) so cached images load correctly  

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>iPhone Price Monitor</title>
  <link rel="stylesheet" href="./styles.css" />
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
  <header>
    <h1>📱 iPhone Price Monitor</h1>
    <p class="subtitle">Historical price tracking dashboard</p>
    <p class="muted">Last update: <strong>{{ last_updated }}</strong></p>
  </header>

  {% if not latest %}
    <p class="muted">
      No data yet. Run:
      <code>uv run python -m scraper.cli run</code>
    </p>
  {% endif %}

  <section class="cards">
    {% for model, item in latest.items() %}
    <a class="card" href="{{ item.product_url }}" target="_blank" rel="noopener">
      {# Normalize Windows paths (backslashes) into web paths #}
      <img src="../{{ (item.image_path | replace('\\', '/')) }}" alt="{{ item.title }}" />
      <h2>{{ item.title }}</h2>

      <p class="price">{{ '%.2f'|format(item.price_eur) }} €</p>

      {% if item.delta is not none %}
        {% if item.delta > 0 %}
          <p class="delta up">↑ +{{ '%.2f'|format(item.delta) }} €</p>
        {% elif item.delta < 0 %}
          <p class="delta down">↓ {{ '%.2f'|format(item.delta|abs) }} €</p>
        {% else %}
          <p class="delta flat">–</p>
        {% endif %}
      {% else %}
        <p class="delta flat">No previous data</p>
      {% endif %}

      <p class="model">{{ model }}</p>
    </a>
    {% endfor %}
  </section>

  <section class="chart">
    <div class="chart-head">
      <h3>Price history</h3>
      <p class="muted">Track how prices evolve over time.</p>
    </div>

    <div class="chart-container">
      <canvas id="priceChart"></canvas>
    </div>
  </section>

  <script>
    // Raw timestamps (unique, ordered)
    const labelsRaw = [
      {% for model, rows in by_model.items() %}
        {% for r in rows %}
          "{{ r.timestamp }}",
        {% endfor %}
      {% endfor %}
    ];
    const uniqLabelsRaw = [...new Set(labelsRaw)];

    // Human-readable labels for the X axis
    const labels = uniqLabelsRaw.map(ts => {
      const d = new Date(ts);
      const date = d.toLocaleDateString("en-GB", { day: "2-digit", month: "short" });
      const time = d.toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" });
      return `${date} ${time}`;
    });

    const datasets = [
      {% for model, rows in by_model.items() %}
      {
        label: "{{ model }}",
        data: uniqLabelsRaw.map(ts => {
          const found = [
            {% for r in rows %}
            { ts: "{{ r.timestamp }}", price: {{ r.price_eur }} },
            {% endfor %}
          ].find(x => x.ts === ts);
          return found ? found.price : null;
        }),
        spanGaps: true,
        tension: 0.35,
        pointRadius: 3
      },
      {% endfor %}
    ];

    new Chart(document.getElementById("priceChart"), {
      type: "line",
      data: { labels, datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "top" },
          tooltip: { mode: "index", intersect: false }
        },
        interaction: { mode: "nearest", intersect: false },
        scales: {
          x: {
            ticks: { maxTicksLimit: 5 }
          },
          y: {
            title: { display: true, text: "€" }
          }
        }
      }
    });
  </script>
</body>
</html>
```


---

### `scraper/report/templates/styles.css`

**Responsibility:**

- visual layout (grid cards)  
- hover effects  
- delta colors  
- chart sizing and spacing  
- modern light UI  

```css
body {
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Arial, sans-serif;
  margin: 32px;
  background: #f9fafb;
  color: #111827;
}

header { margin-bottom: 22px; }
header h1 { margin: 0 0 6px 0; font-size: 32px; }

.subtitle { margin: 0; color: #6b7280; }
.muted { color: #6b7280; margin-top: 8px; }

code {
  background: #eef2ff;
  border: 1px solid #e0e7ff;
  padding: 2px 8px;
  border-radius: 10px;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  margin: 18px 0 28px 0;
}

.card {
  display: block;
  background: white;
  border-radius: 14px;
  padding: 16px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
  text-align: center;
  text-decoration: none;
  color: inherit;
  border: 1px solid #eef2f7;
  transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 22px rgba(0,0,0,0.08);
  border-color: #e5e7eb;
}

.card img {
  width: 100%;
  height: 160px;
  object-fit: contain;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #eef2f7;
}

.card h2 { margin: 12px 0 6px 0; font-size: 18px; }
.price { font-size: 26px; font-weight: 800; margin: 6px 0 0 0; }

.model {
  margin: 8px 0 0 0;
  color: #6b7280;
  font-size: 13px;
}

.delta { font-weight: 800; margin-top: 6px; }
.delta.up { color: #16a34a; }
.delta.down { color: #dc2626; }
.delta.flat { color: #6b7280; }

/* Chart */
.chart {
  background: white;
  border-radius: 14px;
  padding: 16px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
  border: 1px solid #eef2f7;
}

.chart-head { margin-bottom: 10px; }
.chart-head h3 { margin: 0 0 6px 0; font-size: 18px; }

/* Keeps chart shorter & cleaner */
.chart-container { height: 320px; }
```

---

## ▶️ Generate the report

Run the full pipeline:

```bash
uv run python -m scraper.cli run
```

Open:

```
reports/index.html
```

---

## 🧪 Quick verification checklist

After running:

- ✅ `reports/index.html` exists  
- ✅ `reports/styles.css` exists  
- ✅ cards display images from `assets/images/`  
- ✅ chart renders and shows history lines  
- ✅ “Last update” is populated  

---

## 🔧 Troubleshooting

### 1) Images not loading (Windows paths)

If images fail to load on Windows, ensure your template uses:

```
{{ (item.image_path | replace('\\', '/')) }}
```

This converts Windows backslashes into web‑friendly paths.

---

### 2) Report shows “No data yet”

This means `data/processed/prices.json` is empty or missing.

Run:

```bash
uv run python -m scraper.cli run
```

Then confirm the JSON file contains snapshots.

---

### 3) Editor / file write issues (fallback)

If your editor fails to save file contents correctly, you can overwrite files using a heredoc:

```bash
cat > scraper/report/render.py <<'EOF'
# paste file content here
EOF
```

This is a last‑resort workaround used during development.

---

## ✅ What was achieved

By completing this milestone, the project now:

- ✔ generates a static HTML dashboard  
- ✔ displays current prices + price deltas  
- ✔ renders a price timeline chart (Chart.js)  
- ✔ uses cached local images (`image_path`)  
- ✔ produces a self‑contained report under `reports/`  

---

If quieres, puedo ayudarte a unir todos los pasos en un README final impecable y cohesivo.

