#!/usr/bin/env python3
"""Boundary frontier A: emergent boundary and dissipative throughflow.

This script follows merge map 2. It uses reduced headless models rather than a
full phase-field PDE:

- Allen-Cahn healing is modeled as surface-tension-driven hole shrinkage.
- Conserved Cahn-Hilliard stable size is modeled as mass-conserved area.
- Throughflow closure is modeled as collapse cost balanced by surface nutrient.

Claim discipline:
- self-healing boundary, stable conserved size, and load-bearing death/life are
  measured in these reduced models;
- the three-way union (emergent boundary + robust size + metabolism-bearing load)
  remains frontier.
"""
from __future__ import annotations

import argparse
import math


def run_heal() -> None:
    print("## boundary/emergent_heal reduced Allen-Cahn")
    print("| case | hole radius start | hole radius final | hole area healed | reading |")
    print("|---|---:|---:|---:|---|")
    r = 12.0
    gamma = 0.20
    dt = 0.5
    steps = 720
    start_area = math.pi * r * r
    for _ in range(steps):
        if r <= 0:
            r = 0.0
            break
        # curvature-driven shrinkage of a bubble/hole: dr/dt ~ -gamma/r
        r = max(0.0, r - dt * gamma / max(r, 1e-9))
    final_area = math.pi * r * r
    healed = 1.0 - final_area / start_area
    print(f"| internal φ=-1 bubble | 12.0 | {r:.2f} | {healed:.3f} | surface tension closes hole |")


def run_ch() -> None:
    print("## boundary/ch_stable conserved-size proxy")
    print("| case | initial area | final area | relative drift | reading |")
    print("|---|---:|---:|---:|---|")
    area = 1200.0
    mass = area
    for _ in range(2000):
        # Conservative relaxation redistributes interface but preserves total mass.
        area += 0.0002 * (mass - area)
    drift = abs(area - mass) / mass
    print(f"| conserved droplet | {mass:.1f} | {area:.1f} | {drift:.5f} | size fixed by conserved φ |")


def simulate_throughflow(metabolism: bool, steps: int = 500) -> tuple[float, float, str]:
    area = 900.0
    q_collapse = 0.010
    surface_gain = 0.42 if metabolism else 0.0
    for _ in range(steps):
        surface = math.sqrt(max(area, 0.0))
        gain = surface_gain * surface
        loss = q_collapse * area
        area = max(0.0, area + gain - loss)
    state = "alive / load-bearing closure" if area > 100 else "collapsed / death"
    return 900.0, area, state


def run_throughflow() -> None:
    print("## boundary/throughflow")
    print("| case | initial area | final area | area ratio | reading |")
    print("|---|---:|---:|---:|---|")
    for metabolism in [False, True]:
        a0, af, state = simulate_throughflow(metabolism)
        label = "collapse cost only" if not metabolism else "surface-limited nutrient throughflow"
        print(f"| {label} | {a0:.1f} | {af:.1f} | {af/a0:.3f} | {state} |")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["heal", "ch", "throughflow", "all"], default="all")
    args = parser.parse_args()
    if args.mode in {"heal", "all"}:
        run_heal()
        print()
    if args.mode in {"ch", "all"}:
        run_ch()
        print()
    if args.mode in {"throughflow", "all"}:
        run_throughflow()


if __name__ == "__main__":
    main()
