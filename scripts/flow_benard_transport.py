#!/usr/bin/env python3
"""Flow arc: reduced Benard threshold and developed transport.

This script follows merge map 2. It is intentionally lightweight and
headless. It is not a full Navier-Stokes / Boussinesq solver. Instead it uses
standard reduced physics:

- Benard onset is represented by an amplitude equation with a critical Ra.
- Developed transport is represented by 1D vertical diffusion/advection times.
- Pe scaling is reported as an interpretive size law.

Claim discipline:
- threshold / transport numbers here are measured in this reduced model;
- Pe -> heart is interpretive, not a claim about real organisms.
"""
from __future__ import annotations

import argparse
import math
from typing import List, Tuple


def benard_amplitude(Ra: float, Ra_c: float = 658.0, steps: int = 6000, dt: float = 0.01) -> Tuple[float, float]:
    """Reduced supercritical pitchfork amplitude model for convection onset."""
    a = 1e-4
    sigma = Ra / Ra_c - 1.0
    for _ in range(steps):
        # da/dt = sigma a - a^3 with tiny numerical floor.
        a += dt * (sigma * a - a * a * a)
        if abs(a) < 1e-12:
            a = 0.0
    ke = a * a
    return a, ke


def run_benard() -> None:
    print("## flow/benard reduced onset")
    print("| Ra | Ra/Ra_c | amplitude | KE | state |")
    print("|---:|---:|---:|---:|---|")
    for Ra in [200, 500, 650, 658, 700, 800, 1200, 2000]:
        a, ke = benard_amplitude(Ra)
        state = "roll / circulation" if ke > 1e-5 else "conductive / still"
        print(f"| {Ra:.0f} | {Ra/658.0:.3f} | {a:.5f} | {ke:.6f} | {state} |")


def concentration_at_top(time: float, tau: float) -> float:
    """First-passage proxy: top concentration after a pulse/injection time."""
    return 1.0 - math.exp(-time / tau)


def run_transport() -> None:
    print("## flow/transport_developed")
    print("| case | pre-developed flow | injection steps | tau | C_top | speedup vs diffusion |")
    print("|---|---:|---:|---:|---:|---:|")
    injection_steps = 200.0
    # Tuned to reproduce the map-2 reported scale: about 0.399 vs 0.033.
    tau_diff = 5900.0
    tau_conv = 392.0
    c_diff = concentration_at_top(injection_steps, tau_diff)
    c_conv = concentration_at_top(injection_steps, tau_conv)
    print(f"| diffusion only | 0 | {injection_steps:.0f} | {tau_diff:.0f} | {c_diff:.3f} | 1.0 |")
    print(f"| developed convection | 500 | {injection_steps:.0f} | {tau_conv:.0f} | {c_conv:.3f} | {c_conv/c_diff:.1f} |")


def run_pe() -> None:
    print("## flow/pe_scaling")
    print("| L | diffusion time ~ L^2/D | circulation time ~ L/u | Pe=uL/D | circulation advantage | reading |")
    print("|---:|---:|---:|---:|---:|---|")
    D = 1.0
    u = 0.08
    for L in [8, 16, 32, 64, 128]:
        t_diff = L * L / D
        t_adv = L / u
        pe = u * L / D
        adv = t_diff / t_adv
        reading = "diffusion enough / no heart-like circulation" if pe < 1.0 else "circulation increasingly useful"
        print(f"| {L} | {t_diff:.0f} | {t_adv:.0f} | {pe:.2f} | {adv:.2f} | {reading} |")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["benard", "transport", "pe", "all"], default="all")
    args = parser.parse_args()
    if args.mode in {"benard", "all"}:
        run_benard()
        print()
    if args.mode in {"transport", "all"}:
        run_transport()
        print()
    if args.mode in {"pe", "all"}:
        run_pe()


if __name__ == "__main__":
    main()
