#!/usr/bin/env python3
"""Headless sweep for relation-lab.

This dependency-free script tests whether relation-first causal growth rules avoid two
bad collapses:

- chain collapse: almost everything is comparable, width disappears
- hairball collapse: degree explodes, distance becomes unreadable

The model is still a toy. It does not prove emergent spacetime.
"""
from __future__ import annotations

import argparse
import itertools
import math
import random
import statistics
from typing import Dict, Iterable, List


PRESETS: Dict[str, Dict[str, float | int | str]] = {
    # Current first recommendation from the expanded sweep.
    "woven-width-v2": {
        "regime": "balanced",
        "birth": 2,
        "frontier": 32,
        "parents": 4,
        "comp": 0.50,
        "balance": 0.55,
        "maxn": 260,
    },
    # Older first recommendation, kept for comparison.
    "woven-width-v1": {
        "regime": "balanced",
        "birth": 2,
        "frontier": 32,
        "parents": 4,
        "comp": 0.35,
        "balance": 0.70,
        "maxn": 260,
    },
    "thin-causal-v2": {
        "regime": "balanced",
        "birth": 2,
        "frontier": 16,
        "parents": 4,
        "comp": 0.50,
        "balance": 0.55,
        "maxn": 260,
    },
    "wide-frontier-v2": {
        "regime": "balanced",
        "birth": 2,
        "frontier": 60,
        "parents": 4,
        "comp": 0.50,
        "balance": 0.55,
        "maxn": 260,
    },
    "sparse-spacious-v2": {
        "regime": "balanced",
        "birth": 1,
        "frontier": 44,
        "parents": 3,
        "comp": 0.75,
        "balance": 0.45,
        "maxn": 260,
    },
    "low-degree-web": {
        "regime": "balanced",
        "birth": 2,
        "frontier": 80,
        "parents": 2,
        "comp": 0.75,
        "balance": 0.20,
        "maxn": 260,
    },
    "chain-null": {
        "regime": "chain",
        "birth": 2,
        "frontier": 32,
        "parents": 4,
        "comp": 0.50,
        "balance": 0.55,
        "maxn": 260,
    },
    "hairball-null": {
        "regime": "hairball",
        "birth": 2,
        "frontier": 32,
        "parents": 4,
        "comp": 0.50,
        "balance": 0.55,
        "maxn": 260,
    },
    "random-null": {
        "regime": "random",
        "birth": 2,
        "frontier": 32,
        "parents": 4,
        "comp": 0.50,
        "balance": 0.55,
        "maxn": 260,
    },
}


def _angle_diff(a: float, b: float) -> float:
    tau = 2 * math.pi
    d = abs(a - b) % tau
    return d if d <= math.pi else tau - d


def run_once(params: Dict[str, float | int | str], seed: int, maxn: int | None = None) -> Dict[str, float]:
    """Run one graph-growth trial.

    Ancestors are stored as Python integer bitsets, so sweeps stay fast without
    third-party dependencies.
    """
    rng = random.Random(seed)
    nmax = int(maxn if maxn is not None else params["maxn"])
    tau = 2 * math.pi

    phase: List[float] = []
    charge: List[int] = []
    chain: List[int] = []
    ancestors: List[int] = []
    edges = 0

    for _ in range(3):
        phase.append(rng.random() * tau)
        charge.append(-1 if rng.random() < 0.5 else 1)
        chain.append(1)
        ancestors.append(0)

    while len(phase) < nmax:
        for _ in range(int(params["birth"])):
            n = len(phase)
            if n >= nmax:
                break

            regime = str(params["regime"])
            if regime == "chain":
                parent_ids = [n - 1]
            else:
                frontier = int(params["frontier"])
                start = 0 if regime == "random" else max(0, n - frontier)
                want = max(1, int(1 + rng.random() * int(params["parents"])))
                if regime == "hairball":
                    want = min(n - start, max(8, int(params["parents"]) * 8))

                target_q = -1 if sum(charge) > 0 else 1
                ref_phase = phase[-1]
                comp_w = float(params["comp"])
                balance_w = float(params["balance"])
                inv_frontier = 1 / max(1, frontier)

                scored: List[tuple[float, int]] = []
                for p in range(start, n):
                    comp = 1 - _angle_diff(phase[p], ref_phase) / math.pi
                    bal = 1 if charge[p] == target_q else 0
                    recent = 1 - (n - p) * inv_frontier
                    if regime == "balanced":
                        score = comp_w * comp + balance_w * bal + 0.25 * recent + rng.random() * 0.25
                    else:
                        score = rng.random()
                    scored.append((score, p))
                scored.sort(reverse=True)
                parent_ids = [p for _, p in scored[:want]]

            if parent_ids:
                new_phase = sum(phase[p] for p in parent_ids) / len(parent_ids) + (rng.random() - 0.5) * 1.1
                parent_q = sum(charge[p] for p in parent_ids)
                new_q = -1 if parent_q > 0 else 1 if parent_q < 0 else (-1 if rng.random() < 0.5 else 1)
            else:
                new_phase = rng.random() * tau
                new_q = -1 if rng.random() < 0.5 else 1
            if rng.random() < 0.12:
                new_q *= -1

            mask = 0
            new_chain = 1
            for p in parent_ids:
                mask |= (1 << p) | ancestors[p]
                new_chain = max(new_chain, chain[p] + 1)

            phase.append(new_phase)
            charge.append(new_q)
            chain.append(new_chain)
            ancestors.append(mask)
            edges += len(parent_ids)

    n = len(phase)
    levels: Dict[int, int] = {}
    comparable_pairs = 0
    for ch, mask in zip(chain, ancestors):
        levels[ch] = levels.get(ch, 0) + 1
        comparable_pairs += mask.bit_count()

    longest_chain = max(chain)
    width = max(levels.values())
    comparable_ratio = comparable_pairs / (n * (n - 1) / 2)
    avg_degree = 2 * edges / n
    d_hint = math.log(n) / math.log(longest_chain)

    return {
        "n": n,
        "edges": edges,
        "degree": avg_degree,
        "longest_chain": longest_chain,
        "width": width,
        "comparable_ratio": comparable_ratio,
        "d_hint": d_hint,
    }


