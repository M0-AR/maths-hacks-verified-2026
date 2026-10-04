# Methodology — Zero-to-Hero Verification Protocol (2026–2027 standard)

## 0. Principle
> **No file is enhanced by hand without execution.** Every claim in this repo is either
> (a) proved by a passing `pytest`, (b) measured and written to `results/tables/*.json`,
> or (c) explicitly labelled `surveyed, not verified` (e.g. RH proof, Continuum independence, Thurston geometries).

## 1. Map (book → code)
| Book part | Hacks | Module | Verifier |
|---|---|---|---|
| Tricks of the Trade | 1–13 | `run_all.py` + `tests` | induction loop, reductio demo, set ops, truth tables |
| Numerous Numbers | 14–34 | `numbers.py` | sieve, twins, Goldbach to 500, Collatz to 5000, Leibniz/MC π, PNT ratio, Fermat search |
| Science of Structure | 35–49 | `algebra.py` | Zₙ groups, S₃ order-6, rings vs fields, nCk=792, Euler bridges |
| Continuity | 50–56 | `calculus.py` | numeric derivative, trapezoid integral, Taylor, FTC, Lyapunov signs |
| Maths in Space | 57–88 | `geometry.py` | Euclid dist, V−E+F=2, Koch/Cantor, tesseract 16v/32e, spherical excess |
| Maths Meets Reality | 89–100 | `stochastics.py` + live | dice χ-proximity, Hurst, JB, ARCH, Nash, Turing toy, P-vs-NP timing |

## 2. Reproducibility contract
1. **Pinned env**: `python:3.11-slim` + `requirements.txt` (numpy 1.26.4, pandas 2.2.2, scipy 1.13.1, matplotlib 3.8.4, requests 2.32.3, pytest 8.3.2).
2. **Seeded RNG**: `MH_SEED=12345` via `seed_all()`; Monte-Carlo and synthetic fallback are deterministic.
3. **Provenance**: every live fetch writes `data/live_cache/live_<sym>.json` with `source ∈ {yahoo_v8, stooq, synthetic_offline}` + `fetched_at`.
4. **Three gates**: `pytest` → `run_all.py` → `benchmark_all.py` (+ `exp_live_market.py` for reality check). Docker runs all three: `docker compose up research`.
5. **Honest scope**: laptop-scale limits stated next to frontier (e.g. Collatz 5k here vs 2^71 literature). No silent extrapolation.

## 3. Live-data protocol (Hacks #95–97)
1. Primary: Yahoo v8 chart API (`query1.finance.yahoo.com`, no key): `range=1y&interval=1d`.
2. Fallback: Stooq CSV (`stooq.com/q/d/l/?s=spy.us&aapl.us&i=d`).
3. Offline: seeded GBM (μ=0.0004, σ=0.012, n=252) — labelled `synthetic_offline`, never masqueraded as live.
4. Tests per asset: log-returns → Hurst R/S, skew/kurtosis + Jarque–Bera, lag-1 autocorr of squared returns (vol clustering), annualised vol.
5. Interpretation rule: GBM/Wiener is the **null model**; fat tails + clustering are **expected deviations**, not refutations (matches Merton–Samuelson literature).

## 4. Hidden-pattern protocol (original contributions)
Each `DISC_*` must: (i) recompute from scratch, (ii) report effect size + n, (iii) state "supports heuristic, not proof".
- `DISC_benford_factorials`: leading-digit distribution of 1!..60! vs Benford log10(1+1/d).
- `DISC_collatz_stopping_vs_size`: OLS slope of stopping-time on log n (n≤2000) + max.
- `DISC_goldbach_growth`: OLS slope of log(partitions) on n (evens ≤500).
- `DISC_prime_gaps`: census to 5000 (max gap, mode, twin count).

## 5. Benchmark protocol
`benchmarks/benchmark_all.py` records wall-clock `timing_s` (relative, machine-noted) and `accuracy` (absolute errors vs closed forms). CI asserts accuracy, not timing.

## 6. Failure handling
- Network blocked → synthetic fallback + `source` field proves it; suite stays green.
- Yahoo schema change → Stooq; both fail → synthetic. All three paths covered by `test_live_fetch_never_crashes`.
- Non-determinism → seeds + `--allow-errors`-style isolation (notebook lessons from arXiv 2604.01072 applied to scripts).

## 7. From verification to PhD paper
`PAPER.md` is the publishable draft skeleton: abstract, related work (12-source vote table), methods (this file), results (paste `results/tables/*.json` values), threats to validity, future work (OU process, Green–Tao progressions, Jensen polynomials negative result, formal Lean proofs for #1–13).
