# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the moment of inertia: disk slicing, the 2/5 rule, the shell."""
import numpy as np
import pytest

from bell_inertia_zeta import inertia


def test_density_is_mass_over_volume():
    assert inertia.density(1.0, 1.0) == pytest.approx(3.0 / (4.0 * np.pi))
    assert inertia.density(3.0, 2.0) == pytest.approx(3.0 / (4.0 / 3.0 * np.pi * 8.0))


def test_numeric_sphere_matches_two_fifths():
    for radius, mass in [(1.0, 1.0), (2.0, 3.0), (0.5, 2.0)]:
        num = inertia.sphere_inertia_numeric(radius, mass)
        ana = inertia.sphere_inertia_analytic(radius, mass)
        assert num == pytest.approx(ana, rel=1e-6)


def test_sphere_carries_three_fifths_of_a_shell():
    for radius, mass in [(1.0, 1.0), (2.0, 3.0)]:
        ratio = inertia.sphere_inertia_numeric(radius, mass) \
            / inertia.shell_inertia_analytic(radius, mass)
        assert ratio == pytest.approx(0.6, rel=1e-6)


def test_shell_is_two_thirds():
    assert inertia.shell_inertia_analytic(1.0, 1.0) == pytest.approx(2.0 / 3.0)
    assert inertia.sphere_inertia_analytic(1.0, 1.0) == pytest.approx(0.4)
