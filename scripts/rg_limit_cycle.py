#!/usr/bin/env python3
"""Fixed point vs RG limit cycle / log-periodic fingerprint.

Reduced mechanism check:
- a fixed point has constant coupling across log scale;
- a limit cycle rotates in log(scale), giving a log-periodic modulation.

Claim discipline: measured toy flow, not a claim that the universe is a spiral.
"""
from __future__ import annotations

import argparse
import math


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--omega", type=float, default=2.0)
    p.add_argument("--steps", type=int, default=16)
    p.add_argument("--dtau", type=float, default=0.4)
    args = p.parse_args()

    print("## RG fixed point vs limit cycle")
    print("| tau=ln(scale) | fixed coupling | cycle x | cycle y | log-periodic observable | reading |")
    print("|---:|---:|---:|---:|---:|---|")
    r = 1.0
    theta = 0.0
    for i in range(args.steps + 1):
        tau = i * args.dtau
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        obs = 1.0 + 0.25 * math.cos(theta)
        print(f"| {tau:.2f} | 1.000 | {x:.3f} | {y:.3f} | {obs:.3f} | fixed = no choice; cycle = log-periodic fingerprint |")
        theta += args.omega * args.dtau
    period = 2 * math.pi / args.omega
    print(f"\nlog-scale period ΔlnL = {period:.3f}; preferred scale ratio = exp(period) = {math.exp(period):.3f}")


if __name__ == "__main__":
    main()
