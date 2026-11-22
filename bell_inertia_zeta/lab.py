# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only
"""Bell + inertia + zeta: measured claims (bars frozen before evaluation).

Three new scientific outcomes, each measured in this laboratory from
its own first principles, not quoted:

- Bell (1964): the CHSH value of a local hidden-variable model stays
  at or below 2, while the quantum singlet reaches 2 sqrt(2); at equal
  settings the hidden-variable outcomes are perfectly anticorrelated.
- Inertia: the disk-slice integral of a solid sphere gives (2/5) M R^2,
  and the sphere carries 3/5 of a thin shell's inertia.
- Zeta (Riemann, 1859): the first ten zeros on the critical line,
  computed from scratch by Euler-Maclaurin summation, land on the
  established values; ten zeros sit below t = 50, as Riemann-von
  Mangoldt predicts.

Frozen seeds {42, 7, 1234, 2026, 2718} drive the Monte Carlo Bell
measurements (1,000,000 samples per correlation). The inertia and zeta
claims are deterministic; their seeds are not needed.

Claims
-------
(i)   Bell LHV: |S| <= 2.01 over all seeds (bar: 2.01).
(ii)  Bell quantum: |S| = 2 sqrt(2) (bar: within 1e-9).
(iii) Bell EPR: E(a, a) = -1 (bar: within 0.01, all angles and seeds).
(iv)  Inertia sphere: numerical I = (2/5) M R^2 (bar: within 1e-6).
(v)   Inertia ratio: I_sphere / I_shell = 3/5 (bar: within 1e-6).
(vi)  Zeta zeros: the first ten computed zeros match the established
      values (bar: within 1e-3).
(vii) Zeta count: ten zeros below t = 50 (bar: within 1 of the
      Riemann-von Mangoldt estimate).

A claim that fails is recorded as FAIL, honestly, with its measured
numbers. The test suite asserts the measurements are as computed and
the verdicts follow from them; it does not move a bar to force a pass.
"""

from __future__ import annotations

import numpy as np

from . import bell, inertia, zeta

FROZEN_SEEDS = (42, 7, 1234, 2026, 2718)
N_LHV = 1_000_000
BAR_LHV = 2.01
BAR_QUANTUM_REL = 1e-9
BAR_EPR = 0.01
BAR_INERTIA_REL = 1e-6
BAR_ZETA_ZERO = 1e-3
BAR_ZETA_COUNT = 1.0
INERTIA_CASES = [(1.0, 1.0), (2.0, 3.0), (0.5, 2.0)]


def claim_bell_lhv(seeds=FROZEN_SEEDS) -> dict:
    """(i) The local hidden-variable CHSH value stays at or below 2."""
    worst = 0.0
    for seed in seeds:
        worst = max(worst, bell.chsh_lhv(N_LHV, seed))
    verdict = "PASS" if worst <= BAR_LHV else "FAIL"
    return {"id": "(i)", "name": "bell-lhv", "verdict": verdict,
            "max_abs_s": float(worst), "bar": BAR_LHV}


def claim_bell_quantum() -> dict:
    """(ii) The quantum singlet CHSH value is 2 sqrt(2)."""
    measured = bell.chsh_quantum()
    expected = 2.0 * np.sqrt(2.0)
    rel = abs(measured - expected) / expected
    verdict = "PASS" if rel <= BAR_QUANTUM_REL else "FAIL"
    return {"id": "(ii)", "name": "bell-quantum", "verdict": verdict,
            "measured": float(measured), "expected": float(expected),
            "rel_err": float(rel), "bar": BAR_QUANTUM_REL}


def claim_bell_epr(seeds=FROZEN_SEEDS) -> dict:
    """(iii) At equal settings the hidden-variable outcomes are perfectly
    anticorrelated: E(a, a) = -1."""
    worst = 0.0
    for seed in seeds:
        for a in (0.0, np.pi / 4.0, np.pi / 2.0):
            e = bell.lhv_correlation(a, a, 100_000, seed)
            worst = max(worst, abs(e + 1.0))
    verdict = "PASS" if worst <= BAR_EPR else "FAIL"
    return {"id": "(iii)", "name": "bell-epr", "verdict": verdict,
            "worst_abs_err": float(worst), "bar": BAR_EPR}


def claim_inertia_sphere() -> dict:
    """(iv) The numerical disk-slice integral gives (2/5) M R^2."""
    worst = 0.0
    for radius, mass in INERTIA_CASES:
        num = inertia.sphere_inertia_numeric(radius, mass)
        ana = inertia.sphere_inertia_analytic(radius, mass)
        worst = max(worst, abs(num - ana) / ana)
    verdict = "PASS" if worst <= BAR_INERTIA_REL else "FAIL"
    return {"id": "(iv)", "name": "inertia-sphere", "verdict": verdict,
            "worst_rel_err": float(worst), "bar": BAR_INERTIA_REL}


