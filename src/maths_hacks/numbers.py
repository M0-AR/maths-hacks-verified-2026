"""Hacks #14-34, #44-47: numbers — primes, Collatz, Goldbach, pi, irrationals."""
from __future__ import annotations
import math


def sieve(n: int) -> list[int]:
    if n < 2:
        return []
    is_p = bytearray(b"\x01") * (n + 1)
    is_p[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if is_p[i]:
            is_p[i*i:n+1:i] = b"\x00" * len(range(i*i, n+1, i))
    return [i for i, v in enumerate(is_p) if v]


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(n ** 0.5)
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return False
    return True


def prime_factorization(n: int) -> list[int]:
    out = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        out.append(n)
    return out


def twin_primes(limit: int) -> list[tuple[int, int]]:
    ps = set(sieve(limit + 2))
    return [(p, p + 2) for p in sorted(ps) if p + 2 in ps]


def goldbach_partitions(even_n: int, primes_set: set[int] | None = None) -> list[tuple[int, int]]:
    assert even_n % 2 == 0 and even_n > 2
    if primes_set is None:
        primes_set = set(sieve(even_n))
    return [(p, even_n - p) for p in sorted(primes_set) if p <= even_n // 2 and (even_n - p) in primes_set]


def verify_goldbach(limit: int) -> dict:
    primes = set(sieve(limit))
    fails, counts = [], {}
    for e in range(4, limit + 1, 2):
        parts = goldbach_partitions(e, primes)
        counts[e] = len(parts)
        if not parts:
            fails.append(e)
    return {"limit": limit, "fails": fails, "counts": counts, "ok": not fails}


def collatz_steps(n: int) -> int:
    c = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        c += 1
        if c > 100_000:
            raise RuntimeError("Collatz runaway")
    return c


def verify_collatz(limit: int) -> dict:
    max_steps, argmax, fails = -1, -1, []
    for n in range(1, limit + 1):
        try:
            s = collatz_steps(n)
        except RuntimeError:
            fails.append(n)
            continue
        if s > max_steps:
            max_steps, argmax = s, n
    return {"limit": limit, "fails": fails, "max_steps": max_steps, "argmax": argmax, "ok": not fails}


def pi_leibniz(terms: int) -> float:
    return 4.0 * sum((-1) ** k / (2 * k + 1) for k in range(terms))


def pi_monte_carlo(n: int, seed: int = 12345) -> float:
    import random
    rnd = random.Random(seed)
    inside = 0
    for _ in range(n):
        if rnd.random() ** 2 + rnd.random() ** 2 <= 1.0:
            inside += 1
    return 4.0 * inside / n


def sqrt2_irrational_demo(denom_limit: int = 1000) -> dict:
    """Reductio demo (#25): no p/q with q<=limit squares to exactly 2."""
    best = (1, 1, abs(1 - 2))
    for q in range(1, denom_limit + 1):
        p = round(math.sqrt(2) * q)
        for pp in (p - 1, p, p + 1):
            if pp <= 0:
                continue
            err = abs((pp / q) ** 2 - 2)
            if err < best[2]:
                best = (pp, q, err)
    return {"best_p": best[0], "best_q": best[1], "best_err": best[2], "exact_found": best[2] == 0.0}


def prime_number_theorem_check(x: int) -> dict:
    """Compare pi(x) with x/ln(x) (#17/#47 context)."""
    c = len(sieve(x))
    approx = x / math.log(x)
    return {"x": x, "pi_x": c, "x_over_lnx": approx, "ratio": c / approx if approx else None}


def fermat_search(limit: int, n: int) -> list[tuple[int, int, int]]:
    """Brute-force search for x^n+y^n=z^n (expect none for n>2, #45)."""
    sols = []
    powers = {i: i ** n for i in range(1, limit + 1)}
    power_set = set(powers.values())
    for x in range(1, limit + 1):
        for y in range(x, limit + 1):
            if powers[x] + powers[y] in power_set:
                z = round((powers[x] + powers[y]) ** (1.0 / n))
                if z <= limit and z ** n == powers[x] + powers[y]:
                    sols.append((x, y, z))
    return sols
