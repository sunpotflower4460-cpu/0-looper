#!/usr/bin/env python3
"""One-flow sweep: 0/white -> field difference -> event -> relation -> causal order.

This is the integrated track. It is still a toy model:
- the 1D carrier is a computational substrate, not a claim of emergent space;
- events are created by threshold crossings in a local field;
- causal edges are inferred from recent local dependency;
- geometry-like hints are measured after the fact.
"""
from __future__ import annotations

import argparse
import itertools
import math
import random
import statistics
from typing import Dict, Iterable, List

PRESETS: Dict[str, Dict[str, float | int]] = {
    "balanced-oneflow": {"mu": 0.90, "D": 0.22, "eta": 0.012, "thr": 0.60, "rad": 3, "mem": 8, "birthcap": 6, "N": 96, "steps": 2000},
    "quiet-crystallize": {"mu": 0.75, "D": 0.26, "eta": 0.008, "thr": 0.55, "rad": 3, "mem": 10, "birthcap": 4, "N": 96, "steps": 2000},
    "active-web": {"mu": 1.10, "D": 0.16, "eta": 0.016, "thr": 0.62, "rad": 4, "mem": 8, "birthcap": 8, "N": 96, "steps": 2000},
    "wide-memory": {"mu": 0.90, "D": 0.22, "eta": 0.012, "thr": 0.60, "rad": 4, "mem": 14, "birthcap": 6, "N": 96, "steps": 2000},
    "sparse-events": {"mu": 0.80, "D": 0.26, "eta": 0.008, "thr": 0.70, "rad": 3, "mem": 8, "birthcap": 3, "N": 96, "steps": 2000},
    "hairball-null": {"mu": 1.20, "D": 0.35, "eta": 0.030, "thr": 0.35, "rad": 10, "mem": 25, "birthcap": 20, "N": 96, "steps": 2000},
    "weak-link-null": {"mu": 0.70, "D": 0.05, "eta": 0.004, "thr": 0.75, "rad": 1, "mem": 2, "birthcap": 1, "N": 96, "steps": 2000},
}


def noise4(rng: random.Random) -> float:
    return rng.random() + rng.random() + rng.random() + rng.random() - 2.0


def run_once(params: Dict[str, float | int], seed: int, max_events: int = 500) -> Dict[str, float]:
    rng = random.Random(seed)
    N = int(params.get("N", 96))
    steps = int(params.get("steps", 2000))
    mu = float(params["mu"])
    D = float(params["D"])
    eta = float(params["eta"])
    thr = float(params["thr"])
    rad = int(params["rad"])
    mem = int(params["mem"])
    birthcap = int(params["birthcap"])
    dt = 0.08

    u = [0.0] * N
    prev = [0.0] * N
    refractory = [-999] * N
    events: List[Dict[str, float | int]] = []
    edges = 0

    for t in range(steps):
        prev[:] = u[:]
        new = [0.0] * N
        for i, ui in enumerate(u):
            lap = u[(i - 1) % N] + u[(i + 1) % N] - 2 * ui
            du = D * lap + mu * ui - ui * ui * ui + eta * noise4(rng)
            new[i] = ui + dt * du
        u = new

        candidates = []
        for i, ui in enumerate(u):
            crossed = abs(ui) >= thr and abs(prev[i]) < thr
            kicked = abs(ui - prev[i]) > thr * 0.45 and abs(ui) > thr * 0.35
            if (crossed or kicked) and t - refractory[i] > 2:
                candidates.append((abs(ui) + abs(ui - prev[i]), i))
        candidates.sort(reverse=True)

        for _, i in candidates[:birthcap]:
            if len(events) >= max_events:
                break
            refractory[i] = t
            parent_ids = []
            for j in range(len(events) - 1, -1, -1):
                e = events[j]
                age = t - int(e["t"])
                if age > mem:
                    break
                dx = abs(i - int(e["x"]))
                dx = min(dx, N - dx)
                if dx <= rad and int(e["t"]) < t:
                    parent_ids.append(j)

            ancestors = 0
            chain = 1
            for p in parent_ids:
                ancestors |= (1 << p) | int(events[p]["anc"])
                chain = max(chain, int(events[p]["chain"]) + 1)

            events.append({"x": i, "t": t, "q": 1 if u[i] >= 0 else -1, "chain": chain, "anc": ancestors})
            edges += len(parent_ids)

        if len(events) >= max_events:
            break

    n = len(events)
    mean_amp = sum(abs(x) for x in u) / N
    if n < 2:
        return {"events": n, "edges": edges, "degree": 0.0, "chain": 0.0, "width": 0.0, "comparable_r": 0.0, "d_hint": float("nan"), "mean_amp": mean_amp}

    levels: Dict[int, int] = {}
    comparable = 0
    for e in events:
        ch = int(e["chain"])
        levels[ch] = levels.get(ch, 0) + 1
        comparable += int(e["anc"]).bit_count()
    chain = max(levels)
    width = max(levels.values())
    comparable_r = comparable / (n * (n - 1) / 2)
    degree = 2 * edges / n
    d_hint = math.log(n) / math.log(chain) if chain > 1 else float("nan")
    return {"events": float(n), "edges": float(edges), "degree": degree, "chain": float(chain), "width": float(width), "comparable_r": comparable_r, "d_hint": d_hint, "mean_amp": mean_amp}


