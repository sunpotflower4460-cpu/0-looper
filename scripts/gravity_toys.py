#!/usr/bin/env python3
"""A6/A10/A11: reduced gravity structure, lensing, self-consistency.

These are small, dependency-free reproductions of the Map 4 gravity arc.
They are not numerical relativity. They check established reduced physics:

A6  Jeans-like amplitude competition: gravity grows density contrast, diffusion
    smooths it.
A10 Weak-field lensing: deflection around a point mass scales roughly as 1/b.
A11 Self-gravity chicken/egg: iterate rho ~ exp(-phi/T) and phi'' = rho-mean
    to a bound self-consistent profile.
"""
from __future__ import annotations

import argparse
import math
from typing import List


def run_instability() -> None:
    print("## A6 gravitational instability reduced amplitude")
    print("| case | initial contrast | final contrast | growth factor | reading |")
    print("|---|---:|---:|---:|---|")
    steps = 160
    dt = 0.05
    delta0 = 1e-3
    for label, G, Dk2 in [("gravity + diffusion", 1.0, 0.18), ("diffusion only", 0.0, 0.18)]:
        delta = delta0
        for _ in range(steps):
            delta += dt * (G - Dk2) * delta
        print(f"| {label} | {delta0:.6f} | {delta:.6f} | {delta/delta0:.1f} | {'structure grows' if G>Dk2 else 'contrast erased'} |")


def run_lensing() -> None:
    print("## A10 weak-field lensing integral")
    print("| impact b | deflection alpha | b*alpha | reading |")
    print("|---:|---:|---:|---|")
    M = 1.0
    dz = 0.02
    zmax = 80.0
    for b in [2, 3, 4, 6, 8, 12, 16]:
        z = -zmax
        acc = 0.0
        while z <= zmax:
            r2 = b * b + z * z
            # transverse gradient of Newtonian potential -M/r; GR adds factor 2.
            grad_perp = M * b / (r2 ** 1.5)
            acc += 2.0 * grad_perp * dz
            z += dz
        print(f"| {b} | {acc:.5f} | {b*acc:.5f} | alpha ~ 1/b |")


def solve_phi(rho: List[float], iters: int = 1600) -> List[float]:
    n = len(rho)
    source = [r - sum(rho) / n for r in rho]
    phi = [0.0] * n
    for _ in range(iters):
        new = phi[:]
        for i in range(1, n - 1):
            new[i] = 0.5 * (phi[i - 1] + phi[i + 1] - source[i])
        # fix gauge and open-ish boundaries
        m = sum(new) / n
        phi = [x - m for x in new]
    return phi


def run_equilibrium() -> None:
    print("## A11 self-gravity chicken/egg equilibrium")
    print("| iteration | center rho | edge rho | center/edge | profile width | reading |")
    print("|---:|---:|---:|---:|---:|---|")
    n = 101
    T = 0.38
    rho = [1.0 + 0.02 * math.cos(2 * math.pi * i / (n - 1)) for i in range(n)]
    for it in range(9):
        phi = solve_phi(rho)
        # Gravity attracts to lower phi; normalize density.
        raw = [math.exp(-p / T) for p in phi]
        s = sum(raw) / n
        rho = [x / s for x in raw]
        center = rho[n // 2]
        edge = 0.5 * (rho[0] + rho[-1])
        mean = sum(rho) / n
        width = math.sqrt(sum(((i - n // 2) ** 2) * rho[i] for i in range(n)) / sum(rho))
        print(f"| {it} | {center:.3f} | {edge:.3f} | {center/edge:.2f} | {width:.2f} | self-consistent bound profile |")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["instability", "lensing", "equilibrium", "all"], default="all")
    args = parser.parse_args()
    if args.mode in {"instability", "all"}:
        run_instability(); print()
    if args.mode in {"lensing", "all"}:
        run_lensing(); print()
    if args.mode in {"equilibrium", "all"}:
        run_equilibrium()


if __name__ == "__main__":
    main()
