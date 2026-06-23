#!/usr/bin/env python3
"""Dimensional transmutation / self-generated scale.

A dimensionless coupling obeys

    dg / d ln(mu) = - b g^2

and generates a scale

    Lambda = mu0 * exp(-1/(b g0))

This is known physics machinery (QCD-like), used here as a reduced check of how
a scale can arise from dimensionless input. It does not derive the absolute
Planck scale.
"""
from __future__ import annotations

import argparse
import math


def running_g(mu_over_mu0: float, g0: float, b: float) -> float:
    t = math.log(mu_over_mu0)
    return g0 / (1.0 + b * g0 * t)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--b", type=float, default=1.0)
    args = p.parse_args()

    print("## dimensional transmutation")
    print("| g0 | Lambda/mu0 = exp(-1/(b g0)) | hierarchy mu0/Lambda | reading |")
    print("|---:|---:|---:|---|")
    for g0 in [0.05, 0.08, 0.10, 0.15, 0.20]:
        lam = math.exp(-1.0 / (args.b * g0))
        print(f"| {g0:.3f} | {lam:.3e} | {1/lam:.3e} | small dimensionless change -> exponential scale hierarchy |")

    print("\n## running coupling sample")
    print("| mu/mu0 | g(mu) at g0=0.1 | reading |")
    print("|---:|---:|---|")
    for x in [1.0, 0.1, 0.01, 0.001, 1e-4]:
        denom = 1 + args.b * 0.1 * math.log(x)
        g = running_g(x, 0.1, args.b) if denom > 0 else float("inf")
        print(f"| {x:.4g} | {g:.4g} | coupling grows toward generated IR scale |")


if __name__ == "__main__":
    main()
