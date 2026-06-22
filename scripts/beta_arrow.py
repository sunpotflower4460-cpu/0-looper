#!/usr/bin/env python3
from __future__ import annotations
import argparse, math, random, statistics, zlib


def entropy_binary_fraction(p: float) -> float:
    if p <= 0 or p >= 1:
        return 0.0
    return -p * math.log(p, 2) - (1 - p) * math.log(1 - p, 2)


def entropy_state(state):
    return entropy_binary_fraction(sum(1 for x in state if x > 0) / len(state))


def kac_step(state, markers):
    n = len(state)
    out = [0] * n
    for i, s in enumerate(state):
        out[(i + 1) % n] = -s if markers[i] else s
    return out


def kac_inverse_step(state, markers):
    n = len(state)
    old = [0] * n
    for i in range(n):
        old[i] = -state[(i + 1) % n] if markers[i] else state[(i + 1) % n]
    return old


def make_markers(n=200, marker_fraction=0.35, seed=0):
    rng = random.Random(seed)
    return [rng.random() < marker_fraction for _ in range(n)]


def make_state(n=200, plus_fraction=1.0, seed=1, shuffle=True):
    rng = random.Random(seed)
    n_plus = round(n * plus_fraction)
    state = [1] * n_plus + [-1] * (n - n_plus)
    if shuffle:
        rng.shuffle(state)
    return state


def kac_series(n=200, marker_fraction=0.35, plus_fraction=1.0, steps=400, seed=0):
    markers = make_markers(n, marker_fraction, seed)
    state = make_state(n, plus_fraction, seed + 999, shuffle=plus_fraction not in (0.0, 1.0))
    ent = []
    for _ in range(steps + 1):
        ent.append(entropy_state(state))
        state = kac_step(state, markers)
    return ent


def mode_kac():
    print("| initial | S(0) | max S | S(N/4) | S(N/2) | S(N) | S(2N) | reading |")
    print("|---|---:|---:|---:|---:|---:|---:|---|")
    n = 200
    for label, plus in [("low entropy all +", 1.0), ("high entropy random 50/50", 0.5)]:
        s = kac_series(n=n, plus_fraction=plus, steps=2 * n, seed=3)
        reading = "arrow + recurrence" if plus == 1.0 else "no strong arrow"
        print(f"| {label} | {s[0]:.3f} | {max(s):.3f} | {s[n//4]:.3f} | {s[n//2]:.3f} | {s[n]:.3f} | {s[2*n]:.3f} | {reading} |")


def mode_asym():
    print("| initial plus fraction | S(0) | max S | ΔS=max-S0 | reading |")
    print("|---:|---:|---:|---:|---|")
    for plus in [0.50, 0.51, 0.53, 0.55, 0.60, 0.70, 0.90, 1.00]:
        s = kac_series(n=400, plus_fraction=plus, steps=400, seed=7)
        ds = max(s) - s[0]
        reading = "equilibrium/no arrow" if abs(plus - 0.5) < 1e-9 else "continuous, no threshold"
        print(f"| {plus:.2f} | {s[0]:.5f} | {max(s):.5f} | {ds:.5f} | {reading} |")


def coarse_entropy(grid):
    L = len(grid)
    bins = [0] * 16
    for row in grid:
        for v in row:
            k = max(0, min(15, int(v * 15.999)))
            bins[k] += 1
    total = L * L
    return -sum((c / total) * math.log(c / total, 2) for c in bins if c)


def compressed_len(grid):
    raw = bytes(max(0, min(15, int(v * 15.999))) + 65 for row in grid for v in row)
    return len(zlib.compress(raw, 9))


def complexity_rows(L=64, steps=80):
    grid = [[0.0] * L for _ in range(L)]
    for y in range(L):
        for x in range(L):
            if (x - L * 0.35) ** 2 + (y - L * 0.5) ** 2 < (L * 0.16) ** 2:
                grid[y][x] = 1.0
    rows = []
    for t in range(steps + 1):
        rows.append((t, coarse_entropy(grid), compressed_len(grid)))
        # Arnold cat map + weak observational coarse-graining.
        ng = [[0.0] * L for _ in range(L)]
        for y in range(L):
            for x in range(L):
                nx = (x + y) % L
                ny = (x + 2 * y) % L
                ng[ny][nx] = grid[y][x]
        bg = [[0.0] * L for _ in range(L)]
        for y in range(L):
            for x in range(L):
                bg[y][x] = 0.82 * ng[y][x] + 0.045 * (ng[y][(x - 1) % L] + ng[y][(x + 1) % L] + ng[(y - 1) % L][x] + ng[(y + 1) % L][x])
        grid = bg
    return rows


def mode_complexity():
    rows = complexity_rows()
    peak = max(rows, key=lambda x: x[2])
    print("| point | step | coarse entropy | gzip bytes | reading |")
    print("|---|---:|---:|---:|---|")
    for label, row, reading in [
        ("start", rows[0], "ordered / simple"),
        ("complexity peak", peak, "filamented middle"),
        ("final", rows[-1], "coarse mixed / simple again"),
    ]:
        print(f"| {label} | {row[0]} | {row[1]:.3f} | {row[2]} | {reading} |")


def mode_twoarrow():
    n = 200
    markers = make_markers(n, 0.35, 3)
    forward = [1] * n
    backward = [1] * n
    rows = []
    for t in range(0, 101):
        rows.append((t, entropy_state(backward), entropy_state(forward)))
        forward = kac_step(forward, markers)
        backward = kac_inverse_step(backward, markers)
    print("| |t| | S(-t) | S(0) | S(+t) | reading |")
    print("|---:|---:|---:|---:|---|")
    s0 = rows[0][1]
    for t in [0, 25, 50, 100]:
        row = rows[t]
        print(f"| {t} | {row[1]:.3f} | {s0:.3f} | {row[2]:.3f} | entropy rises away from low-entropy boundary |")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["kac", "asym", "complexity", "twoarrow", "all"], default="all")
    args = ap.parse_args()
    if args.mode in ("kac", "all"):
        print("## Kac ring arrow / recurrence")
        mode_kac(); print()
    if args.mode in ("asym", "all"):
        print("## asymmetry scan")
        mode_asym(); print()
    if args.mode in ("complexity", "all"):
        print("## complexity window")
        mode_complexity(); print()
    if args.mode in ("twoarrow", "all"):
        print("## two-arrow low entropy boundary")
        mode_twoarrow()


if __name__ == "__main__":
    main()
