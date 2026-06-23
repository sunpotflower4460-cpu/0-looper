#!/usr/bin/env python3
"""A5: entropic force and the limit of naive entropy for geometry.

A5a: A random-walk chain has no energetic preference among configurations, yet
counting endpoints gives an entropic spring: F=-ln P(R) ~ R^2/(2N).

A5b: Pure entropy in triangulation flips does not prefer flat geometry. Without
flatness action / curvature control, random flips increase degree variance and
shorten distances: the geometry crumples.
"""
from __future__ import annotations

import argparse
import math
import os
import sys
from math import comb

sys.path.append(os.path.dirname(__file__))
from triangulation_flip import build, try_flip, degrees, avg_dist  # type: ignore


def slope(xs, ys):
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    den = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den


def entropic_spring(N: int = 100, max_R: int = 50) -> None:
    data = []
    total = 2 ** N
    for R in range(0, max_R + 1, 2):
        k = (N + R) // 2
        p = comb(N, k) / total
        F = -math.log(p)
        data.append((R, R * R, F))
    F0 = data[0][2]
    xs = [float(r2) for _, r2, _ in data[1:]]
    ys = [F - F0 for _, _, F in data[1:]]
    sl = slope(xs, ys)
    print("## entropic spring from pure counting")
    print("| N steps | fit slope ΔF~s R² | theory 1/(2N) | reading |")
    print("|---:|---:|---:|---|")
    print(f"| {N} | {sl:.5f} | {1/(2*N):.5f} | force from counts, no assigned energy |")
    print("\n| R | density P(R) | ΔF=-lnP+lnP0 |")
    print("|---:|---:|---:|")
    for R, _, F in data[0:8]:
        k = (N + R) // 2
        p = comb(N, k) / total
        print(f"| {R} | {p:.6e} | {F - F0:.4f} |")


def random_flip_crumple(L: int = 14, seed: int = 0) -> None:
    import random
    import statistics

    rng = random.Random(seed)
    T = build(L)
    N = L * L
    checkpoints = [0, 500, 5000]
    print("## pure entropy random flips on triangulated torus")
    print("| flips | degree variance | average distance | reading |")
    print("|---:|---:|---:|---|")
    for step in range(max(checkpoints) + 1):
        if step in checkpoints:
            deg = degrees(T, N)
            var = statistics.pvariance(deg)
            dist = avg_dist(T, N)
            reading = "flat seed" if step == 0 else "entropy-only wandering / crumpling tendency"
            print(f"| {step} | {var:.2f} | {dist:.2f} | {reading} |")
        if step < max(checkpoints):
            T2, ok = try_flip(T, rng)
            if ok:
                T = T2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["spring", "flips", "all"], default="all")
    parser.add_argument("--N", type=int, default=100)
    parser.add_argument("--L", type=int, default=14)
    args = parser.parse_args()
    if args.mode in {"spring", "all"}:
        entropic_spring(args.N)
        print()
    if args.mode in {"flips", "all"}:
        random_flip_crumple(args.L)


if __name__ == "__main__":
    main()
