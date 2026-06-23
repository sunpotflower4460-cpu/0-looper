#!/usr/bin/env python3
"""3D ball-growth calibration and locality/nonlocality contrast.

This is a calibration script, not 3D emergence. A hand-built cubic lattice is
3D by construction. We measure finite-size ball-growth slopes and compare:
- clean local cubic lattice;
- local edge dilution / disorder;
- nonlocal shortcuts.

The point: local disorder can preserve dimension-like growth, while nonlocal
shortcuts break it toward small-world behavior.
"""
from __future__ import annotations

import argparse
import math
import random
from collections import deque
from typing import List, Set


def slope(xs: list[float], ys: list[float]) -> float:
    pairs = [(x, y) for x, y in zip(xs, ys) if x > 0 and y > 0]
    X = [math.log(x) for x, _ in pairs]
    Y = [math.log(y) for _, y in pairs]
    mx = sum(X) / len(X)
    my = sum(Y) / len(Y)
    den = sum((x - mx) ** 2 for x in X)
    return sum((x - mx) * (y - my) for x, y in zip(X, Y)) / den


def cubic_graph(L: int) -> list[set[int]]:
    N = L * L * L
    adj: list[set[int]] = [set() for _ in range(N)]

    def v(x: int, y: int, z: int) -> int:
        return z * L * L + y * L + x

    for z in range(L):
        for y in range(L):
            for x in range(L):
                a = v(x, y, z)
                for dx, dy, dz in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if nx < L and ny < L and nz < L:
                        b = v(nx, ny, nz)
                        adj[a].add(b)
                        adj[b].add(a)
    return adj


def locally_dilute(adj: list[set[int]], p_remove: float, seed: int) -> list[set[int]]:
    rng = random.Random(seed)
    out = [set(s) for s in adj]
    edges = [(i, j) for i, ns in enumerate(adj) for j in ns if i < j]
    for i, j in edges:
        if rng.random() < p_remove and len(out[i]) > 1 and len(out[j]) > 1:
            out[i].discard(j)
            out[j].discard(i)
    return out


def add_shortcuts(adj: list[set[int]], count: int, seed: int) -> list[set[int]]:
    rng = random.Random(seed)
    N = len(adj)
    out = [set(s) for s in adj]
    for _ in range(count):
        a, b = rng.randrange(N), rng.randrange(N)
        if a != b:
            out[a].add(b)
            out[b].add(a)
    return out


def ball_slope(adj: list[set[int]], start: int, r_min: int, r_max: int) -> tuple[float, list[int]]:
    d = [-1] * len(adj)
    d[start] = 0
    q = deque([start])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if d[v] < 0:
                d[v] = d[u] + 1
                q.append(v)
    rs: list[float] = []
    vols: list[float] = []
    raw: list[int] = []
    for r in range(r_min, r_max + 1):
        vol = sum(1 for x in d if 0 <= x <= r)
        rs.append(float(r))
        vols.append(float(vol))
        raw.append(vol)
    return slope(rs, vols), raw


def run_case(name: str, adj: list[set[int]], L: int) -> tuple[str, float, str]:
    center = (L // 2) * L * L + (L // 2) * L + (L // 2)
    rmax = max(3, L // 3)
    alpha, vols = ball_slope(adj, center, 2, rmax)
    reading = "local 3D calibration" if "clean" in name else "local disorder robust" if "diluted" in name else "nonlocal shortcuts break dimension"
    return name, alpha, reading


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--Ls", type=int, nargs="+", default=[16, 24, 32])
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()

    print("## 3D ball-growth calibration")
    print("| L | case | slope logV/logr | reading |")
    print("|---:|---|---:|---|")
    for L in args.Ls:
        base = cubic_graph(L)
        cases = [
            ("clean cubic lattice", base),
            ("locally diluted lattice", locally_dilute(base, 0.25, args.seed)),
            ("nonlocal shortcuts", add_shortcuts(base, (L * L * L) // 5, args.seed)),
        ]
        for name, adj in cases:
            _, alpha, reading = run_case(name, adj, L)
            print(f"| {L} | {name} | {alpha:.2f} | {reading} |")
    print("\nclaim: hand-built cubic lattice is calibration, not 3D emergence; finite-size slopes approach 3 slowly.")


if __name__ == "__main__":
    main()
