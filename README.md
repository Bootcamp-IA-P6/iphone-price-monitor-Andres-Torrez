# Step 5 — Generate the HTML Dashboard (Chart.js)

This step converts your processed historical dataset into a **clean, static, portfolio‑ready HTML dashboard**.  
The dashboard is fully offline‑friendly and can be opened directly in a browser.

---

## 🎯 Goal of this step

The purpose is to take the price history stored in `prices.json` and generate a visual dashboard that includes:

- Current price per iPhone model  
- Price delta vs previous snapshot  
- Local cached product images  
- A timeline chart showing price evolution  
- A “last updated” timestamp  
- A self‑contained HTML report inside `reports/`

This is the most visible artifact of the entire project.

---

## 📦 What the dashboard includes

### **Header**
- Title  
- Subtitle  
- Last update timestamp (computed from all snapshots)

### **Model cards**
Each card displays:
- Local product image  
- Product title  
- Current price  
- Price delta (↑ / ↓ / –)  
- Link to the product page  
- Model name  

### **Price history chart**
- One dataset per model  
- Shared timeline with unique timestamps  
- Human‑readable date/time labels  
- Smooth lines and clean layout  

---

## 🧠 Files added or modified in this step

Below you’ll find **each file involved**, followed by **your original code** and a clear explanation of what it does.

---

# `scraper/report/render.py`

This module is responsible for **loading the processed data, computing deltas, preparing the template context, and generating the final HTML report**.

It performs the following tasks:

- Loads `prices.json`  
- Groups snapshots by model  
- Sorts snapshots chronologically  
- Computes price deltas (current − previous)  
- Extracts the latest timestamp  
- Renders the Jinja2 template `index.html.j2`  
- Copies `styles.css` into the output folder  

### **Code**

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

# `scraper/report/templates/index.html.j2`

This is the **Jinja2 HTML template** used to generate the dashboard.

It defines:

- The page structure (header, cards, chart)  
- How each model card is rendered  
- How deltas are displayed  
- How timestamps and datasets are injected into Chart.js  
- A fix for Windows paths (`\` → `/`) so images load correctly  

### **Code**

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

# `scraper/report/templates/styles.css`

This stylesheet defines the **visual design** of the dashboard:

- Layout and spacing  
- Card design and hover effects  
- Delta color coding  
- Chart container height  
- Light, modern UI  

### **Code**

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

Run the pipeline:

```
uv run python -m scraper.cli run
```

Then open:

```
reports/index.html
```


---

## 🔧 Troubleshooting

If your editor has trouble writing files, you can overwrite them using a heredoc:

```
cat > scraper/report/render.py <<'EOF'
# (paste file content here)
EOF
```

---
