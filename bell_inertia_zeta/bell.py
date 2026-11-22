# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only
"""Bell's theorem: the EPR paradox, measured.

Bell (1964, Physics 1, 195-200) showed that no local hidden-variable
theory can reproduce the statistical predictions of quantum mechanics
for the singlet state. The CHSH form (Clauser, Horne, Shimony, Holt,
1969) is the testable version: for measurement angles a, a' (Alice)
and b, b' (Bob),

    S = E(a,b) - E(a,b') + E(a',b) + E(a',b'),

any local hidden-variable theory gives |S| <= 2, while quantum
mechanics reaches 2 sqrt(2) at a = 0, a' = pi/2, b = pi/4, b' = 3 pi/4.

Here both sides are computed in the same laboratory. The quantum side
is the singlet correlation E(a,b) = -cos(a - b). The classical side is
a local hidden-variable model: each pair carries a hidden variable
lambda uniform on [0, 2 pi); Alice's outcome is sign(cos(lambda - a)),
Bob's is -sign(cos(lambda - b)). That model gives the triangle-wave
correlation E(a,b) = 2|a - b|/pi - 1 (for |a - b| <= pi), which
saturates the bound at |S| = 2 and never exceeds it. The EPR point is
also measured: at equal settings the outcomes are perfectly
anticorrelated, E(a,a) = -1, so the result is predetermined by lambda.
"""

from __future__ import annotations

import numpy as np

# Standard CHSH angles: a = 0, a' = pi/2, b = pi/4, b' = 3 pi/4.
CHSH_ANGLES = (0.0, np.pi / 2.0, np.pi / 4.0, 3.0 * np.pi / 4.0)


def quantum_correlation(a: float, b: float) -> float:
    """Singlet correlation: E(a, b) = -cos(a - b)."""
    return float(-np.cos(float(a) - float(b)))


def chsh_quantum() -> float:
    """|S| from the quantum singlet correlation at the standard angles."""
    a, a_prime, b, b_prime = CHSH_ANGLES
    s = (quantum_correlation(a, b) - quantum_correlation(a, b_prime)
         + quantum_correlation(a_prime, b) + quantum_correlation(a_prime, b_prime))
    return abs(float(s))


def lhv_correlation(a: float, b: float, n: int, seed: int) -> float:
    """Monte Carlo correlation of the local hidden-variable model.

    lambda uniform on [0, 2 pi). A = sign(cos(lambda - a)),
    B = -sign(cos(lambda - b)). E = mean(A * B).
    """
    rng = np.random.default_rng(seed)
    lam = rng.uniform(0.0, 2.0 * np.pi, size=int(n))
    outcome_a = np.sign(np.cos(lam - float(a)))
    outcome_b = -np.sign(np.cos(lam - float(b)))
    return float(np.mean(outcome_a * outcome_b))


def chsh_lhv(n: int, seed: int) -> float:
    """|S| from the local hidden-variable model at the standard angles."""
    a, a_prime, b, b_prime = CHSH_ANGLES
    s = (lhv_correlation(a, b, n, seed) - lhv_correlation(a, b_prime, n, seed)
         + lhv_correlation(a_prime, b, n, seed)
         + lhv_correlation(a_prime, b_prime, n, seed))
    return abs(float(s))
