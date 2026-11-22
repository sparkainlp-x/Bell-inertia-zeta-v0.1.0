# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only
"""Riemann's zeta function and its zeros on the critical line.

Riemann (1859) posed the zeta function

    zeta(s) = sum_{n=1}^{inf} 1 / n^s

and the hypothesis that every nontrivial zero lies on the critical
line Re(s) = 1/2. The first zeros (imaginary parts, established values
from the standard tables) are at t = 14.134725, 21.022040, 25.010858,
30.424876, 32.935062, 37.586178, 40.918719, 43.327073, 48.005151,
49.773832.

Here zeta(s) is computed from scratch by Euler-Maclaurin summation:

    zeta(s) = sum_{n=1}^{N-1} n^{-s} + N^{1-s}/(s-1) + (1/2) N^{-s}
              + sum_{k=1}^{K} B_{2k}/(2k)! * s(s+1)...(s+2k-2)
                * N^{-s-2k+1},

with N = 100 and K = 6. The zeros are found by scanning |zeta(1/2 + it)|
for local minima and refining each by golden-section search. The count
below t = 50 is compared with the Riemann-von Mangoldt formula
N(T) ~ (T/2 pi) log(T/2 pi) - T/2 pi + 7/8.
"""

from __future__ import annotations

import math

import numpy as np

BERNOULLI = {2: 1.0 / 6.0, 4: -1.0 / 30.0, 6: 1.0 / 42.0,
             8: -1.0 / 30.0, 10: 5.0 / 66.0, 12: -691.0 / 2730.0}

# Established first ten zeros on the critical line (imaginary parts),
# the reference the computation is checked against.
KNOWN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
               37.586178, 40.918719, 43.327073, 48.005151, 49.773832]


def zeta_em(s: complex, n_terms: int = 100, k_max: int = 6) -> complex:
    """zeta(s) by Euler-Maclaurin summation (works for Re(s) > 0 here)."""
    s = complex(s)
    total = 0j
    for n in range(1, int(n_terms)):
        total += n ** (-s)
    total += n_terms ** (1.0 - s) / (s - 1.0)
    total += 0.5 * n_terms ** (-s)
    for k in range(1, int(k_max) + 1):
        rising = 1.0 + 0j
        for j in range(2 * k - 1):
            rising *= (s + j)
        total += (BERNOULLI[2 * k] / math.factorial(2 * k)) * rising \
            * n_terms ** (-s - 2 * k + 1)
    return complex(total)


def zeta_critical(t: float) -> complex:
    """zeta(1/2 + i t)."""
    return zeta_em(0.5 + 1j * float(t))


def _golden_min(f, a: float, b: float, tol: float = 1e-10) -> float:
    """Golden-section minimisation of f on [a, b]."""
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    c = b - gr * (b - a)
    d = a + gr * (b - a)
    fc, fd = f(c), f(d)
    while abs(b - a) > tol:
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - gr * (b - a)
            fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + gr * (b - a)
            fd = f(d)
    return 0.5 * (a + b)


def find_zeros(t_max: float = 50.0, step: float = 0.01,
               threshold: float = 0.05) -> list[float]:
    """The zeros of zeta on the critical line with 0 < t < t_max.

    Scan |zeta(1/2 + i t)| for local minima below the threshold, then
    refine each by golden-section search.
    """
    ts = np.arange(0.5, float(t_max), float(step))
    mags = np.array([abs(zeta_critical(float(t))) for t in ts])
    zeros = []
    for i in range(1, len(ts) - 1):
        if mags[i] < threshold and mags[i] <= mags[i - 1] and mags[i] <= mags[i + 1]:
            t0 = _golden_min(lambda t: abs(zeta_critical(t)),
                             float(ts[i] - step), float(ts[i] + step))
            if not zeros or abs(t0 - zeros[-1]) > 0.5:
                zeros.append(float(t0))
    return zeros


def von_mangoldt_count(t: float) -> float:
    """N(T) ~ (T/2 pi) log(T/2 pi) - T/2 pi + 7/8."""
    t = float(t)
    return (t / (2.0 * np.pi)) * math.log(t / (2.0 * np.pi)) - t / (2.0 * np.pi) + 7.0 / 8.0
