# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only
"""Run the laboratory: python -m bell_inertia_zeta."""

from .lab import evaluate_all, report


def main() -> None:
    print(report(evaluate_all()))


if __name__ == "__main__":
    main()
