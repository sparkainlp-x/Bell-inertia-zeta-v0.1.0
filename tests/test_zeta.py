# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for Riemann's zeta: the Euler-Maclaurin sum, the zeros, the count."""
import numpy as np
import pytest

from bell_inertia_zeta import zeta


def test_zeta_at_two_is_pi_squared_over_six():
    assert zeta.zeta_em(2.0) == pytest.approx(np.pi ** 2 / 6.0, rel=1e-9)


def test_zeta_at_four_is_pi_to_the_fourth_over_ninety():
    assert zeta.zeta_em(4.0) == pytest.approx(np.pi ** 4 / 90.0, rel=1e-9)


def test_zeta_at_one_half():
    # zeta(1/2) = -1.4603545088095868 (established value).
    assert zeta.zeta_em(0.5) == pytest.approx(-1.4603545088, rel=1e-6)


def test_first_zero_is_at_fourteen_point_one_three():
    zeros = zeta.find_zeros()
    assert len(zeros) >= 1
    assert zeros[0] == pytest.approx(14.134725, abs=1e-3)


def test_ten_zeros_below_fifty():
    zeros = zeta.find_zeros()
    assert len(zeros) == 10
    for found, known in zip(zeros, zeta.KNOWN_ZEROS):
        assert found == pytest.approx(known, abs=1e-3)


def test_von_mangoldt_count_at_fifty():
    # N(50) ~ 9.43; the true count is 10.
    assert zeta.von_mangoldt_count(50.0) == pytest.approx(9.43, abs=0.05)
