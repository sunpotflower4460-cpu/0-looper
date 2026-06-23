#!/usr/bin/env python3
"""Gravity as key: unscreenable, equivalence principle, universality.

Reduced known-physics checks for the sync note:
1. Single-sign mass cannot be neutralized like charge.
2. A uniform gravitational field is removable by free fall; tidal gradients are not.
3. Acceleration a=GM/r^2 is independent of test mass.

The music/key analogy is interpretive; these checks are standard mechanics.
"""
from __future__ import annotations

import math


def main() -> None:
    print("## gravity as key: three structural checks")
    print("| check | input | output | reading |")
    print("|---|---|---|---|")

    masses = [1, 2, 3, 5]
    charges = [1, -1, 2, -2]
    print(f"| single sign / no shielding | masses={masses} | net mass={sum(masses)} | positive source accumulates; no neutral region |")
    print(f"| charge contrast | charges={charges} | net charge={sum(charges)} | opposite signs can screen/cancel |")

    g0 = 9.8
    sep = 1.0
    tidal = 0.02
    uniform_rel = (g0 - g0) * sep
    tidal_rel = ((g0 + tidal * sep) - g0)
    print(f"| equivalence principle / transposition | uniform g={g0} | relative acceleration={uniform_rel:.3f} | free fall removes uniform field |")
    print(f"| curvature / tide | dg/dx={tidal} | relative acceleration={tidal_rel:.3f} | tidal field remains physical |")

    G = 1.0
    M = 10.0
    r = 5.0
    accs = []
    for m in [0.1, 1.0, 10.0, 100.0]:
        F = G * M * m / (r * r)
        a = F / m
        accs.append(a)
    print(f"| universality | test masses=0.1,1,10,100 | accelerations={', '.join(f'{a:.3f}' for a in accs)} | m cancels; all fall alike |")


if __name__ == "__main__":
    main()
