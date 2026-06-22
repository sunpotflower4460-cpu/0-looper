#!/usr/bin/env python3
"""δ inheritance / marker experiments.

Track from the Claude convergence map:
    D. inheritance marker

This follows γ closure. A closed-loop Gray-Scott-like parent is settled first;
then it is split into two children. We test whether pattern and/or memory-marker
inheritance improves child persistence after stress.

Claim discipline:
This is not biological heredity, DNA, reproduction, or life. It is a toy test of
whether a self-produced marker/memory field can be inherited and affect
post-split persistence.
"""
from __future__ import annotations

import argparse
import math
import random
import statistics
from typing import Dict, List, Tuple

Grid = List[List[float]]


def zeros(n: int, value: float = 0.0) -> Grid:
    return [[value for _ in range(n)] for _ in range(n)]


def clone(a: Grid) -> Grid:
    return [row[:] for row in a]


def lap(a: Grid, x: int, y: int, n: int) -> float:
    return a[y][(x - 1) % n] + a[y][(x + 1) % n] + a[(y - 1) % n][x] + a[(y + 1) % n][x] - 4 * a[y][x]


def mass(a: Grid) -> float:
    return sum(sum(row) for row in a)


def cosine(a: Grid, b: Grid) -> float:
    n = len(a)
    dot = 0.0
    na = 0.0
    nb = 0.0
    for y in range(n):
        for x in range(n):
            av = a[y][x]
            bv = b[y][x]
            dot += av * bv
            na += av * av
            nb += bv * bv
    return dot / math.sqrt(na * nb) if na and nb else 0.0


def step(u: Grid, v: Grid, m: Grid, mode: str) -> Tuple[Grid, Grid, Grid]:
    n = len(u)
    nu = zeros(n)
    nv = zeros(n)
    nm = zeros(n)
    for y in range(n):
        for x in range(n):
            uu = u[y][x]
            vv = v[y][x]
            mm = max(0.0, min(1.0, m[y][x]))
            marker_active = mode in {"marker_only", "full_inheritance", "closed_parent"}
            if marker_active:
                d_v_eff = 0.08 * (1.0 - 0.70 * mm)
                k_eff = 0.060 * (1.0 - 0.45 * mm)
            else:
                d_v_eff = 0.08
                k_eff = 0.060

            reaction = uu * vv * vv
            nu[y][x] = min(1.2, max(0.0, uu + 0.16 * lap(u, x, y, n) - reaction + 0.037 * (1.0 - uu)))
            nv[y][x] = min(1.2, max(0.0, vv + d_v_eff * lap(v, x, y, n) + reaction - (0.037 + k_eff) * vv))
            nm[y][x] = min(1.0, max(0.0, m[y][x] + 0.05 * lap(m, x, y, n) + 0.02 * vv - 0.018 * m[y][x]))
    return nu, nv, nm


