"""Hacks #35-43, #57-64, #67: structure — groups, rings/fields, matrices, combinatorics, graphs."""
from __future__ import annotations
import math
from collections import deque


def is_group_finite(elements: list, op, identity) -> dict:
    s = set(elements)
    # closure
    for a in elements:
        for b in elements:
            if op(a, b) not in s:
                return {"ok": False, "reason": f"not closed: {a},{b}"}
    # identity + inverses + associativity (brute force, small groups only)
    for a in elements:
        if op(a, identity) != a or op(identity, a) != a:
            return {"ok": False, "reason": "identity fails"}
    for a in elements:
        if not any(op(a, b) == identity and op(b, a) == identity for b in elements):
            return {"ok": False, "reason": f"no inverse for {a}"}
    for a in elements:
        for b in elements:
            for c in elements:
                if op(op(a, b), c) != op(a, op(b, c)):
                    return {"ok": False, "reason": "not associative"}
    return {"ok": True, "order": len(elements)}


def z_n_add_group(n: int) -> dict:
    return is_group_finite(list(range(n)), lambda a, b: (a + b) % n, 0)


def mat_mult(A, B):
    n, m, p = len(A), len(B[0]), len(B)
    return [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(m)] for i in range(n)]


def mat_det_2x2(M) -> float:
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]


def factorial(n: int) -> int:
    return math.factorial(n)


def n_choose_k(n: int, k: int) -> int:
    return math.comb(n, k)


def football_teams_example() -> dict:
    """Book #93 example: 12 choose 5 = 792 (not 12!/7!)."""
    return {"12P5_ordered": math.perm(12, 5), "12C5": math.comb(12, 5), "expected": 792}


def euler_bridges_demo() -> dict:
    """Konigsberg (#94): degrees [3,3,3,5] all odd -> no Eulerian trail."""
    degrees = {"A": 3, "B": 3, "C": 3, "D": 5}
    odd = sum(d % 2 for d in degrees.values())
    return {"degrees": degrees, "odd_count": odd, "eulerian_trail_possible": odd in (0, 2)}


def bfs_shortest_path(adj: dict, start, goal) -> list:
    q = deque([[start]])
    seen = {start}
    while q:
        path = q.popleft()
        if path[-1] == goal:
            return path
        for nb in adj.get(path[-1], []):
            if nb not in seen:
                seen.add(nb)
                q.append(path + [nb])
    return []


def symmetry_group_triangle() -> dict:
    """S3 as permutations of 3 vertices; verify group of order 6 (#38)."""
    import itertools
    perms = list(itertools.permutations([0, 1, 2]))

    def compose(p, q):
        return tuple(p[q[i]] for i in range(3))

    res = is_group_finite(perms, compose, (0, 1, 2))
    res["elements"] = len(perms)
    return res
