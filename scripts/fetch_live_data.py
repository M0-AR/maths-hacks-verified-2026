"""Live-data fetch script (standalone): caches SPY + BTC-USD with provenance."""
from maths_hacks.utils import fetch_live_series

if __name__ == "__main__":
    for sym in ("SPY", "BTC-USD", "AAPL"):
        s = fetch_live_series(sym)
        print(f"{sym}: source={s['source']} n={s['n']} last={s['closes'][-1]:.2f}")
