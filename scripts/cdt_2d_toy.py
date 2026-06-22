#!/usr/bin/env python3
"""2D causal dynamical triangulation toy.

This ports the Claude-provided Node.js CDT toy into dependency-free Python.

Track:
    space <- causality

The model builds a causal strip triangulation:
- time slices are 1D spatial rings;
- adjacent slices are connected by causal up/down triangles;
- time is periodic;
- 2D gravity action is not used because in 2D the Einstein-Hilbert term is
  topological, so the point of this toy is to isolate the causal layering.

Null:
    Break causality by rewiring a fraction of edges to random distant nodes.
    Diameter shrinks and estimated dimensions rise toward small-world behavior.

Claim discipline:
    This is a known CDT-style toy / reproduction, not a claim of real spacetime.
"""

from __future__ import annotations

import argparse
import math
from collections import deque
from typing import Iterable, List, Set, Tuple


class LCG:
    def __init__(self, seed: int):
        self.s = seed & 0xFFFFFFFF

    def rnd(self) -> float:
        self.s = (self.s * 1664525 + 1013904223) & 0xFFFFFFFF
        return self.s / 4294967296.0


def js_round(x: float) -> int:
    return math.floor(x + 0.5)


def sign(x: int) -> int:
    return 1 if x > 0 else -1 if x < 0 else 0


def add_edge(adj: List[Set[int]], a: int, b: int) -> None:
    if a == b:
        return
    adj[a].add(b)
    adj[b].add(a)


def build_cdt(T: int, baseN: int, fluct: int, seed: int) -> Tuple[List[List[int]], List[int]]:
    """Build a 2D causal strip triangulation as an undirected graph."""
    rng = LCG(seed)
    minN = 8
    sizes = [baseN] * T
    for i in range(1, T):
        d = js_round((rng.rnd() * 2 - 1) * fluct)
        if rng.rnd() < 0.3:
            d -= sign(sizes[i - 1] - baseN)
        sizes[i] = max(minN, sizes[i - 1] + d)

    offset = [0] * (T + 1)
    for i in range(T):
        offset[i + 1] = offset[i] + sizes[i]
    Nv = offset[T]
    adj: List[Set[int]] = [set() for _ in range(Nv)]

    def vid(i: int, k: int) -> int:
        i %= T
        return offset[i] + (k % sizes[i])

    # Spacelike ring edges.
    for i in range(T):
        for k in range(sizes[i]):
            add_edge(adj, vid(i, k), vid(i, k + 1))

    # Causal strips between adjacent time slices.
    for i in range(T):
        j = (i + 1) % T
        ni, nj = sizes[i], sizes[j]
        seq = [True] * ni + [False] * nj
        for x in range(len(seq) - 1, 0, -1):
            y = int(rng.rnd() * (x + 1))
            seq[x], seq[y] = seq[y], seq[x]

        a = b = 0
        for down in seq:
            if down:
                add_edge(adj, vid(i, a), vid(j, b))
                add_edge(adj, vid(i, a + 1), vid(j, b))
                a += 1
            else:
                add_edge(adj, vid(j, b), vid(i, a))
                add_edge(adj, vid(j, b + 1), vid(i, a))
                b += 1

        if a != ni or b != nj:
            raise RuntimeError(f"Invalid strip closure at slice {i}: a={a}/{ni}, b={b}/{nj}")

    return [sorted(x) for x in adj], sizes


def break_causality(adj: List[List[int]], f: float, seed: int) -> List[List[int]]:
    rng = LCG(seed)
    N = len(adj)
    A = [set(x) for x in adj]

    for u in range(N):
        for v in list(A[u]):
            if v > u and rng.rnd() < f:
                A[u].discard(v)
                A[v].discard(u)
                w = u
                attempts = 0
                while (w == u or w in A[u]) and attempts < N * 4:
                    w = int(rng.rnd() * N)
                    attempts += 1
                if w != u and w not in A[u]:
                    A[u].add(w)
                    A[w].add(u)

    return [sorted(x) for x in A]


def bfs_dist(adj: List[List[int]], src: int) -> List[int]:
    N = len(adj)
    dist = [-1] * N
    dist[src] = 0
    q = deque([src])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] < 0:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def farthest(adj: List[List[int]], src: int) -> Tuple[int, int]:
    dist = bfs_dist(adj, src)
    far = max(range(len(adj)), key=lambda i: dist[i])
    return far, dist[far]


def diameter_double_sweep(adj: List[List[int]], seed: int) -> int:
    rng = LCG(seed)
    src = int(rng.rnd() * len(adj))
    a, _ = farthest(adj, src)
    _, d = farthest(adj, a)
    return d


def bfs_ball(adj: List[List[int]], src: int) -> List[int]:
    dist = bfs_dist(adj, src)
    maxd = max(dist)
    counts = [0] * (maxd + 1)
    for d in dist:
        if d >= 0:
            counts[d] += 1
    cum = []
    total = 0
    for c in counts:
        total += c
        cum.append(total)
    return cum


def ball_dim(adj: List[List[int]], n_src: int = 12, seed: int = 0) -> float:
    N = len(adj)
    rng = LCG(seed)
    acc: List[float] = []
    for _ in range(n_src):
        src = int(rng.rnd() * N)
        c = bfs_ball(adj, src)
        if len(acc) < len(c):
            acc.extend([acc[-1] if acc else 0.0] * (len(c) - len(acc)))
        last = c[-1]
        for r in range(len(acc)):
            acc[r] += c[r] if r < len(c) else last
    acc = [x / n_src for x in acc]

    lo, hi = N * 0.03, N * 0.30
    r1 = r2 = -1
    for r in range(1, len(acc)):
        if acc[r] >= lo and r1 < 0:
            r1 = r
        if acc[r] <= hi:
            r2 = r
    if r1 < 1 or r2 <= r1:
        return float("nan")
    return (math.log(acc[r2]) - math.log(acc[r1])) / (math.log(r2) - math.log(r1))


