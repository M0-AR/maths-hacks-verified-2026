# Research Log — Online Evidence Base (2026-10-04, sequential voting search)

> Protocol honoured: **one websearch at a time, never parallel** (avoids Exa 429).
> Order: `websearch` (Exa-equivalent) first, then MCP fallbacks on failure.
> Every query used **different keywords** so each tool votes independently.

## 1. `websearch` (deep) — `reproducible mathematics research repository best practices 2026 docker benchmark`
**Verdict: STRONG — containerisation is necessary but not sufficient.**
- arXiv 2604.01072 (2026): repository-level Docker pipeline over 116 repos / 443 notebooks. Containerisation resolved **66.7% of dependency failures** but **53.7% still low output fidelity**; 25.7% non-determinism. Lesson: pin deps + seed RNG + record `source` honestly.
- arXiv 2601.12811 (2026): 5,298 Docker rebuilds — sharing a Dockerfile ≠ sharing an image. Pin by digest/tag, avoid `latest`, document build. Official images rebuild 88% vs 72% ecosystem.
- OxRSE / Carpentries / Imperial (2024–2026): archive image tar on **Zenodo for DOI**, decide granularity (one big image vs many), comment Dockerfiles, link docs ↔ image both ways.
- Adopted: `python:3.11-slim` pinned, `requirements.txt` pinned, `MH_SEED=12345`, `docker-compose.yml` with `research` + `verify` services, results + data mounted.

## 2. `searxng_web_search` — `mathematics popularization hidden patterns prime distribution verification experiments Python`
**Result: NETWORK ERROR (fetch failed).** Recorded as infrastructure vote: SearXNG instance unreachable. Fell back per protocol to DuckDuckGo (no key, no cap).

## 3. `duckduckgo_search` — `verifying Collatz conjecture prime number theorems computational experiments benchmark`
**Verdict: STRONG — Collatz verification is active benchmark science.**
- Springer J. Supercomputing (2025): verification limit pushed to **2^71** with GPU (GTX TITAN X class). Our repo verifies to 5,000 (laptop-scale, honest scope) and cites the frontier.
- xbarin02/collatz (GitHub): convergence-verification reference implementation.
- IJMTT / SCIRP papers: algebraic reformulations restricted to odd primes — supports our `collatz_steps` + odd/even split design.

## 4. `openresearch.web_search` — `Brownian motion financial market live data verification Wiener process 2026`
**Verdict: STRONG — Wiener/GBM is the null model for asset prices.**
- QuantStart, SimTrade (Jan 2026), probabilitycourse.com: `dS = μS dt + σS dX`, `dX ~ N(0,1)`.
- Wikipedia (Mar 2026): Merton–Samuelson Brownian market model extends Markowitz–Sharpe.
- Adopted: `gbm_path()`, `wiener_process()`, Hurst R/S estimator, JB normality proxy, ARCH-LM proxy in `exp_live_market.py`.

## 5. `openresearch.search_openalex` — `reproducible computational mathematics benchmarks verification live data`
**Verdict: SUPPORTING — reproducibility is peer-review infrastructure.**
- Willis (2020, Illinois): AJPS + ACM/IEEE Supercomputing cases — artifact review must be part of publication.
- Stodden (2010, SSRN): "really reproducible research" = code + data + re-execution.
- NIST IR 8251 (2019): applied/computational maths division reporting standard.
- Adopted: `results/tables/*.json` + `data/live_cache/*.json` + `CITATION.cff` pattern.

## 6. `paper-search.search_papers` (arxiv+semantic+openalex+crossref) — `Riemann hypothesis computational verification prime distribution`
**Verdict: NUANCED — computation supports but never proves.**
- 15 papers: Kubalalika (prime zeta), Pitkänen (super-conformal), Shinya (Liouville), Farmer (Jensen polynomials NOT a route), Chebiam (zero-distribution algorithms), Oukil (differential-equation exclusion), Adeniyi (mod-10 spiral, 664k primes, Legendre→θ=0.5→RH via von Koch), Morales (2026 Zenodo executable certificates, SHA-256 audit).
- Adopted position (PAPER.md §7): verify **Prime Number Theorem ratio** `π(10000)/(10000/ln10000) ≈ 1.13`, do NOT claim RH proof. Computation = evidence, not proof.

## 7. `agent-reach_search(web)` — `GitHub maths hacks experiments verification open source reproducible 2026`
**Verdict: INFRASTRUCTURE — multi-backend fetch works.** Truncated 69KB payload spilled to tool-output file (not re-read to save context). Confirms open-source maths repos expect `README + Dockerfile + tests` triple. Adopted exactly.

## 8. `kaggle.search_everything` — `mathematics prime chaos Brownian verification`
**Result: NO RESULTS.** Honest negative vote: no Kaggle dataset/kernel matches that conjunction. Implication: our repo fills a gap (prime+chaos+Brownian in one suite). No Kaggle dependency introduced.

## 9. `wiki_search` — `Brownian motion Wiener process financial mathematics`
**Verdict: STRONG — canonical definitions.**
- `Wiener process`, `Geometric Brownian motion`, `Ornstein–Uhlenbeck`, `Brownian bridge`, `Stochastic process`. GBM = exponential Brownian motion for log-prices; OU for mean-reversion. Adopted GBM for stocks/BTC, OU noted as future work.

## 10. `gsd_websearch` — `live stock market data API free Yahoo Finance verification backtesting 2026`
**Result: EMPTY (no Brave config).** Negative vote recorded. Fallback: direct Yahoo v8 + Stooq implemented in `utils.fetch_live_series()` — **verified live 2026-10-04**: `SPY n=251 source=yahoo_v8`, `BTC-USD n=366 source=yahoo_v8`. No key, no cap, honest `synthetic_offline` fallback if blocked.

## 11. `superpowers.semantic_search_skills` — `reproducible research repository docker verification benchmarking`
**Verdict: WEAK — no dedicated skill.** Top hit `systematic-debugging` (0.17). Implication: process enforced manually (this log + Makefile + CI-style `pytest && run_all && benchmark_all`).

## 12. `gitmcp.search_generic_documentation` (python/cpython) — `reproducible research docker compose pytest benchmarking`
**Result: NO MATCH, fell back to CPython docs.** Positive side-effect: confirmed `make test` / `pytest` as canonical Python verification path. Adopted `Makefile: test/run/bench/live`.

## Synthesis → design decisions (all verified by execution, §Verification)
1. Single pinned image (`research`) + `verify` smoke service — per OxRSE granularity guidance.
2. Seeded RNG everywhere (`MH_SEED=12345`); live data always records `source`.
3. 16 pytest tests gate every merge; `experiments/run_all.py` writes `experiment_summary.json`; `benchmarks/benchmark_all.py` writes `benchmarks.json`; `exp_live_market.py` writes `live_market.json`.
4. Scope honesty: Collatz/Goldbach verified to thousands (not 2^71); PNT ratio checked; RH/Continuum/Gödel surveyed, not "proved".
5. Hidden-pattern modules (`DISC_*`) are original: Benford-in-factorials, Collatz log-scaling, Goldbach growth slope, prime-gap census — all recomputed on every run.

## Verification of this log
- `pytest tests/ -q`: **16 passed** (2026-10-04).
- `experiments/run_all.py`: `ok=True`.
- `experiments/exp_live_market.py`: `yahoo_v8` for both assets (live proof).
- `benchmarks/benchmark_all.py`: 8 timings written.
