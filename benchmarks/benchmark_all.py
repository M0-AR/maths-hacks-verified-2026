"""Benchmarks: timing + accuracy table for all major computations."""
from __future__ import annotations
import math
import time
from maths_hacks.utils import save_json, seed_all
from maths_hacks import numbers as N, calculus as C, algebra as A, stochastics as S


def timed(fn, *a, **k):
    t0 = time.perf_counter()
    r = fn(*a, **k)
    return r, time.perf_counter() - t0


def main() -> dict:
    seed_all()
    rows = []
    _, dt = timed(N.sieve, 100_000); rows.append({"task": "sieve_100k", "s": dt})
    _, dt = timed(N.verify_collatz, 5000); rows.append({"task": "collatz_5k", "s": dt})
    _, dt = timed(N.verify_goldbach, 500); rows.append({"task": "goldbach_500", "s": dt})
    _, dt = timed(N.pi_leibniz, 20_000); rows.append({"task": "pi_leibniz_20k", "s": dt})
    _, dt = timed(C.integral_trapezoid, lambda x: x*x, 0, 1); rows.append({"task": "integral_trap_10k", "s": dt})
    _, dt = timed(S.dice_distribution, 60_000); rows.append({"task": "dice_60k", "s": dt})
    _, dt = timed(A.symmetry_group_triangle); rows.append({"task": "S3_verify", "s": dt})
    _, dt = timed(C.lyapunov_logistic, 4.0); rows.append({"task": "lyapunov_5k", "s": dt})

    acc = {
        "pi_leibniz_10k_err": abs(N.pi_leibniz(10_000) - math.pi),
        "pi_mc_50k_err": abs(N.pi_monte_carlo(50_000) - math.pi),
        "integral_x2_err": abs(C.integral_trapezoid(lambda x: x*x, 0, 1) - 1/3),
        "deriv_t2_err": abs(C.derivative_numeric(lambda t: t*t, 1.0) - 2.0),
        "dice_max_err": S.dice_distribution(60_000)["max_abs_err"],
        "pnt_ratio_10k": N.prime_number_theorem_check(10_000)["ratio"],
    }
    out = {"timing_s": rows, "accuracy": acc,
           "machine_note": "Timings are relative (CI/ laptop comparable); accuracy asserts pass in tests."}
    save_json("benchmarks.json", out)
    print(f"benchmarks written: {len(rows)} timings")
    return out


if __name__ == "__main__":
    main()
