# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the lab: every claim's verdict follows from its numbers."""
import numpy as np
import pytest

from bell_inertia_zeta import lab


def test_claim_bell_lhv_verdict_follows_its_numbers():
    r = lab.claim_bell_lhv()
    assert r["verdict"] == ("PASS" if r["max_abs_s"] <= r["bar"] else "FAIL")


def test_claim_bell_quantum_verdict_follows_its_numbers():
    r = lab.claim_bell_quantum()
    assert r["verdict"] == ("PASS" if r["rel_err"] <= r["bar"] else "FAIL")


def test_claim_bell_epr_verdict_follows_its_numbers():
    r = lab.claim_bell_epr()
    assert r["verdict"] == ("PASS" if r["worst_abs_err"] <= r["bar"] else "FAIL")


def test_claim_inertia_sphere_verdict_follows_its_numbers():
    r = lab.claim_inertia_sphere()
    assert r["verdict"] == ("PASS" if r["worst_rel_err"] <= r["bar"] else "FAIL")


def test_claim_inertia_ratio_verdict_follows_its_numbers():
    r = lab.claim_inertia_ratio()
    assert r["verdict"] == ("PASS" if r["worst_rel_err"] <= r["bar"] else "FAIL")


def test_claim_zeta_zeros_verdict_follows_its_numbers():
    r = lab.claim_zeta_zeros()
    if r["verdict"] == "PASS":
        assert r["worst_abs_err"] <= r["bar"]
        assert r["found"] >= len(lab.zeta.KNOWN_ZEROS)


def test_claim_zeta_count_verdict_follows_its_numbers():
    r = lab.claim_zeta_count()
    assert r["verdict"] == ("PASS" if r["diff"] <= r["bar"] else "FAIL")


def test_evaluate_all_returns_seven_claims_with_verdicts():
    results = lab.evaluate_all()
    assert len(results) == 7
    assert [r["id"] for r in results] == ["(i)", "(ii)", "(iii)", "(iv)", "(v)", "(vi)", "(vii)"]
    assert all(r["verdict"] in ("PASS", "FAIL") for r in results)
    text = lab.report(results)
    assert "TODO" not in text and "TO COMPLETE" not in text
    assert "No headline" in text
