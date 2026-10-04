"""Shared utilities: seeding, paths, live-data fetch with offline fallback."""
from __future__ import annotations
import json
import os
import random
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
RESULTS = ROOT / "results"
TABLES = RESULTS / "tables"
FIGURES = RESULTS / "figures"

SEED = int(os.environ.get("MH_SEED", "12345"))


def seed_all(seed: int = SEED) -> None:
    random.seed(seed)
    try:
        import numpy as np
        np.random.seed(seed)
    except Exception:
        pass


def ensure_dirs() -> None:
    for p in [DATA / "processed", DATA / "live_cache", TABLES, FIGURES]:
        p.mkdir(parents=True, exist_ok=True)


def save_json(name: str, payload: dict) -> Path:
    ensure_dirs()
    p = TABLES / name
    p.write_text(json.dumps(payload, indent=2, default=str))
    return p


def _yahoo_chart(symbol: str, range_: str = "1y", interval: str = "1d", timeout: int = 15) -> dict | None:
    """Fetch OHLC closes from Yahoo Finance v8 chart API (no key required)."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={range_}&interval={interval}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8", errors="replace"))
    except Exception:
        return None


def _stooq_daily(symbol: str, timeout: int = 15) -> str | None:
    """Stooq free CSV fallback, e.g. spy.us, aapl.us, btcusd."""
    url = f"https://stooq.com/q/d/l/?s={symbol}&i=d"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception:
        return None


def fetch_live_series(symbol: str = "SPY", cache_name: str | None = None) -> dict:
    """Fetch live daily closes for a symbol, with deterministic synthetic fallback.

    Returns dict with keys: symbol, source (yahoo/stooq/synthetic_offline),
    closes (list[float]), dates (list), fetched_at, n, provenance.
    Never raises: offline environments get seeded synthetic GBM so the
    full suite stays reproducible (source is recorded honestly).
    """
    ensure_dirs()
    cache_name = cache_name or f"live_{symbol.replace('=','').replace('/','_').lower()}.json"
    cache = DATA / "live_cache" / cache_name

    closes: list[float] = []
    dates: list = []
    source = "synthetic_offline"

    y = _yahoo_chart(symbol)
    try:
        if y and y.get("chart", {}).get("result"):
            res = y["chart"]["result"][0]
            ts = res.get("timestamp", [])
            q = res.get("indicators", {}).get("quote", [{}])[0]
            cl = q.get("close", [])
            pairs = [(t, c) for t, c in zip(ts, cl) if c is not None]
            if len(pairs) > 30:
                dates = [time.strftime("%Y-%m-%d", time.gmtime(t)) for t, _ in pairs]
                closes = [float(c) for _, c in pairs]
                source = "yahoo_v8"
    except Exception:
        pass

    if not closes:
        # Stooq mapping for common symbols
        mapping = {"SPY": "spy.us", "AAPL": "aapl.us", "BTC-USD": "btcusd", "BTCUSD": "btcusd"}
        st = mapping.get(symbol, "spy.us")
        csv = _stooq_daily(st)
        try:
            if csv and "Date" in csv:
                lines = csv.strip().splitlines()[1:]
                for ln in lines[-260:]:
                    parts = ln.split(",")
                    if len(parts) >= 5:
                        dates.append(parts[0])
                        closes.append(float(parts[4]))
                if len(closes) > 30:
                    source = "stooq"
        except Exception:
            closes, dates = [], []

    if not closes:
        # Deterministic synthetic GBM (seeded) — honest offline fallback
        seed_all()
        import math
        n = 252
        s, mu, sigma = 100.0, 0.0004, 0.012
        closes = [s]
        for i in range(1, n):
            import random as _r
            shock = _r.gauss(0, 1)
            closes.append(closes[-1] * math.exp((mu - 0.5 * sigma**2) + sigma * shock))
        dates = [f"synth-{i:04d}" for i in range(n)]
        source = "synthetic_offline"

    payload = {
        "symbol": symbol,
        "source": source,
        "n": len(closes),
        "closes": closes,
        "dates": dates,
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "provenance": "yahoo_v8 primary, stooq fallback, seeded-GBM offline fallback; source field is authoritative",
    }
    try:
        cache.write_text(json.dumps(payload))
    except Exception:
        pass
    return payload
