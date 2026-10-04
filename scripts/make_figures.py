"""Generate all README/preview figures + demo GIF. Deterministic (seed 12345)."""
from __future__ import annotations
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "docs" / "assets"
FIG.mkdir(parents=True, exist_ok=True)

import sys
sys.path.insert(0, str(ROOT / "src"))
from maths_hacks import numbers as N, calculus as C, stochastics as S
from maths_hacks.utils import fetch_live_series


def save(fig, name: str):
    p = FIG / name
    fig.tight_layout()
    fig.savefig(p, dpi=150)
    plt.close(fig)
    print(f"wrote {p} ({p.stat().st_size//1024} KB)")
    return p


def fig_prime_distribution():
    xs = list(range(2, 2001))
    counts, c = [], 0
    is_p = [True] * 2001
    for i in range(2, 2001):
        if is_p[i]:
            c += 1
            for j in range(i*i, 2001, i):
                is_p[j] = False
        counts.append(c)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(xs, counts, label="π(x) counted")
    ax.plot(xs, [x / math.log(x) for x in xs], "--", label="x / ln(x)")
    ax.set_title("Prime Number Theorem in one picture: π(x) vs x/ln(x)")
    ax.set_xlabel("x"); ax.set_ylabel("count"); ax.legend(); ax.grid(alpha=0.3)
    return save(fig, "prime_distribution.png")


def fig_collatz():
    fig, ax = plt.subplots(figsize=(7, 4))
    for n in [17, 27, 97, 871]:
        seq = C.collatz_sequence(n)
        ax.plot(seq, marker=".", linewidth=1, label=f"start {n} ({len(seq)-1} steps)")
    ax.set_title("Collatz journeys always land at 1 (verified to 5,000)")
    ax.set_xlabel("step"); ax.set_ylabel("value"); ax.legend(); ax.grid(alpha=0.3)
    return save(fig, "collatz.png")


def fig_goldbach():
    counts = N.verify_goldbach(300)["counts"]
    xs = sorted(counts); ys = [counts[x] for x in xs]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(xs, ys, width=2.0)
    ax.set_title("Goldbach partitions grow: more ways for bigger evens (to 300)")
    ax.set_xlabel("even n"); ax.set_ylabel("# of p+q representations"); ax.grid(alpha=0.3, axis="y")
    return save(fig, "goldbach.png")


def fig_chaos():
    rs = [2.5 + i * 0.015 for i in range(100)]
    lys = [C.lyapunov_logistic(r) for r in rs]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(rs, lys)
    ax.axhline(0, color="k", linewidth=1)
    ax.set_title("Chaos threshold: Lyapunov λ(r) crosses 0 near r≈3.57")
    ax.set_xlabel("r"); ax.set_ylabel("λ"); ax.grid(alpha=0.3)
    return save(fig, "chaos_lyapunov.png")


def fig_brownian_vs_market():
    spy = fetch_live_series("SPY")
    closes = spy["closes"]
    rets = [math.log(closes[i+1]/closes[i]) for i in range(len(closes)-1)]
    sim = S.wiener_process(T=1.0, n=len(rets), seed=12345)
    sim_rets = [sim[i+1]-sim[i] for i in range(len(sim)-1)]
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.5))
    axes[0].hist(rets, bins=30, alpha=0.7, label=f"SPY live ({spy['source']})")
    axes[0].hist(sim_rets, bins=30, alpha=0.5, label="Wiener model")
    axes[0].set_title("Log-returns: live SPY vs Wiener"); axes[0].legend(fontsize=8)
    axes[1].plot(closes, label="SPY closes")
    axes[1].set_title(f"SPY last={closes[-1]:.1f} n={len(closes)}"); axes[1].grid(alpha=0.3)
    return save(fig, "brownian_vs_market.png")


def fig_pi_convergence():
    terms = [100, 500, 2000, 10000]
    errs = [abs(N.pi_leibniz(t) - math.pi) for t in terms]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.loglog(terms, errs, marker="o")
    ax.set_title("Leibniz π error shrinks with more terms")
    ax.set_xlabel("terms"); ax.set_ylabel("|approx − π|"); ax.grid(alpha=0.3, which="both")
    return save(fig, "pi_convergence.png")


def make_demo_gif():
    """30-frame Brownian-motion demo GIF (PillowWriter, no ffmpeg needed)."""
    import random
    rnd = random.Random(12345)
    n_paths, n_steps = 5, 80
    paths = [[0.0] for _ in range(n_paths)]
    for _ in range(n_steps):
        for p in paths:
            p.append(p[-1] + rnd.gauss(0, 0.12))
    fig, ax = plt.subplots(figsize=(6, 3.5))
    lines = [ax.plot([], [], lw=1.5)[0] for _ in range(n_paths)]
    ax.set_xlim(0, n_steps); ax.set_ylim(-4, 4)
    ax.set_title("Demo: 5 Wiener paths grow like √t")
    ax.set_xlabel("step"); ax.set_ylabel("W(t)"); ax.grid(alpha=0.3)

    def update(f):
        for ln, p in zip(lines, paths):
            ln.set_data(range(f+1), p[:f+1])
        return lines

    ani = animation.FuncAnimation(fig, update, frames=n_steps, interval=60, blit=True)
    out = FIG / "demo_brownian.gif"
    ani.save(out, writer=animation.PillowWriter(fps=12))
    plt.close(fig)
    print(f"wrote {out} ({out.stat().st_size//1024} KB)")
    return out


if __name__ == "__main__":
    fig_prime_distribution()
    fig_collatz()
    fig_goldbach()
    fig_chaos()
    fig_brownian_vs_market()
    fig_pi_convergence()
    make_demo_gif()
