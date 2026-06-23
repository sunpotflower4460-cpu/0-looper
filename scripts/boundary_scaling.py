#!/usr/bin/env python3
"""Graph boundary scaling as an entropy-adjacent dimension meter.

Map 3 §5-1: for local d-dimensional geometries, region boundary scales as

    |boundary A| ~ |A|^((d-1)/d)

For a 2D lattice this exponent is 1/2. Small-world and random graphs have much
larger nonlocal boundary, connecting locality/area-law intuition to geometry.
"""
from __future__ import annotations

import argparse
import math
import random
from typing import List, Set


def slope(xs: list[float], ys: list[float]) -> float:
    X = [math.log(x) for x, y in zip(xs, ys) if x > 0 and y > 0]
    Y = [math.log(y) for x, y in zip(xs, ys) if x > 0 and y > 0]
    mx = sum(X) / len(X)
    my = sum(Y) / len(Y)
    den = sum((x - mx) ** 2 for x in X)
    return sum((x - mx) * (y - my) for x, y in zip(X, Y)) / den


def grid(L: int) -> list[set[int]]:
    N = L * L
    adj: list[set[int]] = [set() for _ in range(N)]

    def v(x: int, y: int) -> int:
        return (y % L) * L + (x % L)

    for y in range(L):
        for x in range(L):
            a = v(x, y)
            for dx, dy in [(1, 0), (0, 1)]:
                b = v(x + dx, y + dy)
                adj[a].add(b)
                adj[b].add(a)
    return adj


def add_shortcuts(adj: list[set[int]], count: int, seed: int) -> list[set[int]]:
    rng = random.Random(seed)
    N = len(adj)
    A = [set(s) for s in adj]
    for _ in range(count):
        a = rng.randrange(N)
        b = rng.randrange(N)
        if a != b:
            A[a].add(b)
            A[b].add(a)
    return A


def random_graph(N: int, deg: int, seed: int) -> list[set[int]]:
    rng = random.Random(seed)
    adj: list[set[int]] = [set() for _ in range(N)]
    for a in range(N):
        while len(adj[a]) < deg:
            b = rng.randrange(N)
            if a != b:
                adj[a].add(b)
                adj[b].add(a)
    return adj


def square_region(L: int, s: int) -> set[int]:
    return {y * L + x for y in range(s) for x in range(s)}


def boundary(adj: list[set[int]], A: set[int]) -> int:
    b = 0
    for u in A:
        for v in adj[u]:
            if v not in A:
                b += 1
    return b


def run(L: int, seed: int) -> None:
    base = grid(L)
    sw = add_shortcuts(base, L * L // 2, seed)
    rg = random_graph(L * L, 4, seed)
    print("| graph | exponent B~A^α | B at largest region | reading |")
    print("|---|---:|---:|---|")
    cases = [
        ("2D grid torus", base, "area-law boundary, d≈2"),
        ("2D grid + shortcuts", sw, "extra nonlocal boundary / abnormal"),
        ("random degree graph", rg, "bulk-like boundary, no local geometry"),
    ]
    for name, adj, reading in cases:
        areas: list[float] = []
        bs: list[float] = []
        for s in range(3, L // 2 + 1, 2):
            A = square_region(L, s)
            areas.append(float(len(A)))
            bs.append(float(boundary(adj, A)))
        alpha = slope(areas, bs)
        print(f"| {name} | {alpha:.2f} | {bs[-1]:.0f} | {reading} |")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--L", type=int, default=40)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    run(args.L, args.seed)


if __name__ == "__main__":
    main()
