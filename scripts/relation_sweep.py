#!/usr/bin/env python3
"""Headless sweep for relation-lab.

This is intentionally small and dependency-free.
It tests whether a relation-first causal growth rule avoids the two bad collapses:

- chain collapse: almost everything is comparable, width disappears
- hairball collapse: degree explodes, distance becomes unreadable

The model is still a toy. It does not prove emergent spacetime.
"""
from __future__ import annotations

import argparse
import math
import random
import statistics
from dataclasses import dataclass
from typing import Dict, Iterable, List, Set


@dataclass
class Node:
    id: int
    phase: float
    q: int
    chain: int
    ancestors: Set[int]


PRESETS: Dict[str, Dict[str, float | int | str]] = {
    "woven-width": {
        "regime": "balanced",
        "birth": 2,
        "frontier": 32,
        "parents": 4,
        "comp": 0.35,
        "balance": 0.70,
        "maxn": 260,
    },
    "thin-causal": {
        "regime": "balanced",
        "birth": 2,
        "frontier": 16,
        "parents": 3,
        "comp": 0.35,
        "balance": 0.70,
        "maxn": 260,
    },
    "wide-frontier": {
        "regime": "balanced",
        "birth": 2,
        "frontier": 60,
        "parents": 3,
        "comp": 0.55,
        "balance": 0.20,
        "maxn": 260,
    },
    "sparse-spacious": {
        "regime": "balanced",
        "birth": 1,
        "frontier": 44,
        "parents": 3,
        "comp": 0.75,
        "balance": 0.45,
        "maxn": 260,
    },
    "chain-null": {
        "regime": "chain",
        "birth": 2,
        "frontier": 32,
        "parents": 4,
        "comp": 0.35,
        "balance": 0.70,
        "maxn": 260,
    },
    "hairball-null": {
        "regime": "hairball",
        "birth": 2,
        "frontier": 32,
        "parents": 4,
        "comp": 0.35,
        "balance": 0.70,
        "maxn": 260,
    },
    "random-null": {
        "regime": "random",
        "birth": 2,
        "frontier": 32,
        "parents": 4,
        "comp": 0.35,
        "balance": 0.70,
        "maxn": 260,
    },
}


def angle_diff(a: float, b: float) -> float:
    tau = 2 * math.pi
    d = abs(a - b) % tau
    return min(d, tau - d)


def run_once(params: Dict[str, float | int | str], seed: int) -> Dict[str, float]:
    rng = random.Random(seed)
    maxn = int(params["maxn"])
    nodes: List[Node] = []
    edges = 0

    def add_root() -> None:
        nodes.append(
            Node(
                id=len(nodes),
                phase=rng.random() * 2 * math.pi,
                q=-1 if rng.random() < 0.5 else 1,
                chain=1,
                ancestors=set(),
            )
        )

    for _ in range(3):
        add_root()

    def choose_parents() -> List[Node]:
        n = len(nodes)
        regime = str(params["regime"])
        if regime == "chain":
            return [nodes[-1]]

        frontier = int(params["frontier"])
        pool = nodes[max(0, n - frontier) :] if regime != "random" else nodes[:]
        want = max(1, math.floor(1 + rng.random() * int(params["parents"])))
        if regime == "hairball":
            want = min(len(pool), max(8, int(params["parents"]) * 8))

        qsum = sum(x.q for x in nodes)
        target_q = -1 if qsum > 0 else 1
        ref_phase = nodes[-1].phase
        comp_w = float(params["comp"])
        balance_w = float(params["balance"])
        inv_frontier = 1 / max(1, frontier)

        scored = []
        for p in pool:
            comp = 1 - angle_diff(p.phase, ref_phase) / math.pi
            balance = 1 if p.q == target_q else 0
            recent = 1 - (n - p.id) * inv_frontier
            if regime == "balanced":
                score = comp_w * comp + balance_w * balance + 0.25 * recent + rng.random() * 0.25
            else:
                score = rng.random()
            scored.append((score, p))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [p for _, p in scored[:want]]

    while len(nodes) < maxn:
        for _ in range(int(params["birth"])):
            if len(nodes) >= maxn:
                break
            parents = choose_parents()
            if parents:
                phase = sum(p.phase for p in parents) / len(parents) + (rng.random() - 0.5) * 1.1
                parent_q = sum(p.q for p in parents)
                q = -1 if parent_q > 0 else 1 if parent_q < 0 else (-1 if rng.random() < 0.5 else 1)
            else:
                phase = rng.random() * 2 * math.pi
                q = -1 if rng.random() < 0.5 else 1
            if rng.random() < 0.12:
                q *= -1

            ancestors: Set[int] = set()
            chain = 1
            for p in parents:
                ancestors.add(p.id)
                ancestors.update(p.ancestors)
                chain = max(chain, p.chain + 1)

            nodes.append(Node(len(nodes), phase, q, chain, ancestors))
            edges += len(parents)

    n = len(nodes)
    degree = 2 * edges / n
    longest_chain = max(x.chain for x in nodes)
    levels: Dict[int, int] = {}
    comparable_pairs = 0
    for x in nodes:
        levels[x.chain] = levels.get(x.chain, 0) + 1
        comparable_pairs += len(x.ancestors)
    width = max(levels.values())
    comparable_ratio = comparable_pairs / (n * (n - 1) / 2)
    d_hint = math.log(n) / math.log(longest_chain)

    return {
        "n": n,
        "edges": edges,
        "degree": degree,
        "longest_chain": longest_chain,
        "width": width,
        "comparable_ratio": comparable_ratio,
        "d_hint": d_hint,
    }


def summarize(params: Dict[str, float | int | str], seeds: Iterable[int]) -> Dict[str, float]:
    runs = [run_once(params, seed) for seed in seeds]
    out: Dict[str, float] = {}
    for key in runs[0]:
        values = [r[key] for r in runs]
        out[key] = statistics.mean(values)
        out[key + "_std"] = statistics.pstdev(values)
    return out


def verdict(row: Dict[str, float]) -> str:
    if row["comparable_ratio"] > 0.85:
        return "FAIL: chain collapse"
    if row["degree"] > 18:
        return "FAIL: hairball collapse"
    if row["width"] > 10 and row["longest_chain"] > 20:
        return "PASS: width+chain coexist"
    return "WATCH"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=30)
    args = parser.parse_args()
    seeds = range(args.seeds)

    print("| preset | avg degree | longest chain | width | comparable r | d hint | verdict |")
    print("|---|---:|---:|---:|---:|---:|---|")
    for name, params in PRESETS.items():
        row = summarize(params, seeds)
        print(
            f"| {name} | {row['degree']:.2f} | {row['longest_chain']:.1f} | "
            f"{row['width']:.1f} | {row['comparable_ratio']:.3f} | {row['d_hint']:.2f} | {verdict(row)} |"
        )


if __name__ == "__main__":
    main()
