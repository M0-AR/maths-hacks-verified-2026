"""Hacks #50-56, #89-91: continuity — derivatives, integrals, Taylor, chaos."""
from __future__ import annotations
import math


def derivative_numeric(f, x: float, h: float = 1e-6) -> float:
    return (f(x + h) - f(x - h)) / (2 * h)


def integral_trapezoid(f, a: float, b: float, n: int = 10_000) -> float:
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        s += f(a + i * h)
    return s * h


def taylor_exp(x: float, terms: int = 12) -> float:
    return sum(x ** k / math.factorial(k) for k in range(terms))


def taylor_sin(x: float, terms: int = 10) -> float:
    return sum(((-1) ** k) * x ** (2 * k + 1) / math.factorial(2 * k + 1) for k in range(terms))


def ftc_demo() -> dict:
    """FTC (#53): integrate f'=2t from 0..3 -> 9 = f(3)-f(0) for f=t^2."""
    fprime = lambda t: 2 * t
    area = integral_trapezoid(fprime, 0, 3, n=50_000)
    return {"integral_0_3_2t": area, "expected": 9.0, "abs_err": abs(area - 9.0)}


def logistic_bifurcation(r_vals, x0: float = 0.5, transient: int = 500, record: int = 100) -> dict:
    out = {}
    for r in r_vals:
        x = x0
        for _ in range(transient):
            x = r * x * (1 - x)
        pts = []
        for _ in range(record):
            x = r * x * (1 - x)
            pts.append(x)
        out[float(r)] = pts
    return out


def lyapunov_logistic(r: float, x0: float = 0.5, n: int = 5000) -> float:
    x = x0
    s = 0.0
    for _ in range(500):
        x = r * x * (1 - x)
    for _ in range(n):
        x = r * x * (1 - x)
        s += math.log(abs(r * (1 - 2 * x)) + 1e-300)
    return s / n


def collatz_sequence(n: int) -> list[int]:
    seq = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        seq.append(n)
    return seq
