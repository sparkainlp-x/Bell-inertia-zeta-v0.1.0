# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only
"""Moment of inertia of a solid sphere, by slicing into disks.

Slice the sphere (radius R, mass M, uniform density rho) into thin
disks at height z. A disk at height z has radius y with
y^2 = R^2 - z^2 and mass dm = rho pi y^2 dz, and a disk's moment of
inertia about the z axis is dI = (1/2) y^2 dm. So

    I = (1/2) rho pi int_{-R}^{R} y^4 dz
      = (1/2) rho pi int_{-R}^{R} (R^2 - z^2)^2 dz
      = (8/15) rho pi R^5.

With rho = M / (4/3 pi R^3), I = (2/5) M R^2. A thin spherical shell
of the same M and R has I_shell = (2/3) M R^2, so the solid sphere
carries 3/5 of the shell's inertia: its mass sits closer to the axis.

Here the disk-slice integral is done numerically (Simpson's rule) and
compared with the analytic (2/5) M R^2.
"""

from __future__ import annotations

import numpy as np


def density(mass: float, radius: float) -> float:
    """Uniform density of a solid sphere."""
    return float(mass) / (4.0 / 3.0 * np.pi * float(radius) ** 3)


def sphere_inertia_numeric(radius: float, mass: float, n_slices: int = 20001) -> float:
    """I of a solid sphere by numerically slicing it into disks (Simpson)."""
    r = float(radius)
    rho = density(mass, r)
    n = int(n_slices)
    if n % 2 == 0:
        n += 1  # Simpson's rule needs an odd number of points
    z = np.linspace(-r, r, n)
    y2 = r * r - z * z
    integrand = y2 * y2  # (R^2 - z^2)^2
    h = 2.0 * r / (n - 1)
    integral = h / 3.0 * (integrand[0] + integrand[-1]
                          + 4.0 * np.sum(integrand[1:-1:2])
                          + 2.0 * np.sum(integrand[2:-1:2]))
    return 0.5 * rho * np.pi * float(integral)


def sphere_inertia_analytic(radius: float, mass: float) -> float:
    """I = (2/5) M R^2."""
    return 0.4 * float(mass) * float(radius) ** 2


def shell_inertia_analytic(radius: float, mass: float) -> float:
    """I = (2/3) M R^2 for a thin spherical shell."""
    return (2.0 / 3.0) * float(mass) * float(radius) ** 2
