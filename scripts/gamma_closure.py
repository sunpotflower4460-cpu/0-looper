#!/usr/bin/env python3
"""γ closure / vessel toy experiments.

Track from the Claude convergence map:
    vessel / closure

A Gray-Scott-like reaction-diffusion seed is used as a minimal proxy for
self-organizing pattern. A second field m is a memory / membrane proxy.

Tests:
- self-repair: pattern after half-destruction recovers mass/structure.
- memory: memory+confinement improves return to pre-damage pattern.
- closure: A->M and M->A arms are both needed for strongest persistence.

Claim discipline:
This is not life, cell biology, or a real membrane. It is a toy test of whether
self-produced memory/confinement improves persistence after damage.
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


def lap(a: Grid, x: int, y: int, n: int) -> float:
    return a[y][(x - 1) % n] + a[y][(x + 1) % n] + a[(y - 1) % n][x] + a[(y + 1) % n][x] - 4 * a[y][x]


def mass(a: Grid) -> float:
    return sum(sum(row) for row in a)


def cosine(a: Grid, b: Grid) -> float:
    n = len(a)
    dot = sum(a[y][x] * b[y][x] for y in range(n) for x in range(n))
    na = math.sqrt(sum(a[y][x] ** 2 for y in range(n) for x in range(n)))
    nb = math.sqrt(sum(b[y][x] ** 2 for y in range(n) for x in range(n)))
    return dot / (na * nb) if na and nb else 0.0


def clone(a: Grid) -> Grid:
    return [row[:] for row in a]


def run_once(
    seed: int = 0,
    n: int = 40,
    settle: int = 500,
    recover: int = 300,
    produce_m: bool = False,
    confine: bool = False,
    initial_m: bool = False,
    F: float = 0.037,
    k: float = 0.060,
    Du: float = 0.16,
    Dv: float = 0.08,
    Dm: float = 0.05,
    alpha: float = 0.02,
    beta: float = 0.02,
    damage_m_factor: float = 0.2,
) -> Dict[str, float]:
    rng = random.Random(seed)
    u = zeros(n, 1.0)
    v = zeros(n, 0.0)
    m = zeros(n, 0.0)

    c = n // 2
    r = max(2, n // 10)
    for y in range(c - r, c + r):
        for x in range(c - r, c + r):
            u[y % n][x % n] = 0.5 + 0.02 * (rng.random() - 0.5)
            v[y % n][x % n] = 0.25 + 0.02 * (rng.random() - 0.5)
            if initial_m:
                m[y % n][x % n] = 0.8

    def step() -> None:
        nonlocal u, v, m
        nu = zeros(n)
        nv = zeros(n)
        nm = zeros(n)
        for y in range(n):
            for x in range(n):
                uu = u[y][x]
                vv = v[y][x]
                mm = max(0.0, min(1.0, m[y][x]))

                # m is a memory/confinement proxy.
                # If confine=True, high m lowers activator leakage/decay locally.
                d_v_eff = Dv * (1.0 - 0.45 * mm) if confine else Dv
                k_eff = k * (1.0 - 0.25 * mm) if confine else k

                reaction = uu * vv * vv
                nuv = uu + Du * lap(u, x, y, n) - reaction + F * (1.0 - uu)
                nvv = vv + d_v_eff * lap(v, x, y, n) + reaction - (F + k_eff) * vv

                if produce_m:
                    nmm = m[y][x] + Dm * lap(m, x, y, n) + alpha * vv - beta * m[y][x]
                else:
                    nmm = m[y][x] + Dm * lap(m, x, y, n) - beta * m[y][x]

                nu[y][x] = min(1.2, max(0.0, nuv))
                nv[y][x] = min(1.2, max(0.0, nvv))
                nm[y][x] = min(1.0, max(0.0, nmm))
        u, v, m = nu, nv, nm

    for _ in range(settle):
        step()

    pre_v = clone(v)
    pre_mass = mass(v)
    pre_membrane = mass(m)

    # Half-destruction: wipe activator on left half and damage memory there.
    for y in range(n):
        for x in range(n // 2):
            u[y][x] = 1.0
            v[y][x] = 0.0
            m[y][x] *= damage_m_factor

    post_mass = mass(v)
    post_membrane = mass(m)

    for _ in range(recover):
        step()

    final_mass = mass(v)
    final_membrane = mass(m)
    structural_similarity = cosine(pre_v, v)
    recovery_ratio = (final_mass - post_mass) / (pre_mass - post_mass) if pre_mass > post_mass else 0.0
    persistence_index = structural_similarity * (final_mass / pre_mass if pre_mass else 0.0)

    return {
        "pre_mass": pre_mass,
        "post_mass": post_mass,
        "final_mass": final_mass,
        "pre_membrane": pre_membrane,
        "post_membrane": post_membrane,
        "final_membrane": final_membrane,
        "recovery_ratio": recovery_ratio,
        "structural_similarity": structural_similarity,
        "persistence_index": persistence_index,
    }


CONFIGS: Dict[str, Dict[str, bool]] = {
    "no_closure": {"produce_m": False, "confine": False, "initial_m": False},
    "A_to_M_only": {"produce_m": True, "confine": False, "initial_m": False},
    "M_to_A_only": {"produce_m": False, "confine": True, "initial_m": True},
    "closed_loop": {"produce_m": True, "confine": True, "initial_m": False},
}


def summarize(name: str, seeds: int, n: int, settle: int, recover: int) -> Dict[str, float]:
    rows = [run_once(seed=s, n=n, settle=settle, recover=recover, **CONFIGS[name]) for s in range(seeds)]
    out: Dict[str, float] = {}
    for key in rows[0]:
        values = [row[key] for row in rows]
        out[key] = statistics.mean(values)
        out[key + "_std"] = statistics.pstdev(values) if len(values) > 1 else 0.0
    return out


def print_table(rows: List[Tuple[str, Dict[str, float]]]) -> None:
    print("| config | pre mass | post damage | final mass | recovery | similarity | persistence | final membrane |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|")
    for name, row in rows:
        print(
            f"| {name} | {row['pre_mass']:.2f} | {row['post_mass']:.2f} | {row['final_mass']:.2f} | "
            f"{row['recovery_ratio']:.2f} | {row['structural_similarity']:.3f} | "
            f"{row['persistence_index']:.3f} | {row['final_membrane']:.2f} |"
        )


def run_self_repair(seeds: int, n: int, settle: int, recover: int) -> None:
    rows = [("gray_scott_seed", summarize("no_closure", seeds, n, settle, recover))]
    print_table(rows)


def run_memory(seeds: int, n: int, settle: int, recover: int) -> None:
    rows = [("no_memory", summarize("no_closure", seeds, n, settle, recover)), ("memory_closed_loop", summarize("closed_loop", seeds, n, settle, recover))]
    print_table(rows)


def run_closure(seeds: int, n: int, settle: int, recover: int) -> None:
    rows = [(name, summarize(name, seeds, n, settle, recover)) for name in CONFIGS]
    print_table(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["self-repair", "memory", "closure", "all"], default="all")
    parser.add_argument("--seeds", type=int, default=3)
    parser.add_argument("--n", type=int, default=40)
    parser.add_argument("--settle", type=int, default=500)
    parser.add_argument("--recover", type=int, default=300)
    args = parser.parse_args()

    if args.mode in ("self-repair", "all"):
        print("## self repair")
        run_self_repair(args.seeds, args.n, args.settle, args.recover)
        print()
    if args.mode in ("memory", "all"):
        print("## memory")
        run_memory(args.seeds, args.n, args.settle, args.recover)
        print()
    if args.mode in ("closure", "all"):
        print("## closure arms")
        run_closure(args.seeds, args.n, args.settle, args.recover)


if __name__ == "__main__":
    main()
