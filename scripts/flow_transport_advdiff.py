#!/usr/bin/env python3
"""Non-tautological 1D advection-diffusion transport check.

This script is a response to the map2 audit: the earlier
`flow_benard_transport.py --mode transport` encoded the reported 12x result by
choosing two time constants. That is useful as a regression smoke-test, but not
as physics verification.

Here we actually evolve a passive scalar on a 1D vertical column:

    ∂c/∂t + u ∂c/∂y = D ∂²c/∂y²

using explicit finite differences. If the parameters are wrong, the result can
fail. The output is therefore a lightweight mechanism check, not a hard-coded
reprint of map2's numbers.

Claim discipline:
- this is still not a full 2D Boussinesq flow solver;
- it checks transport by a given developed velocity field;
- generating that velocity field from Benard dynamics remains the next step.
"""
from __future__ import annotations

import argparse


def simulate(
    n: int = 201,
    steps: int = 800,
    dt: float = 0.5,
    D: float = 2e-5,
    u: float = 0.0,
    source_steps: int = 50,
) -> tuple[float, float, float]:
    dy = 1.0 / (n - 1)
    diff_cfl = D * dt / (dy * dy)
    adv_cfl = abs(u) * dt / dy
    if diff_cfl > 0.5:
        raise ValueError(f"unstable diffusion CFL={diff_cfl:.3f}; reduce D or dt")
    if adv_cfl > 1.0:
        raise ValueError(f"unstable advection CFL={adv_cfl:.3f}; reduce u or dt")

    c = [0.0] * n
    for t in range(steps):
        old = c[:]
        if t < source_steps:
            old[0] = 1.0
        new = old[:]
        for i in range(1, n - 1):
            diffusion = diff_cfl * (old[i - 1] - 2.0 * old[i] + old[i + 1])
            if u >= 0:
                advection = -adv_cfl * (old[i] - old[i - 1])
            else:
                advection = -adv_cfl * (old[i + 1] - old[i])
            new[i] = max(0.0, min(1.0, old[i] + diffusion + advection))
        # Bottom source during injection; otherwise no-flux boundaries.
        new[0] = 1.0 if t < source_steps else new[1]
        new[-1] = new[-2]
        c = new

    top_mean = sum(c[-10:]) / 10.0
    total_mass = sum(c) / n
    return top_mean, total_mass, max(c)


def run(args: argparse.Namespace) -> None:
    print("| case | u | steps | source steps | C_top mean | total mass | max c | mechanism |")
    print("|---|---:|---:|---:|---:|---:|---:|---|")
    diff_top, diff_mass, diff_max = simulate(n=args.n, steps=args.steps, dt=args.dt, D=args.D, u=0.0, source_steps=args.source_steps)
    print(f"| diffusion only | 0.0000 | {args.steps} | {args.source_steps} | {diff_top:.6f} | {diff_mass:.6f} | {diff_max:.3f} | diffusion PDE |")
    for u in args.u:
        top, mass, mx = simulate(n=args.n, steps=args.steps, dt=args.dt, D=args.D, u=u, source_steps=args.source_steps)
        ratio = top / diff_top if diff_top > 1e-12 else float("inf")
        ratio_txt = f"; top/diff={ratio:.1f}" if ratio != float("inf") else "; top/diff=inf"
        print(f"| developed advection | {u:.4f} | {args.steps} | {args.source_steps} | {top:.6f} | {mass:.6f} | {mx:.3f} | adv-diff PDE{ratio_txt} |")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=201)
    parser.add_argument("--steps", type=int, default=800)
    parser.add_argument("--dt", type=float, default=0.5)
    parser.add_argument("--D", type=float, default=2e-5)
    parser.add_argument("--source-steps", type=int, default=50)
    parser.add_argument("--u", type=float, nargs="+", default=[0.001, 0.002, 0.003])
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
