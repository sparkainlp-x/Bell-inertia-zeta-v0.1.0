# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only
"""Bell + inertia + zeta: three measured scientific outcomes.

Bell's theorem (1964), the moment of inertia of a solid sphere, and
Riemann's zeta zeros -- each measured in this laboratory from its own
first principles. Synthetic and classical.
"""

from . import bell, inertia, lab, zeta
from .lab import evaluate_all, report

__all__ = ["bell", "evaluate_all", "inertia", "lab", "report", "zeta"]