def summarize(params: Dict[str, float | int | str], seeds: Iterable[int], maxn: int | None = None) -> Dict[str, float]:
    runs = [run_once(params, seed, maxn=maxn) for seed in seeds]
    out: Dict[str, float] = {}
    for key in runs[0]:
        values = [r[key] for r in runs]
        out[key] = statistics.mean(values)
        out[f"{key}_std"] = statistics.pstdev(values)
    return out


def verdict(row: Dict[str, float]) -> str:
    if row["comparable_ratio"] > 0.85:
        return "FAIL: chain collapse"
    if row["degree"] > 18:
        return "FAIL: hairball collapse"
    if row["width"] > 10 and row["longest_chain"] > 20:
        return "PASS: width+chain coexist"
    return "WATCH"


def score(row: Dict[str, float], target_r: float = 0.23) -> float:
    if row["degree"] > 14 or row["comparable_ratio"] > 0.72 or row["width"] < 7 or row["longest_chain"] < 12:
        return -999.0
    s = 0.0
    s += min(row["longest_chain"] / 60, 1.4) * 2
    s += min(row["width"] / 30, 1.4) * 2
    s += max(0, 1 - abs(row["comparable_ratio"] - target_r) / 0.2) * 2
    s += max(0, 1 - abs(row["degree"] - 5) / 5)
    s -= row.get("longest_chain_std", 0) / 40
    s -= row.get("width_std", 0) / 30
    return s


def print_table(rows: List[tuple[str, Dict[str, float]]]) -> None:
    print("| preset | avg degree | longest chain | width | comparable r | d hint | verdict |")
    print("|---|---:|---:|---:|---:|---:|---|")
    for name, row in rows:
        print(
            f"| {name} | {row['degree']:.2f} | {row['longest_chain']:.1f} | "
            f"{row['width']:.1f} | {row['comparable_ratio']:.3f} | {row['d_hint']:.2f} | {verdict(row)} |"
        )


def run_presets(seeds_count: int) -> None:
    seeds = range(seeds_count)
    rows = [(name, summarize(params, seeds)) for name, params in PRESETS.items()]
    print_table(rows)


def run_grid(seeds_count: int, top: int) -> None:
    seeds = range(seeds_count)
    rows: List[tuple[str, Dict[str, float]]] = []
    for birth, frontier, parents, comp, balance in itertools.product(
        [1, 2, 3],
        [12, 16, 24, 32, 44, 60, 80],
        [2, 3, 4, 6],
        [0.25, 0.50, 0.75],
        [0.20, 0.55, 0.85],
    ):
        params: Dict[str, float | int | str] = {
            "regime": "balanced",
            "birth": birth,
            "frontier": frontier,
            "parents": parents,
            "comp": comp,
            "balance": balance,
            "maxn": 220,
        }
        row = summarize(params, seeds)
        row["score"] = score(row)
        label = f"b{birth}-f{frontier}-p{parents}-c{comp:.2f}-bal{balance:.2f}"
        rows.append((label, row))
    rows.sort(key=lambda x: x[1]["score"], reverse=True)
    print_table(rows[:top])


def run_scaling(seeds_count: int) -> None:
    seeds = range(seeds_count)
    sizes = [120, 180, 260, 380, 520]
    names = ["woven-width-v2", "thin-causal-v2", "wide-frontier-v2", "sparse-spacious-v2", "low-degree-web"]
    print("| preset | maxn | avg degree | longest chain | width | comparable r | d hint |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    for name in names:
        params = PRESETS[name]
        for n in sizes:
            row = summarize(params, seeds, maxn=n)
            print(
                f"| {name} | {n} | {row['degree']:.2f} | {row['longest_chain']:.1f} | "
                f"{row['width']:.1f} | {row['comparable_ratio']:.3f} | {row['d_hint']:.2f} |"
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=30)
    parser.add_argument("--mode", choices=["presets", "grid", "scaling"], default="presets")
    parser.add_argument("--top", type=int, default=12)
    args = parser.parse_args()

    if args.mode == "presets":
        run_presets(args.seeds)
    elif args.mode == "grid":
        run_grid(args.seeds, args.top)
    else:
        run_scaling(args.seeds)


if __name__ == "__main__":
    main()
