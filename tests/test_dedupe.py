from datetime import datetime, timezone

from scraper.models import ProductSnapshot
from scraper.pipeline.dedupe import dedupe_snapshots


def _snap(ts: datetime, model: str, price: float) -> ProductSnapshot:
    return ProductSnapshot(
        timestamp=ts,
        model=model,
        title=f"{model}",
        sku="X",
        price_eur=price,
        product_url="https://example.com/a",
        image_url="https://example.com/a.png",
    )


def test_dedupe_removes_exact_duplicates() -> None:
    ts = datetime(2026, 2, 5, tzinfo=timezone.utc)
    a = _snap(ts, "iphone_15", 799.0)
    b = _snap(ts, "iphone_15", 799.0)
    out = dedupe_snapshots([a, b])
    assert len(out) == 1


def test_dedupe_keeps_price_changes() -> None:
    ts = datetime(2026, 2, 5, tzinfo=timezone.utc)
    a = _snap(ts, "iphone_15", 799.0)
    b = _snap(ts, "iphone_15", 749.0)  # price change
    out = dedupe_snapshots([a, b])
    assert len(out) == 2


def test_dedupe_is_stably_sorted() -> None:
    ts1 = datetime(2026, 2, 5, tzinfo=timezone.utc)
    ts2 = datetime(2026, 2, 6, tzinfo=timezone.utc)

    rows = [
        _snap(ts2, "iphone_16", 999.0),
        _snap(ts1, "iphone_17", 1099.0),
        _snap(ts1, "iphone_15", 799.0),
    ]
    out = dedupe_snapshots(rows)

    # sorted by (timestamp, model)
    assert [r.model for r in out] == ["iphone_15", "iphone_17", "iphone_16"]

