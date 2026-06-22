#!/usr/bin/env python3
"""Async causal origin experiment.

Goal:
    Test the track suggested by Claude's latest notes:

        no shared global clock
        -> local asynchronous changes
        -> dependency DAG
        -> causal layers / time slices
        -> dimension-like scaling

This is a toy model. The 1D ring is a computational substrate, so this does not
claim that space itself has emerged. It tests the complementary statement:
"time/order can be read from local change dependencies without a shared clock."
"""
from __future__ import annotations

import argparse
import math
import random
import statistics
from collections import defaultdict, deque
from typing import Dict, Iterable, List, Tuple


def run_once(
    n_cells: int = 32,
    sweeps: int = 32,
    seed: int = 0,
    radius: int = 1,
    inject_ctc: bool = False,
    keep_ancestors: bool = True,
) -> Dict[str, float | bool]:
    rng = random.Random(seed)
    n_events = n_cells * sweeps

    last_event: List[int | None] = [None] * n_cells
    event_cell: List[int] = []
    parents_by_event: List[List[int]] = []
    depth: List[int] = []
    ancestors: List[int] = []
    edges: List[Tuple[int, int]] = []

    for event_id in range(n_events):
        cell = rng.randrange(n_cells)
        parents: List[int] = []

        for dx in range(-radius, radius + 1):
            parent = last_event[(cell + dx) % n_cells]
            if parent is not None and parent not in parents:
                parents.append(parent)

        ancestor_bits = 0
        event_depth = 1
        for parent in parents:
            if keep_ancestors:
                ancestor_bits |= (1 << parent) | ancestors[parent]
            event_depth = max(event_depth, depth[parent] + 1)
            edges.append((parent, event_id))

        event_cell.append(cell)
        parents_by_event.append(parents)
        depth.append(event_depth)
        ancestors.append(ancestor_bits)
        last_event[cell] = event_id

    ctc_injected = False
    if inject_ctc and n_events > 1:
        first_cell = event_cell[0]
        target = None
        for event_id in range(n_events - 1, 0, -1):
            if event_cell[event_id] == first_cell:
                target = event_id
                break
        if target is not None:
            # target is normally a descendant along the same cell history.
            # Adding target -> 0 creates a closed time-like dependency.
            edges.append((target, 0))
            ctc_injected = True

    topo_count = topo_sort_count(n_events, edges)
    levels: Dict[int, int] = defaultdict(int)
    for d in depth:
        levels[d] += 1

    comparable_pairs = sum(bits.bit_count() for bits in ancestors) if keep_ancestors else 0
    total_pairs = n_events * (n_events - 1) / 2
    comparable_ratio = comparable_pairs / total_pairs if total_pairs else 0.0

    return {
        "events": float(n_events),
        "edges": float(len(edges)),
        "dag": topo_count == n_events,
        "topo_ordered": float(topo_count),
        "depth": float(max(depth)),
        "width": float(max(levels.values())),
        "avg_width": float(sum(levels.values()) / len(levels)),
        "comparable_ratio": comparable_ratio,
        "ctc_injected": ctc_injected,
    }


def topo_sort_count(n_events: int, edges: Iterable[Tuple[int, int]]) -> int:
    indegree = [0] * n_events
    children: List[List[int]] = [[] for _ in range(n_events)]
    for parent, child in edges:
        if 0 <= parent < n_events and 0 <= child < n_events:
            children[parent].append(child)
            indegree[child] += 1

    queue = deque(i for i, deg in enumerate(indegree) if deg == 0)
    count = 0
    while queue:
        node = queue.popleft()
        count += 1
        for child in children[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    return count


def summarize(n_cells: int, sweeps: int, seeds: int, radius: int, inject_ctc: bool = False) -> Dict[str, float]:
    rows = [run_once(n_cells, sweeps, seed, radius, inject_ctc) for seed in range(seeds)]
    out: Dict[str, float] = {}
    for key in ["events", "edges", "topo_ordered", "depth", "width", "avg_width", "comparable_ratio"]:
        vals = [float(row[key]) for row in rows]
        out[key] = statistics.mean(vals)
        out[key + "_std"] = statistics.pstdev(vals) if len(vals) > 1 else 0.0
    out["dag_rate"] = statistics.mean(1.0 if row["dag"] else 0.0 for row in rows)
    out["ctc_rate"] = statistics.mean(1.0 if row["ctc_injected"] else 0.0 for row in rows)
    return out


def dimension_scaling(sizes: List[int], seeds: int, radius: int) -> Dict[str, float | List[Tuple[int, float, float]]]:
    # Use sweeps = n_cells so the sampled region is roughly space-size by time-size.
    points: List[Tuple[int, float, float]] = []
    for n_cells in sizes:
        depths = []
        events = []
        for seed in range(seeds):
            row = run_once(n_cells, n_cells, seed, radius, keep_ancestors=False)
            depths.append(float(row["depth"]))
            events.append(float(row["events"]))
        points.append((n_cells, statistics.mean(events), statistics.mean(depths)))

    xs = [math.log(events) for _, events, _ in points]
    ys = [math.log(depth) for _, _, depth in points]
    mx = statistics.mean(xs)
    my = statistics.mean(ys)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    dim = 1 / slope if slope else float("inf")
    return {"points": points, "slope": slope, "dimension_hint": dim}


def print_summary(label: str, row: Dict[str, float]) -> None:
    print(f"## {label}")
    print("| events | edges | DAG rate | topo ordered | depth | width | avg width | comparable r |")
    print("|---:|---:|---:|---:|---:|---:|---:|---:|")
    print(
        f"| {row['events']:.1f} | {row['edges']:.1f} | {row['dag_rate']:.2f} | "
        f"{row['topo_ordered']:.1f} | {row['depth']:.1f} | {row['width']:.1f} | "
        f"{row['avg_width']:.1f} | {row['comparable_ratio']:.3f} |"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["summary", "ctc", "scaling"], default="summary")
    parser.add_argument("--cells", type=int, default=32)
    parser.add_argument("--sweeps", type=int, default=32)
    parser.add_argument("--seeds", type=int, default=10)
    parser.add_argument("--radius", type=int, default=1)
    args = parser.parse_args()

    if args.mode == "summary":
        print_summary("async local updates", summarize(args.cells, args.sweeps, args.seeds, args.radius))
    elif args.mode == "ctc":
        print_summary("with injected CTC", summarize(args.cells, args.sweeps, args.seeds, args.radius, inject_ctc=True))
    else:
        result = dimension_scaling([16, 24, 32, 48, 64], args.seeds, args.radius)
        print("| cells | events | depth |")
        print("|---:|---:|---:|")
        for n_cells, events, depth in result["points"]:  # type: ignore[index]
            print(f"| {n_cells} | {events:.1f} | {depth:.1f} |")
        print(f"\nslope = {result['slope']:.3f}")
        print(f"dimension_hint = {result['dimension_hint']:.3f}")


if __name__ == "__main__":
    main()
