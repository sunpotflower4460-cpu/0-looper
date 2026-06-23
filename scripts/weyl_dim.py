#!/usr/bin/env python3
"""Weyl-law spectral dimension checks.

For a d-dimensional grid Laplacian, Weyl scaling gives

    lambda_k ~ k^(2/d)

so the slope of log(lambda_k) vs log(k) is 2/d.

This script uses analytic path/grid eigenvalues, avoiding fragile dense solvers
for the baseline dimensional checks. Shortcut anomaly is included as a graph
ball-growth proxy rather than a claimed spectral calculation.
"""
from __future__ import annotations

import argparse
import math
import random
from collections import deque
from typing import List, Set


def slope(xs: List[float], ys: List[float]) -> float:
    pairs = [(x, y) for x, y in zip(xs, ys) if x > 0 and y > 0]
    X = [math.log(x) for x, _ in pairs]
    Y = [math.log(y) for _, y in pairs]
    mx = sum(X) / len(X)
    my = sum(Y) / len(Y)
    den = sum((x - mx) ** 2 for x in X)
    return sum((x - mx) * (y - my) for x, y in zip(X, Y)) / den


def path_eigs(L: int) -> List[float]:
    return [2.0 - 2.0 * math.cos(math.pi * k / L) for k in range(L)]


def grid_eigs(L: int, d: int) -> List[float]:
    one = path_eigs(L)
    vals = [0.0]
    for _ in range(d):
        vals = [v + e for v in vals for e in one]
    return sorted(vals)


def estimate(vals: List[float], kmin: int, kmax: int) -> tuple[float, float]:
    nz = [v for v in vals if v > 1e-12]
    kmax = min(kmax, len(nz) - 1)
    ks = list(range(kmin, kmax + 1))
    ys = [nz[k - 1] for k in ks]
    sl = slope([float(k) for k in ks], ys)
    return sl, 2.0 / sl


def run_lattice() -> None:
    print("## Weyl spectral dimension on path/grid Laplacians")
    print("| graph | vertices | fit k range | slope logλ/logk | d≈2/slope | reading |")
    print("|---|---:|---|---:|---:|---|")
    cases = [
        ("1D path", 256, 1, 10, 90),
        ("2D grid", 80, 2, 10, 1000),
        ("3D grid", 30, 3, 10, 5000),
    ]
    for name, L, d, kmin, kmax in cases:
        vals = grid_eigs(L, d)
        sl, dim = estimate(vals, kmin, kmax)
        print(f"| {name} | {L ** d} | {kmin}..{kmax} | {sl:.3f} | {dim:.2f} | integer-dimensional baseline |")


def run_shortcuts(seed: int = 0) -> None:
    # Graph-distance growth proxy for small-world anomaly, not a Laplacian eigensolver.
    L = 30
    N = L * L
    rng = random.Random(seed)
    adj: List[Set[int]] = [set() for _ in range(N)]

    def vid(x: int, y: int) -> int:
        return (y % L) * L + (x % L)

    for y in range(L):
        for x in range(L):
            a = vid(x, y)
            for dx, dy in [(1, 0), (0, 1)]:
                b = vid(x + dx, y + dy)
                adj[a].add(b)
                adj[b].add(a)
    for _ in range(N // 2):
        a = rng.randrange(N)
        b = rng.randrange(N)
        if a != b:
            adj[a].add(b)
            adj[b].add(a)

    rs: List[float] = []
    vols: List[float] = []
    for src in [0, N // 3, 2 * N // 3]:
        dist = [-1] * N
        dist[src] = 0
        q = deque([src])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if dist[v] < 0:
                    dist[v] = dist[u] + 1
                    q.append(v)
        for r in range(1, 6):
            rs.append(float(r))
            vols.append(float(sum(1 for d in dist if 0 <= d <= r)))
    sl = slope(rs, vols)
    print("\n## shortcut anomaly ball-growth proxy")
    print("| graph | growth slope logV/logr | reading |")
    print("|---|---:|---|")
    print(f"| 2D torus + random shortcuts | {sl:.2f} | abnormal / small-world-like growth, not clean 2D |")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["lattice", "shortcuts", "all"], default="all")
    args = parser.parse_args()
    if args.mode in {"lattice", "all"}:
        run_lattice()
    if args.mode in {"shortcuts", "all"}:
        run_shortcuts()


if __name__ == "__main__":
    main()