def spectral_dim(adj: List[List[int]], n_src: int = 8, seed: int = 0, t1: int = 6, t2: int = 30) -> float:
    N = len(adj)
    rng = LCG(seed)
    dims = []
    for _ in range(n_src):
        src = int(rng.rnd() * N)
        p = [0.0] * N
        p[src] = 1.0
        P = []
        for _t in range(t2 + 1):
            P.append(p[src])
            np = [0.0] * N
            for i, pi in enumerate(p):
                if pi == 0.0:
                    continue
                dg = len(adj[i]) or 1
                np[i] += 0.5 * pi
                mv = 0.5 * pi / dg
                for k in adj[i]:
                    np[k] += mv
            p = np
        if P[t1] > 0 and P[t2] > 0:
            dims.append(-2 * (math.log(P[t2]) - math.log(P[t1])) / (math.log(t2) - math.log(t1)))
    return sum(dims) / len(dims) if dims else float("nan")


def slope(xs: Iterable[float], ys: Iterable[float]) -> float:
    X = [math.log(x) for x in xs]
    Y = [math.log(y) for y in ys]
    n = len(X)
    sx, sy = sum(X), sum(Y)
    sxx = sum(x * x for x in X)
    sxy = sum(x * y for x, y in zip(X, Y))
    denom = n * sxx - sx * sx
    return (n * sxy - sx * sy) / denom if denom else float("nan")


def run_sizes(sides: List[int], fluct: int, seed: int, n_src: int) -> None:
    Ns, diams = [], []
    print("| side | vertices | diameter | ball dim | spectral dim | avg degree |")
    print("|---:|---:|---:|---:|---:|---:|")
    for idx, side in enumerate(sides):
        adj, sizes = build_cdt(side, side, fluct, seed + idx * 1009)
        N = len(adj)
        d = diameter_double_sweep(adj, seed + idx * 2003)
        bd = ball_dim(adj, n_src=n_src, seed=seed + idx * 3001)
        sd = spectral_dim(adj, n_src=max(4, n_src // 2), seed=seed + idx * 4001)
        deg = sum(len(x) for x in adj) / N
        Ns.append(N)
        diams.append(d)
        print(f"| {side} | {N} | {d} | {bd:.2f} | {sd:.2f} | {deg:.2f} |")
    sl = slope(Ns, diams)
    print(f"\ndiameter_slope = {sl:.3f}")
    print(f"diameter_dimension = {1/sl:.2f}")


def run_rewire(side: int, fluct: int, seed: int, n_src: int) -> None:
    base, _ = build_cdt(side, side, fluct, seed)
    print("| rewiring f | vertices | diameter | ball dim | spectral dim | avg degree |")
    print("|---:|---:|---:|---:|---:|---:|")
    for idx, f in enumerate([0.0, 0.05, 0.15, 0.30]):
        adj = base if f == 0.0 else break_causality(base, f, seed + idx * 5555)
        N = len(adj)
        d = diameter_double_sweep(adj, seed + idx * 211)
        bd = ball_dim(adj, n_src=n_src, seed=seed + idx * 313)
        sd = spectral_dim(adj, n_src=max(4, n_src // 2), seed=seed + idx * 419)
        deg = sum(len(x) for x in adj) / N
        print(f"| {f:.2f} | {N} | {d} | {bd:.2f} | {sd:.2f} | {deg:.2f} |")


def run_fluct(side: int, seed: int, n_src: int) -> None:
    print("| fluct | vertices | diameter | ball dim | spectral dim | avg degree |")
    print("|---:|---:|---:|---:|---:|---:|")
    for idx, fluct in enumerate([2, 5, 8, 12]):
        adj, _ = build_cdt(side, side, fluct, seed + idx * 777)
        N = len(adj)
        d = diameter_double_sweep(adj, seed + idx * 991)
        bd = ball_dim(adj, n_src=n_src, seed=seed + idx * 1231)
        sd = spectral_dim(adj, n_src=max(4, n_src // 2), seed=seed + idx * 1871)
        deg = sum(len(x) for x in adj) / N
        print(f"| {fluct} | {N} | {d} | {bd:.2f} | {sd:.2f} | {deg:.2f} |")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["sizes", "rewire", "fluct", "all"], default="all")
    parser.add_argument("--seed", type=int, default=12345)
    parser.add_argument("--fluct", type=int, default=2)
    parser.add_argument("--side", type=int, default=40)
    parser.add_argument("--sources", type=int, default=12)
    args = parser.parse_args()

    if args.mode in ("sizes", "all"):
        print("## diameter / ball / spectral scaling")
        run_sizes([14, 20, 28, 40], args.fluct, args.seed, args.sources)
        print()
    if args.mode in ("rewire", "all"):
        print("## causality-breaking rewiring")
        run_rewire(args.side, args.fluct, args.seed, args.sources)
        print()
    if args.mode in ("fluct", "all"):
        print("## fluctuation robustness")
        run_fluct(args.side, args.seed, args.sources)


if __name__ == "__main__":
    main()
