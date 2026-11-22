# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only
.PHONY: test run clean

test:
	python3 -m pytest tests/ -q

run:
	python3 -m bell_inertia_zeta

clean:
	rm -rf __pycache__ bell_inertia_zeta/__pycache__ tests/__pycache__ .pytest_cache
