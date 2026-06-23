#!/usr/bin/env python3
"""Torus triangulation flips: third/face keeps 2D manifold valid.

Map 3's key measured claim is that edge-only relation dynamics tends to string
or crumple, while a genuine 2-cell/third structure can keep a 2-manifold. This
script builds a triangular torus, performs Pachner 2-2 edge flips, and applies a
simple flatness action

    E = sum_v (deg(v) - 6)^2

with Metropolis temperature T. It measures degree variance and average graph
distance while checking that every edge is shared by exactly two triangles.
"""
from __future__ import annotations

import argparse
import random
import statistics
from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple

Tri = Tuple[int, int, int]
Edge = Tuple[int, int]


def tri(a: int, b: int, c: int) -> Tri:
    return tuple(sorted((a, b, c)))


def edges(t: Tri) -> list[Edge]:
    a, b, c = t
    return [tuple(sorted((a, b))), tuple(sorted((a, c))), tuple(sorted((b, c)))]


def build(L: int) -> set[Tri]:
    def v(x: int, y: int) -> int:
        return (y % L) * L + (x % L)

    T: set[Tri] = set()
    for y in range(L):
        for x in range(L):
            a = v(x, y)
            b = v(x + 1, y)
            c = v(x, y + 1)
            d = v(x + 1, y + 1)
            T.add(tri(a, b, c))
            T.add(tri(b, d, c))
    return T


def edge_faces(T: set[Tri]) -> Dict[Edge, List[Tri]]:
    out: Dict[Edge, List[Tri]] = defaultdict(list)
    for t in T:
        for e in edges(t):
            out[e].append(t)
    return out


def degrees(T: set[Tri], N: int) -> list[int]:
    adj = [set() for _ in range(N)]
    for t in T:
        for a, b in edges(t):
            adj[a].add(b)
            adj[b].add(a)
    return [len(a) for a in adj]


def energy(T: set[Tri], N: int) -> int:
    return sum((d - 6) ** 2 for d in degrees(T, N))


def manifold_ok(T: set[Tri]) -> bool:
    return all(len(fs) == 2 for fs in edge_faces(T).values())


def avg_dist(T: set[Tri], N: int, samples: int = 12) -> float:
    adj = [set() for _ in range(N)]
    for t in T:
        for a, b in edges(t):
            adj[a].add(b)
            adj[b].add(a)
    starts = list(range(0, N, max(1, N // samples)))[:samples]
    vals: list[int] = []
    for s in starts:
        d = [-1] * N
        d[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if d[v] < 0:
                    d[v] = d[u] + 1
                    q.append(v)
        vals += [x for x in d if x > 0]
    return sum(vals) / len(vals)


def try_flip(T: set[Tri], rng: random.Random) -> tuple[set[Tri], bool]:
    ef = edge_faces(T)
    candidates = [(e, fs) for e, fs in ef.items() if len(fs) == 2]
    rng.shuffle(candidates)
    for (a, b), fs in candidates:
        t1, t2 = fs
        x = list(set(t1) - {a, b})
        y = list(set(t2) - {a, b})
        if len(x) != 1 or len(y) != 1:
            continue
        x0 = x[0]
        y0 = y[0]
        if x0 == y0:
            continue
        newe = tuple(sorted((x0, y0)))
        if newe in ef:
            continue
        nt1 = tri(x0, y0, a)
        nt2 = tri(x0, y0, b)
        if nt1 in T or nt2 in T:
            continue
        NT = set(T)
        NT.remove(t1)
        NT.remove(t2)
        NT.add(nt1)
        NT.add(nt2)
        if manifold_ok(NT):
            return NT, True
    return T, False


def run(L: int, Ttemp: float, steps: int, seed: int) -> tuple[float, float, bool, int, int]:
    rng = random.Random(seed)
    N = L * L
    T = build(L)
    E = energy(T, N)
    accepted = 0
    for _ in range(steps):
        cand, ok = try_flip(T, rng)
        if not ok:
            continue
        Ec = energy(cand, N)
        dE = Ec - E
        if dE <= 0 or (Ttemp > 0 and rng.random() < pow(2.718281828, -dE / Ttemp)):
            T = cand
            E = Ec
            accepted += 1
    deg = degrees(T, N)
    var = statistics.pvariance(deg)
    dist = avg_dist(T, N)
    return var, dist, manifold_ok(T), accepted, E


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--L", type=int, default=8)
    parser.add_argument("--steps", type=int, default=300)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    print("| case | T | degree variance | average distance | manifold | accepted flips | E |")
    print("|---|---:|---:|---:|---|---:|---:|")
    for name, temp in [("seed flat", 0.0), ("low open T=5", 5.0), ("high open T=20", 20.0)]:
        var, dist, ok, acc, E = run(args.L, temp, args.steps, args.seed)
        print(f"| {name} | {temp:.1f} | {var:.2f} | {dist:.2f} | {ok} | {acc} | {E} |")


if __name__ == "__main__":
    main()
