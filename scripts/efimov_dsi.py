#!/usr/bin/env python3
"""DSI / Efimov-style geometric ladder check.

Reduced mechanism check for the sync note:
- scale-invariant inverse-square-like systems can produce discrete scale invariance;
- for g > 1/4, s0=sqrt(g-1/4), and the ladder ratio is exp(2*pi/s0);
- the anchor moves the whole ladder, while ratios stay fixed;
- below the critical point g <= 1/4, the ladder is absent.

This is formula-level known-physics reproduction, not a claim that the universe
itself is a spiral.
"""
from __future__ import annotations

import argparse
import math


def ladder(g: float, anchor: float, n: int) -> list[float]:
    if g <= 0.25:
        return []
    s0 = math.sqrt(g - 0.25)
    ratio = math.exp(2.0 * math.pi / s0)
    # Think of sizes/radii increasing geometrically. Energies would invert as r^-2.
    return [anchor * (ratio ** k) for k in range(n)]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--g", type=float, default=2.0)
    p.add_argument("--n", type=int, default=5)
    args = p.parse_args()

    print("## DSI ladder: critical on/off and anchor independence")
    print("| g | s0 | universal ratio exp(2π/s0) | anchor | first levels | measured ratios | reading |")
    print("|---:|---:|---:|---:|---|---|---|")
    for g in [0.20, 0.25, args.g]:
        if g <= 0.25:
            print(f"| {g:.3f} | - | - | 1.0 | none | none | below/at critical: no DSI ladder |")
            continue
        s0 = math.sqrt(g - 0.25)
        ratio = math.exp(2 * math.pi / s0)
        for anchor in [1.0, 3.0]:
            xs = ladder(g, anchor, args.n)
            rs = [xs[i + 1] / xs[i] for i in range(len(xs) - 1)]
            print(
                f"| {g:.3f} | {s0:.3f} | {ratio:.3f} | {anchor:.1f} | "
                + ", ".join(f"{x:.3g}" for x in xs[:4])
                + " | "
                + ", ".join(f"{r:.3f}" for r in rs[:3])
                + " | anchor shifts phase; ratio fixed |"
            )


if __name__ == "__main__":
    main()
