#!/usr/bin/env python3
"""Self-consistent graph <-> spectral coordinate remeshing loop.

Map 3 frames the chicken/egg relation as a self-consistency problem:

    graph -> spectral coordinates -> geometric kNN graph -> repeat

This script shows the qualitative floor:
- naive remeshing can improve briefly, then fragment/collapse;
- connected remeshing stabilizes, but tends toward string-like fixed points.

This is not a proof about all local rules. It is a small mechanism check for
the remeshing loop described in the map.
"""
from __future__ import annotations

import argparse
import math
import random
from collections import deque
from typing import List, Set, Tuple


def jacobi(A: List[List[float]], max_sweeps: int = 5000, eps: float = 1e-10) -> tuple[List[float], List[List[float]]]:
    n = len(A)
    a = [row[:] for row in A]
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(max_sweeps):
        p = q = 0
        m = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > m:
                    m = abs(a[i][j])
                    p = i
                    q = j
        if m < eps:
            break
        theta = 0.5 * math.atan2(2.0 * a[p][q], a[q][q] - a[p][p])
        c = math.cos(theta)
        s = math.sin(theta)
        app = c * c * a[p][p] - 2.0 * s * c * a[p][q] + s * s * a[q][q]
        aqq = s * s * a[p][p] + 2.0 * s * c * a[p][q] + c * c * a[q][q]
        a[p][q] = a[q][p] = 0.0
        a[p][p] = app
        a[q][q] = aqq
        for k in range(n):
            if k != p and k != q:
                akp = a[k][p]
                akq = a[k][q]
                a[k][p] = a[p][k] = c * akp - s * akq
                a[k][q] = a[q][k] = s * akp + c * akq
        for k in range(n):
            vkp = V[k][p]
            vkq = V[k][q]
            V[k][p] = c * vkp - s * vkq
            V[k][q] = s * vkp + c * vkq
    vals = [a[i][i] for i in range(n)]
    order = sorted(range(n), key=lambda i: vals[i])
    return [vals[i] for i in order], [[V[r][i] for i in order] for r in range(n)]


def laplacian(adj: List[Set[int]]) -> List[List[float]]:
    n = len(adj)
    L = [[0.0] * n for _ in range(n)]
    for i, neis in enumerate(adj):
        L[i][i] = float(len(neis))
        for j in neis:
            L[i][j] -= 1.0
    return L


def spectral_xy(adj: List[Set[int]]) -> tuple[List[tuple[float, float]], float]:
    vals, V = jacobi(laplacian(adj))
    return [(V[i][1], V[i][2]) for i in range(len(adj))], vals[1]


def random_graph(n: int, k: int, seed: int) -> List[Set[int]]:
    rng = random.Random(seed)
    adj: List[Set[int]] = [set() for _ in range(n)]
    for i in range(n):
        while len(adj[i]) < k:
            j = rng.randrange(n)
            if i != j:
                adj[i].add(j)
                adj[j].add(i)
    return adj


def knn(coords: List[tuple[float, float]], k: int, connected: bool = False) -> List[Set[int]]:
    n = len(coords)
    adj: List[Set[int]] = [set() for _ in range(n)]
    pairs: List[tuple[float, int, int]] = []
    for i in range(n):
        ds: List[tuple[float, int]] = []
        xi, yi = coords[i]
        for j in range(n):
            if i == j:
                continue
            xj, yj = coords[j]
            ds.append(((xi - xj) ** 2 + (yi - yj) ** 2, j))
        ds.sort()
        for _, j in ds[:k]:
            adj[i].add(j)
            adj[j].add(i)
        if connected:
            for d, j in ds:
                pairs.append((d, i, j))
    if connected:
        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        pairs.sort()
        for _, i, j in pairs:
            ri = find(i)
            rj = find(j)
            if ri != rj:
                parent[ri] = rj
                adj[i].add(j)
                adj[j].add(i)
    return adj


def comps(adj: List[Set[int]]) -> List[int]:
    n = len(adj)
    seen = [False] * n
    sizes: List[int] = []
    for i in range(n):
        if seen[i]:
            continue
        q = [i]
        seen[i] = True
        c = 0
        while q:
            u = q.pop()
            c += 1
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    q.append(v)
        sizes.append(c)
    return sizes


def avg_dist(adj: List[Set[int]]) -> float:
    n = len(adj)
    starts = list(range(0, n, max(1, n // 8)))[:8]
    vals: List[int] = []
    for s in starts:
        d = [-1] * n
        d[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if d[v] < 0:
                    d[v] = d[u] + 1
                    q.append(v)
        vals += [x for x in d if x > 0]
    return sum(vals) / len(vals) if vals else float("inf")


def run(stabilize: bool, seed: int, n: int, k: int, iters: int) -> list[tuple[int, int, int, float, float]]:
    adj = random_graph(n, k, seed)
    rows = []
    for t in range(iters + 1):
        cs = comps(adj)
        coords, lam2 = spectral_xy(adj)
        rows.append((t, len(cs), max(cs), avg_dist(adj), lam2))
        if t < iters:
            adj = knn(coords, k, connected=stabilize)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=60)
    parser.add_argument("--k", type=int, default=4)
    parser.add_argument("--iters", type=int, default=4)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    print("| loop | mode | components | largest comp | avg dist | lambda2 | reading |")
    print("|---:|---|---:|---:|---:|---:|---|")
    for mode, stabilize in [("naive", False), ("connected", True)]:
        for t, c, lc, dist, lam2 in run(stabilize, args.seed, args.n, args.k, args.iters):
            reading = "may fragment/collapse" if not stabilize else "stable fixed point, often string-like"
            print(f"| {t} | {mode} | {c} | {lc} | {dist:.2f} | {lam2:.4f} | {reading} |")


if __name__ == "__main__":
    main()
