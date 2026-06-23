#!/usr/bin/env python3
"""A4: defect / matter bends graph metric.

A conical triangular-lattice toy is built by gluing m triangular sectors around a
center. m=6 is flat triangular lattice, m=5 is a positive disclination
(+ curvature / missing wedge), and m=7 is a negative disclination
(extra wedge). We do not assign an external Euclidean metric; we measure
circumference and area using graph distance from the defect center.

This is a reduced combinatorial check of: defect -> curvature -> changed metric.
"""
from __future__ import annotations

import argparse
from collections import deque
from typing import Dict, List, Set, Tuple


def build_cone(sectors: int, R: int) -> tuple[list[set[int]], dict[tuple[int, int], int]]:
    idx: dict[tuple[int, int], int] = {(0, 0): 0}
    nodes: list[tuple[int, int]] = [(0, 0)]
    for r in range(1, R + 1):
        for i in range(sectors * r):
            idx[(r, i)] = len(nodes)
            nodes.append((r, i))
    adj: list[set[int]] = [set() for _ in nodes]

    def add(a: int, b: int) -> None:
        if a != b:
            adj[a].add(b)
            adj[b].add(a)

    for r in range(1, R + 1):
        n = sectors * r
        # ring edges
        for i in range(n):
            add(idx[(r, i)], idx[(r, (i + 1) % n)])
        # radial edges to previous ring. These make the graph a cone made of sectors.
        if r == 1:
            for i in range(n):
                add(0, idx[(r, i)])
        else:
            prev_n = sectors * (r - 1)
            for i in range(n):
                p0 = (i * prev_n) // n
                p1 = ((i + 1) * prev_n) // n
                add(idx[(r, i)], idx[(r - 1, p0 % prev_n)])
                add(idx[(r, i)], idx[(r - 1, p1 % prev_n)])
    return adj, idx


def spheres(adj: list[set[int]], max_r: int) -> tuple[list[int], list[int]]:
    d = [-1] * len(adj)
    d[0] = 0
    q = deque([0])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if d[v] < 0:
                d[v] = d[u] + 1
                q.append(v)
    circumference = [sum(1 for x in d if x == r) for r in range(1, max_r + 1)]
    area = [sum(1 for x in d if 0 <= x <= r) for r in range(1, max_r + 1)]
    return circumference, area


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--R", type=int, default=9)
    args = parser.parse_args()
    cases = [("positive defect deg5 / missing wedge", 5), ("flat deg6", 6), ("negative defect deg7 / extra wedge", 7)]
    print("## graph-distance circumference around a defect")
    print("| case | sectors | r=1 | r=2 | r=3 | r=4 | r=5 | r=6 | r=7 | r=8 | r=9 | reading |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for name, sectors in cases:
        adj, _ = build_cone(sectors, args.R)
        c, _ = spheres(adj, args.R)
        reading = "less circumference / positive curvature" if sectors < 6 else "flat" if sectors == 6 else "extra circumference / negative curvature"
        vals = c + [0] * max(0, 9 - len(c))
        print(f"| {name} | {sectors} | " + " | ".join(str(vals[i]) for i in range(9)) + f" | {reading} |")
    print("\n## graph-distance area around a defect")
    print("| case | sectors | area r=3 | area r=6 | area r=9 | reading |")
    print("|---|---:|---:|---:|---:|---|")
    for name, sectors in cases:
        adj, _ = build_cone(sectors, args.R)
        _, a = spheres(adj, args.R)
        reading = "smaller than flat" if sectors < 6 else "flat" if sectors == 6 else "larger than flat"
        print(f"| {name} | {sectors} | {a[2]} | {a[5]} | {a[8]} | {reading} |")


if __name__ == "__main__":
    main()
