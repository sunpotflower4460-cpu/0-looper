#!/usr/bin/env python3
"""Curvature lives on faces / third.

For an equilateral triangular mesh around a vertex:

    curvature defect = 2π - deg * (π/3)

A 1D path cannot enclose a face, so it cannot detect curvature holonomy. This
script is a tiny combinatorial check of the 'third/face is irreducible' point.
"""
from __future__ import annotations

import math


def main() -> None:
    print("## angle deficit at a triangular-mesh vertex")
    print("| deg | angle sum | deficit | curvature sign | reading |")
    print("|---:|---:|---:|---|---|")
    for deg in [5, 6, 7]:
        angle_sum = deg * math.pi / 3.0
        deficit = 2.0 * math.pi - angle_sum
        sign = "positive" if deficit > 1e-9 else "flat" if abs(deficit) <= 1e-9 else "negative"
        reading = "missing wedge / cone" if sign == "positive" else "Euclidean flat" if sign == "flat" else "extra wedge / saddle-like"
        print(f"| {deg} | {angle_sum:.3f} | {deficit:.3f} | {sign} | {reading} |")

    print("\n## 1D path contrast")
    print("| object | closed face? | holonomy/deficit detectable? | reading |")
    print("|---|---|---|---|")
    print("| 1D path / edge relation | no | no | edges alone do not hold curvature |")
    print("| 2D face / triangle loop | yes | yes | curvature is read by going around a face |")


if __name__ == "__main__":
    main()
