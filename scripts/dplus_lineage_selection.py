#!/usr/bin/env python3
"""D+ lineage selection toy.

This follows docs/14 delta inheritance.

Question:
    If a closed parent can split and transmit pattern/marker information, does a
    marker-rich closed loop persist across repeated generations better than
    pattern-only or marker-only inheritance?

This is a coarse lineage-level toy, not biology. It intentionally abstracts the
expensive Gray-Scott grid into two inherited state variables:

    p: active pattern strength
    m: memory / marker strength

Modes:
    no_inheritance : child starts from weak fresh seed
    pattern_only   : child inherits p but not m
    marker_only    : child inherits m but not p
    full_loop      : child inherits p and m; p maintains m, m protects p

The output is a survival curve across generations.
"""
from __future__ import annotations

import argparse
import random
import statistics
from typing import Dict, List, Tuple

MODES = ["no_inheritance", "pattern_only", "marker_only", "full_loop"]

Individual = Dict[str, float]
Row = Tuple[int, int, float, float, float]


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def make_child(parent: Individual, mode: str, rng: random.Random) -> Individual:
    if mode == "no_inheritance":
        p = 0.30 + 0.08 * rng.random()
        m = 0.02 * rng.random()
        protect = 0.0
    elif mode == "pattern_only":
        p = clamp(0.86 * parent["p"] + 0.08 * (rng.random() - 0.5))
        m = 0.02 * rng.random()
        protect = 0.0
    elif mode == "marker_only":
        p = 0.30 + 0.08 * rng.random()
        m = clamp(0.90 * parent["m"] + 0.04 * (rng.random() - 0.5))
        protect = m
    elif mode == "full_loop":
        m = clamp(0.86 * parent["m"] + 0.18 * parent["p"] + 0.04 * (rng.random() - 0.5))
        p = clamp(0.82 * parent["p"] + 0.22 * m + 0.08 * (rng.random() - 0.5))
        protect = m
    else:
        raise ValueError(mode)

    # Repeated environmental stress. Marker protects the active pattern only
    # when it is coupled back to p.
    stress = 0.25 + 0.55 * rng.random()
    damage = 0.34 * stress * (1.0 - 0.75 * protect)
    p_after = clamp(p - damage + 0.14 * m + 0.035 * (rng.random() - 0.5))

    if mode == "full_loop":
        m_after = clamp(0.90 * m + 0.18 * p_after - 0.035 * stress)
    elif mode == "marker_only":
        m_after = clamp(0.92 * m - 0.055 * stress)
    else:
        m_after = m

    return {"p": p_after, "m": m_after}


def survives(child: Individual, rng: random.Random) -> bool:
    survive_prob = clamp((child["p"] - 0.16) / 0.38 + 0.20 * child["m"])
    return rng.random() < survive_prob


def run_lineage(mode: str, seed: int = 0, generations: int = 20, founders: int = 24, cap: int = 200) -> List[Row]:
    rng = random.Random(seed)
    pop: List[Individual] = [{"p": 1.0, "m": 1.0} for _ in range(founders)]
    rows: List[Row] = []

    for g in range(generations + 1):
        if pop:
            mean_p = statistics.mean(x["p"] for x in pop)
            mean_m = statistics.mean(x["m"] for x in pop)
            persistence = statistics.mean(x["p"] * (0.5 + 0.5 * x["m"]) for x in pop)
        else:
            mean_p = mean_m = persistence = 0.0
        rows.append((g, len(pop), mean_p, mean_m, persistence))
        if g == generations:
            break

        children: List[Individual] = []
        for parent in pop:
            for _ in range(2):
                child = make_child(parent, mode, rng)
                if survives(child, rng):
                    children.append(child)

        # Carrying capacity plus selection by persistence.
        if len(children) > cap:
            children = sorted(children, key=lambda x: x["p"] * (0.55 + 0.45 * x["m"]), reverse=True)[:cap]
        pop = children
    return rows


def summarize(seeds: int, generations: int, founders: int, cap: int) -> Dict[int, Dict[str, Dict[str, float]]]:
    points = [1, 5, 10, generations]
    out: Dict[int, Dict[str, Dict[str, float]]] = {g: {} for g in points}
    for mode in MODES:
        runs = [run_lineage(mode, seed=s, generations=generations, founders=founders, cap=cap) for s in range(seeds)]
        for g in points:
            alive = [1.0 if run[g][1] > 0 else 0.0 for run in runs]
            counts = [float(run[g][1]) for run in runs]
            mean_p = [run[g][2] for run in runs]
            mean_m = [run[g][3] for run in runs]
            pers = [run[g][4] for run in runs]
            out[g][mode] = {
                "alive_rate": statistics.mean(alive),
                "count": statistics.mean(counts),
                "mean_p": statistics.mean(mean_p),
                "mean_m": statistics.mean(mean_m),
                "persistence": statistics.mean(pers),
            }
    return out


def print_generation_tables(seeds: int, generations: int, founders: int, cap: int) -> None:
    result = summarize(seeds, generations, founders, cap)
    for g, rows in result.items():
        print(f"## generation {g}")
        print("| mode | alive rate | mean count | mean pattern p | mean marker m | persistence |")
        print("|---|---:|---:|---:|---:|---:|")
        for mode in MODES:
            r = rows[mode]
            print(
                f"| {mode} | {r['alive_rate']:.2f} | {r['count']:.1f} | {r['mean_p']:.3f} | "
                f"{r['mean_m']:.3f} | {r['persistence']:.3f} |"
            )
        print()


def print_final_comparison(seeds: int, generations: int, founders: int, cap: int) -> None:
    result = summarize(seeds, generations, founders, cap)[generations]
    print("| mode | alive at final gen | final count | final persistence | reading |")
    print("|---|---:|---:|---:|---|")
    readings = {
        "no_inheritance": "fresh weak seeds die out",
        "pattern_only": "pattern alone does not survive repeated stress",
        "marker_only": "marker alone decays without active pattern",
        "full_loop": "p and m reinforce; lineage persists",
    }
    for mode in MODES:
        r = result[mode]
        print(f"| {mode} | {r['alive_rate']:.2f} | {r['count']:.1f} | {r['persistence']:.3f} | {readings[mode]} |")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["curve", "final", "all"], default="all")
    parser.add_argument("--seeds", type=int, default=12)
    parser.add_argument("--generations", type=int, default=20)
    parser.add_argument("--founders", type=int, default=24)
    parser.add_argument("--cap", type=int, default=200)
    args = parser.parse_args()

    if args.mode in {"curve", "all"}:
        print_generation_tables(args.seeds, args.generations, args.founders, args.cap)
    if args.mode in {"final", "all"}:
        print("## final comparison")
        print_final_comparison(args.seeds, args.generations, args.founders, args.cap)


if __name__ == "__main__":
    main()
