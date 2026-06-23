#!/usr/bin/env python3
"""A7: entropy-only crumpling vs causal/layered restriction.

This script complements entropy_action_frontier.py. It is not a full CDT Monte
Carlo. It compares:

- entropy-only random Pachner flips on an unconstrained triangulated torus;
- a layered causal triangulation proxy where edges/faces respect time slices.

The point is modest: unrestricted entropy tends to shorten distances / crumple,
while causal/layered restrictions keep extended distances. This is a reduced
mechanism check, not a derivation of the CDT action.
"""
from __future__ import annotations

import argparse
import os
import statistics
import sys
from collections import deque
from typing import List, Set, Tuple

sys.path.append(os.path.dirname(__file__))
from triangulation_flip import avg_dist, build, degrees, try_flip  # type: ignore


def layered_graph(space: int, time: int) -> list[set[int]]:
    N = space * time
    adj: list[set[int]] = [set() for _ in range(N)]

    def v(x: int, t: int) -> int:
        return (t % time) * space + (x % space)

    for t in range(time):
        for x in range(space):
            a = v(x, t)
            # spatial ring edge and causal next-slice edges
            for b in [v(x + 1, t), v(x, t + 1), v(x + 1, t + 1), v(x - 1, t + 1)]:
                adj[a].add(b)
                adj[b].add(a)
    return adj


def graph_avg_dist(adj: list[set[int]], samples: int = 12) -> float:
    n = len(adj)
    starts = list(range(0, n, max(1, n // samples)))[:samples]
    vals: list[int] = []
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
    return sum(vals) / len(vals)


def run_entropy_only(L: int, flips: int, seed: int) -> tuple[float, float, float]:
    import random

    rng = random.Random(seed)
    T = build(L)
    N = L * L
    for _ in range(flips):
        T2, ok = try_flip(T, rng)
        if ok:
            T = T2
    deg = degrees(T, N)
    return statistics.pvariance(deg), avg_dist(T, N), float(N)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--L", type=int, default=18)
    parser.add_argument("--flips", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    var0, dist0, N = run_entropy_only(args.L, 0, args.seed)
    var1, dist1, _ = run_entropy_only(args.L, args.flips, args.seed)
    layered = layered_graph(args.L, args.L)
    dist_layered = graph_avg_dist(layered)
    print("| case | vertices | degree variance | avg distance | reading |")
    print("|---|---:|---:|---:|---|")
    print(f"| flat triangulation seed | {int(N)} | {var0:.2f} | {dist0:.2f} | extended flat baseline |")
    print(f"| entropy-only random flips | {int(N)} | {var1:.2f} | {dist1:.2f} | crumpling / shortened distances |")
    print(f"| causal layered proxy | {len(layered)} | - | {dist_layered:.2f} | restriction keeps extended distance scale |")


if __name__ == "__main__":
    main()
