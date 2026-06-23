#!/usr/bin/env python3
"""Optional minimal Model-H-like vessel check.

Map 2 F1 asks for a flowing boundary cell: phase-separated membrane carried by
internal circulation. This is a deliberately reduced amplitude model:

- internal KE is driven by buoyancy inside the boundary and damped outside;
- Allen-Cahn-like membrane area shrinks under curvature;
- integrity remains one connected object unless flow stress exceeds tension.

Claim discipline:
- coexistence of circulation + coherent boundary is measured in this reduced toy;
- stable flowing cell is frontier.
"""
from __future__ import annotations

import argparse


def run_model(steps: int = 600) -> None:
    area = 1.0
    ke = 0.0
    tension = 1.0
    broken = False
    for _ in range(steps):
        drive = 0.040 * area
        damping = 0.006 * ke
        nonlinear = 0.0000009 * ke * ke
        ke = max(0.0, ke + drive - damping - nonlinear)
        flow_stress = 0.00008 * ke
        area = max(0.0, area - 0.00095 * area - 0.00004 * flow_stress)
        if flow_stress > tension:
            broken = True
    print("| steps | internal KE | area ratio | shrink percent | integrity | claim |")
    print("|---:|---:|---:|---:|---|---|")
    integrity = "coherent single boundary" if not broken else "broken"
    print(f"| {steps} | {ke:.1f} | {area:.3f} | {(1-area)*100:.1f}% | {integrity} | coexistence measured, stable size frontier |")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=600)
    args = parser.parse_args()
    run_model(args.steps)


if __name__ == "__main__":
    main()
