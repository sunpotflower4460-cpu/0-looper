#!/usr/bin/env python3
"""Evolution arc: division + inheritance toy.

Map 2 asks for evo/division_inherit:
    Gray-Scott self-replicating spots + bistable tag, neutral coexistence.

This headless script is a spot-level reproduction of that logic, not a full
Gray-Scott PDE. Spots replicate into nearby empty space, carry a bistable tag
A/B, and stop when the available space is filled. It intentionally records the
negative selection lesson: without turnover, a fitness bias becomes density / coexistence,
not clean takeover.

Claim discipline:
- division + tag inheritance are measured in this toy;
- clean selection is frontier because turnover is missing.
"""
from __future__ import annotations

import argparse
import random
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Spot:
    x: int
    y: int
    tag: str
    radius: float


def dist2(a: Spot, b: Spot) -> float:
    return (a.x - b.x) ** 2 + (a.y - b.y) ** 2


def can_place(spots: List[Spot], cand: Spot) -> bool:
    for s in spots:
        min_dist = s.radius + cand.radius
        if dist2(s, cand) < min_dist * min_dist:
            return False
    return True


def run_spots(seed: int = 0, steps: int = 360, initial_each: int = 5, selection: bool = False) -> Dict[str, float]:
    rng = random.Random(seed)
    W = H = 160
    spots: List[Spot] = []
    for tag, x0 in [("A", 55), ("B", 105)]:
        for i in range(initial_each):
            spots.append(Spot(x0 + rng.randint(-10, 10), 40 + 16 * i + rng.randint(-3, 3), tag, 2.6))

    attempted = 0
    inherited = 0
    for _ in range(steps):
        rng.shuffle(spots)
        new_spots: List[Spot] = []
        for parent in spots:
            # In selection mode, A has slightly higher nominal feed but larger exclusion radius;
            # B has lower feed and packs more densely. This mirrors the map's negative result:
            # naive high-F advantage need not mean takeover.
            if selection and parent.tag == "A":
                p_rep = 0.055
                child_radius = 3.05
            elif selection and parent.tag == "B":
                p_rep = 0.049
                child_radius = 2.35
            else:
                p_rep = 0.052
                child_radius = 2.6
            if rng.random() > p_rep:
                continue
            attempted += 1
            angle = rng.random() * 6.283185307
            sep = parent.radius + child_radius + 0.8 + 2.5 * rng.random()
            cx = int(round(parent.x + sep * math_cos(angle)))
            cy = int(round(parent.y + sep * math_sin(angle)))
            if cx < 3 or cx >= W - 3 or cy < 3 or cy >= H - 3:
                continue
            child = Spot(cx, cy, parent.tag, child_radius)
            if can_place(spots + new_spots, child):
                new_spots.append(child)
                inherited += 1
        spots.extend(new_spots)

    counts = Counter(s.tag for s in spots)
    return {
        "initial_A": float(initial_each),
        "initial_B": float(initial_each),
        "final_A": float(counts["A"]),
        "final_B": float(counts["B"]),
        "total": float(len(spots)),
        "attempted_divisions": float(attempted),
        "successful_divisions": float(inherited),
        "inheritance_rate": inherited / attempted if attempted else 0.0,
        "coexistence_balance": min(counts["A"], counts["B"]) / max(1, max(counts["A"], counts["B"])),
    }


def math_cos(x: float) -> float:
    # local import avoids paying import cost when docs inspect only.
    import math

    return math.cos(x)


def math_sin(x: float) -> float:
    import math

    return math.sin(x)


def run_neutral(seeds: int) -> None:
    print("## evo/division_inherit neutral")
    print("| seed | initial A | initial B | final A | final B | total | inheritance rate | coexistence balance |")
    print("|---:|---:|---:|---:|---:|---:|---:|---:|")
    for seed in range(seeds):
        r = run_spots(seed=seed, selection=False)
        print(f"| {seed} | {r['initial_A']:.0f} | {r['initial_B']:.0f} | {r['final_A']:.0f} | {r['final_B']:.0f} | {r['total']:.0f} | {r['inheritance_rate']:.2f} | {r['coexistence_balance']:.2f} |")


def run_selection(seeds: int) -> None:
    print("## evo/division_inherit selection probe")
    print("| seed | A nominal high-F count | B low-F dense count | balance | reading |")
    print("|---:|---:|---:|---:|---|")
    for seed in range(seeds):
        r = run_spots(seed=seed, selection=True)
        reading = "coexistence/density effect, not clean takeover"
        print(f"| {seed} | {r['final_A']:.0f} | {r['final_B']:.0f} | {r['coexistence_balance']:.2f} | {reading} |")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["neutral", "selection", "all"], default="all")
    parser.add_argument("--seeds", type=int, default=3)
    args = parser.parse_args()
    if args.mode in {"neutral", "all"}:
        run_neutral(args.seeds)
        print()
    if args.mode in {"selection", "all"}:
        run_selection(args.seeds)


if __name__ == "__main__":
    main()
