#!/usr/bin/env python3
"""Spectral coordinates: position as wrapped low eigenmodes.

Map 3 asks for a small spectral toolbox:
- ring eigenmodes as winding phase / octave doubling;
- 2D grid low Laplacian eigenvectors as smooth coordinate axes.

Dependency-free: uses a small dense Jacobi eigensolver. This is fine for the
small CI checks here; for entanglement entropy use numpy/scipy instead.
"""
from __future__ import annotations

import argparse
import math
from typing import List, Tuple

Matrix = List[List[float]]


def jacobi_eigh(A: Matrix, max_sweeps: int = 10000, eps: float = 1e-12) -> Tuple[List[float], Matrix]:
    n = len(A)
    a = [row[:] for row in A]
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(max_sweeps):
        p = q = 0
        m = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                v = abs(a[i][j])
                if v > m:
                    m = v
                    p = i
                    q = j
        if m < eps:
            break
        theta = 0.5 * math.atan2(2.0 * a[p][q], a[q][q] - a[p][p])
        c = math.cos(theta)
        s = math.sin(theta)
        app = c * c * a[p][p] - 2.0 * s * c * a[p][q] + s * s * a[q][q]
        aqq = s * s * a[p][p] + 2.0 * s * c * a[p][q] + c * c * a[q][q]
        a[p][q] = a[q][p] = 0.0
        a[p][p] = app
        a[q][q] = aqq
        for k in range(n):
            if k != p and k != q:
                akp = a[k][p]
                akq = a[k][q]
                a[k][p] = a[p][k] = c * akp - s * akq
                a[k][q] = a[q][k] = s * akp + c * akq
        for k in range(n):
            vkp = V[k][p]
            vkq = V[k][q]
            V[k][p] = c * vkp - s * vkq
            V[k][q] = s * vkp + c * vkq
    vals = [a[i][i] for i in range(n)]
    order = sorted(range(n), key=lambda i: vals[i])
    return [vals[i] for i in order], [[V[r][i] for i in order] for r in range(n)]


def grid_laplacian(L: int) -> Matrix:
    n = L * L
    A = [[0.0] * n for _ in range(n)]

    def vid(x: int, y: int) -> int:
        return y * L + x

    for y in range(L):
        for x in range(L):
            i = vid(x, y)
            deg = 0
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx = x + dx
                ny = y + dy
                if 0 <= nx < L and 0 <= ny < L:
                    j = vid(nx, ny)
                    A[i][j] -= 1.0
                    deg += 1
            A[i][i] = float(deg)
    return A


def corr(a: List[float], b: List[float]) -> float:
    ma = sum(a) / len(a)
    mb = sum(b) / len(b)
    aa = [x - ma for x in a]
    bb = [x - mb for x in b]
    da = math.sqrt(sum(x * x for x in aa))
    db = math.sqrt(sum(x * x for x in bb))
    return sum(x * y for x, y in zip(aa, bb)) / (da * db) if da and db else 0.0


def ring_modes(N: int = 32) -> None:
    print("## ring modes as wrapped phase")
    print("| k | winding | wavelength | octave from k=1 | first phases |")
    print("|---:|---:|---:|---:|---|")
    for k in [0, 1, 2, 4, 8]:
        phases = [(2.0 * math.pi * k * j / N) % (2.0 * math.pi) for j in range(6)]
        octave = "-" if k == 0 else f"{math.log2(k):.0f}"
        wavelength = "∞" if k == 0 else f"{N / k:.1f}"
        print(f"| {k} | {k} | {wavelength} | {octave} | {', '.join(f'{p:.2f}' for p in phases)} |")


def grid_coords(L: int = 8) -> None:
    print("## spectral coordinates on 2D open grid")
    vals, V = jacobi_eigh(grid_laplacian(L))
    xs = [x for y in range(L) for x in range(L)]
    ys = [y for y in range(L) for x in range(L)]
    print("| mode | eigenvalue | corr x | corr y | coordinate reading |")
    print("|---:|---:|---:|---:|---|")
    for mode in range(1, 6):
        v = [V[i][mode] for i in range(L * L)]
        cx = abs(corr(v, xs))
        cy = abs(corr(v, ys))
        reading = "smooth coordinate axis" if max(cx, cy) > 0.85 else "higher / mixed mode"
        print(f"| v{mode + 1} | {vals[mode]:.6f} | {cx:.3f} | {cy:.3f} | {reading} |")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["ring", "grid", "all"], default="all")
    parser.add_argument("--L", type=int, default=8)
    parser.add_argument("--N", type=int, default=32)
    args = parser.parse_args()
    if args.mode in {"ring", "all"}:
        ring_modes(args.N)
        print()
    if args.mode in {"grid", "all"}:
        grid_coords(args.L)


if __name__ == "__main__":
    main()
