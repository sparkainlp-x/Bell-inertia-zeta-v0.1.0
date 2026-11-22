# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for Bell's theorem: the singlet, the LHV model, CHSH."""
import numpy as np
import pytest

from bell_inertia_zeta import bell


def test_quantum_correlation_is_minus_cos():
    assert bell.quantum_correlation(0.0, 0.0) == pytest.approx(-1.0)
    assert bell.quantum_correlation(0.0, np.pi / 2) == pytest.approx(0.0, abs=1e-12)
    assert bell.quantum_correlation(0.0, np.pi) == pytest.approx(1.0)


def test_quantum_chsh_is_two_root_two():
    assert bell.chsh_quantum() == pytest.approx(2.0 * np.sqrt(2.0), rel=1e-9)


def test_lhv_correlation_matches_the_triangle_wave():
    # E(a, b) = 2|a - b| / pi - 1 for |a - b| <= pi.
    for a, b, expected in [(0.0, 0.0, -1.0), (0.0, np.pi / 2, 0.0),
                           (0.0, np.pi / 4, -0.5), (np.pi / 2, np.pi / 4, -0.5)]:
        measured = bell.lhv_correlation(a, b, 200_000, 42)
        assert measured == pytest.approx(expected, abs=0.02)


def test_lhv_anticorrelation_at_equal_settings():
    for a in (0.0, np.pi / 4, np.pi / 2):
        assert bell.lhv_correlation(a, a, 100_000, 7) == pytest.approx(-1.0, abs=0.01)


def test_lhv_chsh_stays_at_or_below_two():
    # The LHV model saturates the bound; Monte Carlo noise is ~0.002.
    assert bell.chsh_lhv(500_000, 1234) <= 2.01