def claim_inertia_ratio() -> dict:
    """(v) The solid sphere carries 3/5 of a thin shell's inertia."""
    worst = 0.0
    for radius, mass in INERTIA_CASES:
        ratio = inertia.sphere_inertia_numeric(radius, mass) \
            / inertia.shell_inertia_analytic(radius, mass)
        worst = max(worst, abs(ratio - 0.6) / 0.6)
    verdict = "PASS" if worst <= BAR_INERTIA_REL else "FAIL"
    return {"id": "(v)", "name": "inertia-ratio", "verdict": verdict,
            "worst_rel_err": float(worst), "expected": 0.6, "bar": BAR_INERTIA_REL}


def claim_zeta_zeros() -> dict:
    """(vi) The first ten computed zeros land on the established values."""
    found = zeta.find_zeros()
    if len(found) < len(zeta.KNOWN_ZEROS):
        return {"id": "(vi)", "name": "zeta-zeros", "verdict": "FAIL",
                "found": len(found), "expected": len(zeta.KNOWN_ZEROS),
                "worst_abs_err": float("nan"), "bar": BAR_ZETA_ZERO}
    worst = max(abs(f - k) for f, k in zip(found[:10], zeta.KNOWN_ZEROS))
    verdict = "PASS" if worst <= BAR_ZETA_ZERO else "FAIL"
    return {"id": "(vi)", "name": "zeta-zeros", "verdict": verdict,
            "found": len(found), "worst_abs_err": float(worst),
            "bar": BAR_ZETA_ZERO, "zeros": [float(z) for z in found[:10]]}


def claim_zeta_count() -> dict:
    """(vii) Ten zeros sit below t = 50, as Riemann-von Mangoldt predicts."""
    found = zeta.find_zeros()
    count = len(found)
    estimate = zeta.von_mangoldt_count(50.0)
    diff = abs(count - estimate)
    verdict = "PASS" if diff <= BAR_ZETA_COUNT else "FAIL"
    return {"id": "(vii)", "name": "zeta-count", "verdict": verdict,
            "count": int(count), "estimate": float(estimate),
            "diff": float(diff), "bar": BAR_ZETA_COUNT}


def evaluate_all(seeds=FROZEN_SEEDS) -> list[dict]:
    """Run every claim. Bars are frozen; verdicts are measured."""
    return [
        claim_bell_lhv(seeds),
        claim_bell_quantum(),
        claim_bell_epr(seeds),
        claim_inertia_sphere(),
        claim_inertia_ratio(),
        claim_zeta_zeros(),
        claim_zeta_count(),
    ]


def report(results: list[dict]) -> str:
    """One line per claim, plus the total. No headline is emitted."""
    lines = ["Bell + inertia + zeta -- measured claims (bars frozen before evaluation)", ""]
    for r in results:
        if r["id"] == "(i)":
            lines.append(f"(i) bell-lhv: {r['verdict']} -- max |S| {r['max_abs_s']:.4f} (bar <={r['bar']})")
        elif r["id"] == "(ii)":
            lines.append(f"(ii) bell-quantum: {r['verdict']} -- |S| {r['measured']:.6f}, "
                         f"expected 2 sqrt(2) = {r['expected']:.6f} (rel err {r['rel_err']:.2e}, bar {r['bar']})")
        elif r["id"] == "(iii)":
            lines.append(f"(iii) bell-epr: {r['verdict']} -- worst |E(a,a) + 1| "
                         f"{r['worst_abs_err']:.2e} (bar {r['bar']})")
        elif r["id"] == "(iv)":
            lines.append(f"(iv) inertia-sphere: {r['verdict']} -- worst rel err "
                         f"{r['worst_rel_err']:.2e} (bar {r['bar']})")
        elif r["id"] == "(v)":
            lines.append(f"(v) inertia-ratio: {r['verdict']} -- worst rel err "
                         f"{r['worst_rel_err']:.2e} (bar {r['bar']}), expected ratio {r['expected']}")
        elif r["id"] == "(vi)":
            lines.append(f"(vi) zeta-zeros: {r['verdict']} -- {r['found']} zeros found, "
                         f"worst |t - known| {r['worst_abs_err']:.2e} (bar {r['bar']})")
        elif r["id"] == "(vii)":
            lines.append(f"(vii) zeta-count: {r['verdict']} -- count {r['count']}, "
                         f"Riemann-von Mangoldt estimate {r['estimate']:.2f} (diff {r['diff']:.2f}, bar {r['bar']})")
    n_pass = sum(1 for r in results if r["verdict"] == "PASS")
    lines.append("")
    lines.append(f"{n_pass}/{len(results)} claims pass. Synthetic, classical. No headline.")
    return "\n".join(lines)
