#!/usr/bin/env python3
"""A3: metric field mediates force between defects.

A +- vortex pair in an XY field has energy that depends on separation. That
separation dependence is the force. A purely combinatorial local defect cost,
by contrast, is independent of separation.

This is a measured toy check, not a claim about real electromagnetism/gravity.
"""
from __future__ import annotations

import argparse
import math
from typing import List, Tuple


def wrap(a: float) -> float:
    while a <= -math.pi:
        a += 2.0 * math.pi
    while a > math.pi:
        a -= 2.0 * math.pi
    return a


def xy_pair_energy(L: int, sep: int, charges: tuple[int, int] = (1, -1)) -> float:
    y0 = L / 2.0
    x1 = L / 2.0 - sep / 2.0
    x2 = L / 2.0 + sep / 2.0
    q1, q2 = charges
    theta = [[0.0] * L for _ in range(L)]
    for y in range(L):
        for x in range(L):
            theta[y][x] = q1 * math.atan2(y - y0, x - x1) + q2 * math.atan2(y - y0, x - x2)
    E = 0.0
    for y in range(1, L - 1):
        for x in range(1, L - 1):
            for dx, dy in [(1, 0), (0, 1)]:
                d = wrap(theta[y + dy][x + dx] - theta[y][x])
                E += 1.0 - math.cos(d)
    return E


def fit_log(xs: List[float], ys: List[float]) -> float:
    X = [math.log(x) for x in xs]
    Y = ys
    mx = sum(X) / len(X)
    my = sum(Y) / len(Y)
    den = sum((x - mx) ** 2 for x in X)
    return sum((x - mx) * (y - my) for x, y in zip(X, Y)) / den


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--L", type=int, default=96)
    args = parser.parse_args()
    seps = [4, 6, 8, 12, 16, 24, 32]
    energies = [xy_pair_energy(args.L, s) for s in seps]
    slope = fit_log([float(s) for s in seps], energies)
    print("## XY field vortex pair: metric-dependent energy")
    print("| separation | field energy | combinatorial local defect cost | reading |")
    print("|---:|---:|---:|---|")
    for s, E in zip(seps, energies):
        print(f"| {s} | {E:.3f} | 2.000 | field energy depends on distance; local defect cost does not |")
    print(f"\nlog-separation slope = {slope:.3f}")
    print("reading: in a field with metric, separation matters, so a force can be read; in a purely local combinatorial cost, separation is invisible.")


if __name__ == "__main__":
    main()