def make_parent(seed: int, n: int, settle: int) -> Tuple[Grid, Grid, Grid]:
    rng = random.Random(seed)
    u = zeros(n, 1.0)
    v = zeros(n, 0.0)
    m = zeros(n, 0.0)
    c = n // 2
    r = max(2, n // 9)
    for y in range(c - r, c + r):
        for x in range(c - r, c + r):
            u[y % n][x % n] = 0.5 + 0.02 * (rng.random() - 0.5)
            v[y % n][x % n] = 0.25 + 0.02 * (rng.random() - 0.5)
    for _ in range(settle):
        u, v, m = step(u, v, m, "closed_parent")
    return u, v, m


def extract_half(parent: Tuple[Grid, Grid, Grid], side: str) -> Tuple[Grid, Grid, Grid]:
    u, v, m = parent
    n = len(v)
    cu = zeros(n, 1.0)
    cv = zeros(n, 0.0)
    cm = zeros(n, 0.0)
    xs = range(0, n // 2) if side == "L" else range(n // 2, n)
    offset = n // 4
    for y in range(n):
        for i, x in enumerate(xs):
            tx = offset + i
            cu[y][tx] = u[y][x]
            cv[y][tx] = v[y][x]
            cm[y][tx] = m[y][x]
    return cu, cv, cm


def prepare_child(init: Tuple[Grid, Grid, Grid], mode: str, seed: int) -> Tuple[Grid, Grid, Grid]:
    u, v, m = [clone(x) for x in init]
    n = len(u)
    if mode == "no_inheritance":
        rng = random.Random(seed + 1000)
        u = zeros(n, 1.0)
        v = zeros(n, 0.0)
        m = zeros(n, 0.0)
        c = n // 2
        r = max(2, n // 10)
        for y in range(c - r, c + r):
            for x in range(c - r, c + r):
                u[y % n][x % n] = 0.5 + 0.02 * (rng.random() - 0.5)
                v[y % n][x % n] = 0.25 + 0.02 * (rng.random() - 0.5)
    elif mode == "pattern_only":
        m = zeros(n, 0.0)
    elif mode == "marker_only":
        v = [[0.22 * vv for vv in row] for row in v]
    elif mode == "full_inheritance":
        pass
    else:
        raise ValueError(mode)
    return u, v, m


def stress(u: Grid, v: Grid, m: Grid, marker_strength: float) -> None:
    n = len(u)
    # Stronger memory weakens damage, modeling marker-assisted survival.
    damage = 0.02 + 0.18 * (1.0 - marker_strength)
    for y in range(n // 4, 3 * n // 4):
        for x in range(n // 4, 3 * n // 4):
            v[y][x] *= damage
            m[y][x] *= 0.85


def run_child(init: Tuple[Grid, Grid, Grid], mode: str, seed: int, recover: int) -> Tuple[Grid, Grid, Grid]:
    u, v, m = prepare_child(init, mode, seed)
    marker_strength = min(1.0, mass(m) / (0.20 * len(m) * len(m))) if mass(m) > 0 else 0.0
    for t in range(recover):
        if t == max(10, recover // 4):
            stress(u, v, m, marker_strength if mode in {"marker_only", "full_inheritance"} else 0.0)
        u, v, m = step(u, v, m, mode)
    return u, v, m


MODES = ["no_inheritance", "pattern_only", "marker_only", "full_inheritance"]


def run_once(seed: int, n: int, settle: int, recover: int) -> Dict[str, Dict[str, float]]:
    parent = make_parent(seed, n, settle)
    out: Dict[str, Dict[str, float]] = {}
    for mode in MODES:
        sim: List[float] = []
        marker_sim: List[float] = []
        mass_ratio: List[float] = []
        survival: List[float] = []
        persistence: List[float] = []
        for side in ["L", "R"]:
            init = extract_half(parent, side)
            ref_v = init[1]
            ref_m = init[2]
            _, cv, cm = run_child(init, mode, seed + (101 if side == "R" else 0), recover)
            mr = mass(cv) / (mass(ref_v) or 1.0)
            vs = cosine(ref_v, cv)
            ms = cosine(ref_m, cm) if mass(ref_m) and mass(cm) else 0.0
            sim.append(vs)
            marker_sim.append(ms)
            mass_ratio.append(mr)
            survival.append(1.0 if mr > 0.65 else 0.0)
            persistence.append(vs * min(1.0, mr) * (0.5 + 0.5 * ms))
        out[mode] = {
            "child_similarity": sum(sim) / len(sim),
            "marker_similarity": sum(marker_sim) / len(marker_sim),
            "mass_ratio": sum(mass_ratio) / len(mass_ratio),
            "survival_rate": sum(survival) / len(survival),
            "persistence_index": sum(persistence) / len(persistence),
        }
    return out


def summarize(seeds: int, n: int, settle: int, recover: int) -> Dict[str, Dict[str, float]]:
    rows = [run_once(seed, n, settle, recover) for seed in range(seeds)]
    out: Dict[str, Dict[str, float]] = {}
    for mode in MODES:
        out[mode] = {}
        for key in rows[0][mode]:
            values = [row[mode][key] for row in rows]
            out[mode][key] = statistics.mean(values)
            out[mode][key + "_std"] = statistics.pstdev(values) if len(values) > 1 else 0.0
    return out


def print_table(rows: Dict[str, Dict[str, float]]) -> None:
    print("| mode | child similarity | marker similarity | mass ratio | survival | persistence index |")
    print("|---|---:|---:|---:|---:|---:|")
    for mode in MODES:
        row = rows[mode]
        print(
            f"| {mode} | {row['child_similarity']:.3f} | {row['marker_similarity']:.3f} | "
            f"{row['mass_ratio']:.2f} | {row['survival_rate']:.2f} | {row['persistence_index']:.3f} |"
        )


def run_split(seeds: int, n: int, settle: int, recover: int) -> None:
    rows = summarize(seeds, n, settle, recover)
    print_table(rows)


def run_selection(seeds: int, n: int, settle: int, recover: int) -> None:
    rows = summarize(seeds, n, settle, recover)
    print("| class | survival | persistence index | reading |")
    print("|---|---:|---:|---|")
    low_surv = (rows["no_inheritance"]["survival_rate"] + rows["marker_only"]["survival_rate"]) / 2
    low_pers = (rows["no_inheritance"]["persistence_index"] + rows["marker_only"]["persistence_index"]) / 2
    high_surv = (rows["pattern_only"]["survival_rate"] + rows["full_inheritance"]["survival_rate"]) / 2
    high_pers = (rows["pattern_only"]["persistence_index"] + rows["full_inheritance"]["persistence_index"]) / 2
    print(f"| weak/no transmitted activator | {low_surv:.2f} | {low_pers:.3f} | marker alone is not enough |")
    print(f"| transmitted active pattern | {high_surv:.2f} | {high_pers:.3f} | pattern-bearing children survive stress |")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["split", "selection", "all"], default="all")
    parser.add_argument("--seeds", type=int, default=3)
    parser.add_argument("--n", type=int, default=36)
    parser.add_argument("--settle", type=int, default=350)
    parser.add_argument("--recover", type=int, default=220)
    args = parser.parse_args()

    if args.mode in {"split", "all"}:
        print("## split inheritance")
        run_split(args.seeds, args.n, args.settle, args.recover)
        print()
    if args.mode in {"selection", "all"}:
        print("## selection bias")
        run_selection(args.seeds, args.n, args.settle, args.recover)


if __name__ == "__main__":
    main()
