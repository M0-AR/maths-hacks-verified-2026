"""Hacks #59-88: space — Euclid, Euler characteristic, fractals, curvature demos."""
from __future__ import annotations
import math


def euclid_dist(p, q) -> float:
    return math.dist(p, q)


def euler_characteristic(v: int, e: int, f: int) -> int:
    return v - e + f


def known_euler() -> dict:
    return {
        "tetrahedron": euler_characteristic(4, 6, 4),
        "cube": euler_characteristic(8, 12, 6),
        "octahedron": euler_characteristic(6, 12, 8),
        "torus_min": 0,  # V-E+F for standard torus triangulation
        "sphere_expected": 2,
    }


def koch_snowflake_points(iterations: int) -> list[tuple[float, float]]:
    pts = [(0.0, 0.0), (1.0, 0.0)]
    for _ in range(iterations):
        new = [pts[0]]
        for i in range(len(pts) - 1):
            x0, y0 = pts[i]
            x1, y1 = pts[i + 1]
            dx, dy = (x1 - x0) / 3, (y1 - y0) / 3
            p1 = (x0 + dx, y0 + dy)
            p3 = (x0 + 2 * dx, y0 + 2 * dy)
            # peak of equilateral bump
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            nx, ny = -(y1 - y0), (x1 - x0)
            norm = math.hypot(nx, ny) or 1.0
            h = math.hypot(dx, dy) * math.sqrt(3)
            p2 = (mx - nx / norm * h / 3 * 0 + ( -dy * math.sqrt(3) / 3), my + (dx * math.sqrt(3) / 3))
            # Simpler robust peak:
            ang = math.atan2(dy, dx) + math.pi / 3
            seg = math.hypot(dx, dy)
            p2 = (p1[0] + seg * math.cos(ang), p1[1] + seg * math.sin(ang))
            new += [p1, p2, p3, (x1, y1)]
        pts = new
    return pts


def koch_length(iterations: int) -> float:
    return (4 / 3) ** iterations  # unit segment grows without bound


def cantor_set_intervals(iterations: int) -> list[tuple[float, float]]:
    segs = [(0.0, 1.0)]
    for _ in range(iterations):
        out = []
        for a, b in segs:
            third = (b - a) / 3
            out += [(a, a + third), (b - third, b)]
        segs = out
    return segs


def box_counting_dimension_koch(samples: int = 4) -> dict:
    # Theoretical Hausdorff dim of Koch curve = log4/log3 ≈ 1.2619
    theory = math.log(4) / math.log(3)
    lengths = [koch_length(i) for i in range(samples)]
    return {"theory": theory, "lengths": lengths, "diverges": lengths[-1] > lengths[0]}


def sphere_vs_plane_triangle_angle_sum() -> dict:
    """Flat triangle sums to pi; spherical excess demo (unit octant = 3*pi/2)."""
    return {"euclidean_sum": math.pi, "octant_sum": 3 * math.pi / 2, "excess": math.pi / 2}


def tesseract_vertices() -> list[tuple[int, int, int, int]]:
    return [(x, y, z, w) for x in (0, 1) for y in (0, 1) for z in (0, 1) for w in (0, 1)]


def tesseract_projected_edges() -> int:
    # 4-cube has 32 edges; perspective projection preserves count
    return 32