def summarize(params: Dict[str, float | int], seeds: Iterable[int]) -> Dict[str, float]:
    rows = [run_once(params, s) for s in seeds]
    out: Dict[str, float] = {}
    for key in rows[0]:
        vals = [r[key] for r in rows if not math.isnan(r[key])]
        out[key] = statistics.mean(vals) if vals else float("nan")
        out[key + "_std"] = statistics.pstdev(vals) if len(vals) > 1 else 0.0
    return out


def verdict(row: Dict[str, float]) -> str:
    if row["events"] < 40:
        return "WEAK: too few events"
    if row["degree"] > 12 or row["comparable_r"] > 0.35:
        return "FAIL/WATCH: too dense"
    if row["degree"] < 1.0 or row["chain"] < 4:
        return "WEAK: too few relations"
    if row["width"] > 12 and row["chain"] > 6:
        return "PASS: one-flow candidate"
    return "WATCH"


def print_table(rows: List[tuple[str, Dict[str, float]]]) -> None:
    print("| template | events | avg degree | chain | width | comparable r | d hint | verdict |")
    print("|---|---:|---:|---:|---:|---:|---:|---|")
    for name, row in rows:
        print(f"| {name} | {row['events']:.1f} | {row['degree']:.2f} | {row['chain']:.1f} | {row['width']:.1f} | {row['comparable_r']:.3f} | {row['d_hint']:.2f} | {verdict(row)} |")


def run_presets(seeds: int) -> None:
    print_table([(name, summarize(params, range(seeds))) for name, params in PRESETS.items()])


def run_grid(seeds: int, top: int) -> None:
    rows = []
    for mu, D, eta, thr, rad, mem in itertools.product([0.75, 0.90, 1.05], [0.16, 0.22, 0.28], [0.008, 0.012], [0.55, 0.65], [3, 4], [8, 12]):
        p = {"mu": mu, "D": D, "eta": eta, "thr": thr, "rad": rad, "mem": mem, "birthcap": 6, "N": 80, "steps": 1400}
        row = summarize(p, range(seeds))
        score = 0.0
        if verdict(row).startswith("PASS"):
            score += 10
        score += max(0, 1 - abs(row["d_hint"] - 2.0))
        score += min(row["width"] / 30, 1.0)
        score += min(row["chain"] / 12, 1.0)
        score -= max(0, row["degree"] - 6) / 4
        rows.append((f"mu{mu}-D{D}-eta{eta}-thr{thr}-r{rad}-m{mem}", row, score))
    rows.sort(key=lambda x: x[2], reverse=True)
    print_table([(name, row) for name, row, _ in rows[:top]])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["presets", "grid"], default="presets")
    parser.add_argument("--seeds", type=int, default=20)
    parser.add_argument("--top", type=int, default=12)
    args = parser.parse_args()
    if args.mode == "presets":
        run_presets(args.seeds)
    else:
        run_grid(args.seeds, args.top)


if __name__ == "__main__":
    main()
