#!/usr/bin/env python3
"""A1/A1b: XY/TDGL-like vortex dynamics and quench coarsening.

This is a lightweight phase-only relaxation model:

    theta_t += eta * sum_neighbors sin(theta_neighbor - theta)

It is not a full complex Ginzburg-Landau solver, but it captures the basic XY
energy descent. It measures:
- controlled +- pair attraction / annihilation tendency;
- controlled ++ pair repulsion tendency;
- random quench creates balanced + and - vortices and relaxation reduces them.

Claim discipline: measured toy check / XY analogy, not real particle physics.
"""
from __future__ import annotations

import argparse
import math
import random
from typing import List, Tuple

Grid = List[List[float]]


def wrap(a: float) -> float:
    while a <= -math.pi:
        a += 2.0 * math.pi
    while a > math.pi:
        a -= 2.0 * math.pi
    return a


def energy(theta: Grid) -> float:
    L = len(theta)
    e = 0.0
    for y in range(L):
        for x in range(L):
            for dx, dy in [(1, 0), (0, 1)]:
                d = wrap(theta[(y + dy) % L][(x + dx) % L] - theta[y][x])
                e += 1.0 - math.cos(d)
    return e


def relax(theta: Grid, steps: int, eta: float = 0.12) -> Grid:
    L = len(theta)
    th = [row[:] for row in theta]
    for _ in range(steps):
        nt = [row[:] for row in th]
        for y in range(L):
            for x in range(L):
                force = 0.0
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    force += math.sin(th[(y + dy) % L][(x + dx) % L] - th[y][x])
                nt[y][x] = wrap(th[y][x] + eta * force)
        th = nt
    return th


def vortices(theta: Grid) -> list[tuple[int, int, int]]:
    L = len(theta)
    out: list[tuple[int, int, int]] = []
    for y in range(L):
        for x in range(L):
            pts = [(x, y), ((x + 1) % L, y), ((x + 1) % L, (y + 1) % L), (x, (y + 1) % L)]
            s = 0.0
            for i in range(4):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % 4]
                s += wrap(theta[y1][x1] - theta[y0][x0])
            q = round(s / (2.0 * math.pi))
            if q:
                out.append((x, y, q))
    return out


def make_pair(L: int, sep: float, charges: tuple[int, int]) -> Grid:
    y0 = L / 2.0
    x1 = L / 2.0 - sep / 2.0
    x2 = L / 2.0 + sep / 2.0
    q1, q2 = charges
    return [[wrap(q1 * math.atan2(y - y0, x - x1) + q2 * math.atan2(y - y0, x - x2)) for x in range(L)] for y in range(L)]


def defect_distance(vs: list[tuple[int, int, int]], target: str) -> float:
    if target == "+-":
        A = [(x, y) for x, y, q in vs if q > 0]
        B = [(x, y) for x, y, q in vs if q < 0]
    else:
        A = [(x, y) for x, y, q in vs if q > 0]
        B = A[1:]
        A = A[:1]
    if not A or not B:
        return 0.0
    return min(math.hypot(ax - bx, ay - by) for ax, ay in A for bx, by in B)


def run_controlled(L: int, steps: int) -> None:
    print("## controlled vortex pairs")
    print("| pair | initial defects | final defects | initial distance | final distance | initial E | final E | reading |")
    print("|---|---:|---:|---:|---:|---:|---:|---|")
    for label, charges in [("+-", (1, -1)), ("++", (1, 1))]:
        th0 = make_pair(L, L / 3, charges)
        v0 = vortices(th0)
        e0 = energy(th0)
        th1 = relax(th0, steps)
        v1 = vortices(th1)
        e1 = energy(th1)
        d0 = defect_distance(v0, label)
        d1 = defect_distance(v1, label)
        reading = "+- annihilates / attracts" if label == "+-" else "like charges do not annihilate; repulsion/escape tendency"
        print(f"| {label} | {len(v0)} | {len(v1)} | {d0:.2f} | {d1:.2f} | {e0:.2f} | {e1:.2f} | {reading} |")


def run_quench(L: int, steps: int, seed: int) -> None:
    rng = random.Random(seed)
    th0 = [[rng.uniform(-math.pi, math.pi) for _ in range(L)] for _ in range(L)]
    checkpoints = [0, steps // 4, steps // 2, steps]
    th = th0
    print("## random quench coarsening")
    print("| step | + defects | - defects | net charge | total defects | energy | reading |")
    print("|---:|---:|---:|---:|---:|---:|---|")
    for s in range(steps + 1):
        if s in checkpoints:
            vs = vortices(th)
            plus = sum(1 for *_, q in vs if q > 0)
            minus = sum(1 for *_, q in vs if q < 0)
            print(f"| {s} | {plus} | {minus} | {plus-minus} | {len(vs)} | {energy(th):.2f} | topology balances net charge; relaxation removes pairs |")
        if s < steps:
            th = relax(th, 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["controlled", "quench", "all"], default="all")
    parser.add_argument("--L", type=int, default=48)
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    if args.mode in {"controlled", "all"}:
        run_controlled(args.L, args.steps)
        print()
    if args.mode in {"quench", "all"}:
        run_quench(args.L, args.steps, args.seed)


if __name__ == "__main__":
    main()
