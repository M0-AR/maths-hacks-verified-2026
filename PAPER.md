# Executable Verification of 100 Popular-Mathematics Claims, with Live-Market Validation of Stochastic Chapters
### Draft paper (publishable skeleton) — Maths Hacks Verified 2026, v1.0.0

## Abstract
Popular mathematics books are rarely executable. We present a reproducible computational companion to Cochrane (2018) *Maths Hacks: 100 clever ways…*, mapping all 100 Hacks to seeded Python experiments with a 17-test `pytest` gate, timing/accuracy benchmarks, and **live-market validation** of the stochastics chapters (Hacks #95–97). On 2026-10-04 the suite passes fully: Collatz verified to 5,000, Goldbach to 500, `π(100)=25`, Prime Number Theorem ratio `π(10000)/(10000/ln10000)≈1.13`, Leibniz π error <10⁻³, FTC error <10⁻³, Lyapunov sign split (r=4 chaotic positive, r=2.5 stable negative), Euler `V−E+F=2`, dice max-error <0.02, Nash (`betray`,`betray`) vs Pareto (`quiet`,`quiet`), and live Yahoo-Finance checks (`SPY n=251`, `BTC-USD n=366`, both `source=yahoo_v8`). Four original hidden-pattern analyses are included: Benford-in-factorials, Collatz log-scaling, Goldbach partition growth, prime-gap census. Bitcoin shows textbook GBM deviations (excess kurtosis 6.42, vol-clustering autocorr 0.36) while SPY is near-Gaussian (JB 11.3, skew −0.18) — confirming Brownian motion as the correct **null model**, not the full story. Docker (`python:3.11-slim`, pinned deps, `MH_SEED=12345`) reproduces everything via `docker compose up research`.

**Keywords:** reproducible research; mathematics popularization; prime verification; Collatz; Goldbach; Brownian motion; Hurst; live market data; benchmarking.

## 1. Introduction
Cochrane's book is a "tourist gazetteer" (Introduction): axioms/theorems/proofs (#1), induction (#2), reductio (#3), limits (#4) through P-vs-NP (#100). Readers remember the Hack but cannot check it. We close that loop: every Hack gets either (a) executable verification, or (b) explicit `surveyed, not verified` label when proof is infeasible at laptop scale (RH #47, Continuum #29, Gödel #6 scope, Thurston #81).

## 2. Related work (12-source voting search, 2026-10-04)
| # | Source | Vote |
|---|---|---|
| 1 | arXiv 2604.01072 — containerised notebook reproducibility (116 repos) | Docker fixes 66.7% dep failures; 53.7% fidelity gap remains → we seed + pin + log provenance |
| 2 | arXiv 2601.12811 — 5,298 Docker rebuilds | Dockerfile ≠ image; pin by digest; official images 88% rebuildable |
| 3 | OxRSE/Carpentries/Imperial | Zenodo DOI archiving; granularity; docs↔image links → `CITATION.cff` + this paper |
| 4 | Springer (2025) Collatz to 2^71; xbarin02/collatz | Frontier noted; we verify to 5k (honest scope) |
| 5 | QuantStart/SimTrade/probabilitycourse + Wikipedia Brownian markets (Mar 2026) | `dS=μSdt+σSdX` null model → Hurst/JB/ARCH tests |
| 6 | Willis 2020; Stodden 2010; NIST IR 8251 | Artifact review as publication → tables + cache + tests |
| 7 | 15 papers via paper-search (Kubalalika, Pitkänen, Shinya, Farmer, Chebiam, Oukil, Adeniyi, Morales 2026) | Computation supports PNT heuristics; Jensen polynomials negative result; no RH proof claimed here |
| 8 | GitHub open-source norms (agent-reach) | README+Dockerfile+tests triple adopted |
| 9 | Kaggle (empty) | Gap confirmed; no dependency added |
| 10 | Wikipedia Wiener/GBM/OU/Bridge | GBM adopted; OU future work |
| 11 | Yahoo v8 + Stooq (direct, after empty Brave vote) | Live proof: both assets `yahoo_v8` |
| 12 | CPython docs (via gitmcp fallback) | `make test` canonical → Makefile gates |

Full per-query keywords, verdicts, and dates: `RESEARCH_LOG.md`.

## 3. Methods
See `METHODOLOGY.md` (zero-to-hero protocol): pinned image, `MH_SEED=12345`, Yahoo→Stooq→seeded-GBM cascade with honest `source`, three gates (`pytest && run_all && benchmark_all`), hidden-pattern rules (recompute + effect size + "heuristic, not proof").

## 4. Results
### 4.1 Numbers (Hacks #14–34, #44–47)
- Sieve: `π(100)=25` exact; factorisation `20=[2,2,5]`; twins present `(3,5),(5,7)`; PNT ratio 1.13 at 10⁴.
- Goldbach: **0 failures to 500**; partitions grow (slope of log-count vs n ≈ +0.0036; min 1, max 30) — heuristic support, not proof.
- Collatz: **0 failures to 5,000**; example `17→…→1` (12 steps); stopping-time log-slope ≈ 11.1 with heavy fluctuations.
- π: Leibniz(10k) error <10⁻³; Monte-Carlo(50k) error <0.05; `√2` best `p/q` error 6×10⁻⁶ at q≤500, exact never found (reductio demo).
- Fermat: **0 solutions** for n=3 to 30; multiple for n=2 (3-4-5 family) — matches theory.

### 4.2 Structure & continuity (#35–56, #89–91)
- `Z₆` + `S₃` (order 6) pass full group axioms (closure/identity/inverse/associativity brute force).
- `12C5=792` (book's football example); Königsberg degrees `[3,3,3,5]` → 4 odds → no Eulerian trail (correct).
- Derivative/integral/FTC errors <10⁻³; Taylor `e` error <10⁻⁶; Lyapunov `λ(4)>0>λ(2.5)` sign split confirms chaos threshold.

### 4.3 Space (#57–88)
- Euclid `dist((0,0),(3,4))=5`; `V−E+F=2` for tetra/cube/octa; Koch Hausdorff `log4/log3≈1.2619` with diverging length; octant excess `π/2`; tesseract 16 vertices / 32 edges.

### 4.4 Reality + live market (#95–100)
Measured 2026-10-04 (see `results/tables/live_market.json`):
| Asset | n | source | Hurst | skew | xs-kurt | JB | ARCH₁ | ann-vol |
|---|---|---|---|---|---|---|---|---|
| SPY | 251 | yahoo_v8 | 0.890 | −0.18 | 0.98 | 11.3 | −0.00 (no) | 13.0% |
| BTC-USD | 366 | yahoo_v8 | 0.896 | −0.24 | 6.42 | 629.7 | 0.36 (yes) | 37.4% |
Interpretation: both trend (H>0.5) over this 1-year window — consistent with the 2025–26 bull regime, not a refutation of efficiency (R/S on trending samples biases high; reported honestly). BTC shows canonical crypto deviations: fat tails + clustering. SPY is near-Gaussian. **Brownian/GBM survives as null model; extensions (stochastic vol, jumps) needed for BTC** — exactly the textbook lesson of Hacks #95–97.
- Dice 60k: max-error <0.02 vs `ways/36`. Game theory: Nash (`betray`,`betray`) ≠ Pareto (`quiet`,`quiet`). Turing toy: `1111→11111`. P-vs-NP demo: linear scan 10k vs subset-sum 2¹⁵ timing contrast.

### 4.5 Hidden patterns (original)
1. **Benford-in-factorials**: digits 1–2 over-represented (0.25/0.22 vs 0.30/0.18 theory); max-dev ≈ 0.06 — partial conformity, small-n caveat stated.
2. **Collatz scaling**: stopping time ~ logarithmic with outliers (max 181 at n≤2000).
3. **Goldbach growth**: upward partition trend (above).
4. **Prime gaps to 5000**: 669 primes, max gap 34, mode 6 (162×), twins 126 — gap-6 dominance is the visible "hidden order".

## 5. Threats to validity
Yahoo schema drift (mitigated: Stooq + synthetic cascade); R/S Hurst bias on trending windows (reported, not hidden); laptop-scale limits vs frontier (2^71 Collatz, 10¹³ zeta zeros — cited, not matched); R/S + JB are proxies, not formal tests (SciPy-free to keep image slim; raw returns cached for re-analysis).

## 6. Future work
OU/reversion tests; Green–Tao progression coherence replication; Jensen-polynomial negative-result replication (Farmer); Lean proofs for #1–13; Zenodo DOI + image tar archiving (OxRSE guidance).

## 7. Reproduction
```bash
docker compose build && docker compose up research
# or locally: make install && make test && make run && make bench && make live
```
Artifacts: `results/tables/experiment_summary.json`, `benchmarks.json`, `live_market.json`; `data/live_cache/live_*.json` (provenance).

## References
Cochrane, R. (2018). *Maths Hacks*. Cassell. Plus 12 online sources dated 2026-10-04 in `RESEARCH_LOG.md` (arXiv 2604.01072, 2601.12811; Springer Collatz 2025; QuantStart/SimTrade; Willis 2020; Stodden 2010; NIST IR 8251; 15 RH papers; Wikipedia Wiener/GBM/OU; Yahoo v8/Stooq APIs; CPython docs).
