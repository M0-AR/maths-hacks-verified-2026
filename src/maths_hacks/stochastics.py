"""Hacks #95-100: reality — probability, stats, Brownian, games, computability, PvsNP."""
from __future__ import annotations
import math
import random


def dice_distribution(trials: int = 60_000, seed: int = 12345) -> dict:
    rnd = random.Random(seed)
    counts = {s: 0 for s in range(2, 13)}
    for _ in range(trials):
        counts[rnd.randint(1, 6) + rnd.randint(1, 6)] += 1
    total = sum(counts.values())
    empirical = {k: v / total for k, v in counts.items()}
    # theory: ways/36
    ways = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}
    theory = {k: v / 36 for k, v in ways.items()}
    max_err = max(abs(empirical[k] - theory[k]) for k in counts)
    return {"empirical": empirical, "theory": theory, "max_abs_err": max_err, "trials": trials}


def descriptive_stats(xs: list[float]) -> dict:
    import statistics
    return {
        "n": len(xs),
        "mean": statistics.mean(xs),
        "median": statistics.median(xs),
        "stdev": statistics.pstdev(xs),
        "min": min(xs),
        "max": max(xs),
    }


def wiener_process(T: float = 1.0, n: int = 1000, seed: int = 12345) -> list[float]:
    rnd = random.Random(seed)
    dt = T / n
    w, out = 0.0, [0.0]
    for _ in range(n):
        w += math.sqrt(dt) * rnd.gauss(0, 1)
        out.append(w)
    return out


def gbm_path(s0: float = 100.0, mu: float = 0.05, sigma: float = 0.2, T: float = 1.0,
             n: int = 252, seed: int = 7) -> list[float]:
    rnd = random.Random(seed)
    dt = T / n
    s, out = s0, [s0]
    for _ in range(n):
        s *= math.exp((mu - 0.5 * sigma**2) * dt + sigma * math.sqrt(dt) * rnd.gauss(0, 1))
        out.append(s)
    return out


def hurst_exponent(series: list[float], max_lag: int = 20) -> float:
    """Simple R/S Hurst estimator (H~0.5 random, >0.5 trending, <0.5 mean-reverting)."""
    import math as m
    lags = list(range(2, max_lag + 1))
    tau = []
    for lag in lags:
        chunks = [series[i:i + lag] for i in range(0, len(series) - lag + 1, lag)]
        rs = []
        for c in chunks:
            if len(c) < lag:
                continue
            mean = sum(c) / len(c)
            dev = [x - mean for x in c]
            cum = []
            s = 0.0
            for d in dev:
                s += d
                cum.append(s)
            r = max(cum) - min(cum)
            var = sum(d * d for d in dev) / len(dev)
            if var > 0:
                rs.append(r / m.sqrt(var))
        if rs:
            tau.append(sum(rs) / len(rs))
    if len(tau) < 2:
        return float("nan")
    lx = [m.log(l) for l in lags[:len(tau)]]
    ly = [m.log(t) for t in tau]
    mx, my = sum(lx) / len(lx), sum(ly) / len(ly)
    num = sum((a - mx) * (b - my) for a, b in zip(lx, ly))
    den = sum((a - mx) ** 2 for a in lx) or 1e-12
    return num / den


def prisoners_dilemma() -> dict:
    # (row_years, col_years); lower is better
    payoffs = {
        ("quiet", "quiet"): (1, 1),
        ("quiet", "betray"): (10, 0),
        ("betray", "quiet"): (0, 10),
        ("betray", "betray"): (5, 5),
    }

    def best_response(other: str) -> str:
        return min(["quiet", "betray"], key=lambda mine: payoffs[(mine, other)][0])

    return {
        "payoffs": {f"{k[0]}/{k[1]}": v for k, v in payoffs.items()},
        "best_vs_quiet": best_response("quiet"),
        "best_vs_betray": best_response("betray"),
        "nash": ("betray", "betray"),
        "pareto_optimal": ("quiet", "quiet"),
    }


def turing_demo(tape: str = "1111", rule: str = "increment_unary") -> str:
    """Toy Turing-style machine: unary increment (1111 -> 11111)."""
    if rule == "increment_unary":
        assert set(tape) <= {"1"}, "unary tape only"
        return tape + "1"
    raise ValueError("unknown rule")


def poly_vs_exp_timing() -> dict:
    """P vs NP intuition (#100): linear scan vs brute-force subset search."""
    import time
    linear_n = 10_000
    xs = list(range(linear_n))
    t0 = time.perf_counter()
    assert sum(1 for _ in xs if _ == linear_n - 1) == 1
    t_linear = time.perf_counter() - t0

    # NP-style: subset-sum brute force grows as 2^n (tiny n only!)
    t0 = time.perf_counter()
    arr, target = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9], 25
    found = None
    n = len(arr)
    for mask in range(1 << n):
        if sum(arr[i] for i in range(n) if mask >> i & 1) == target:
            found = mask
            break
    t_exp = time.perf_counter() - t0
    return {"linear_scan_10k_s": t_linear, "subset_sum_2_15_s": t_exp, "subset_found": found is not None}
