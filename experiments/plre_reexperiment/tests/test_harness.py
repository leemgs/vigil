"""Offline checks of the harness logic with a mock LLM (no API calls).

The mock cites every passage it is shown and answers YES, so the tests check
plumbing (what each system shows, how stale citations are measured, how the
bootstrap behaves), not model quality. Nothing here produces paper results.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import compute_metrics as cm  # noqa: E402
import run_b5_plre as b5  # noqa: E402
import run_plre_infer as infer  # noqa: E402

PROMPTS: list[tuple[str, str]] = []


def fake_chat_json(system, user, temperature, seed=None):
    PROMPTS.append((system, user))
    ids = [line.split("doc_id=")[1].split()[0] for line in user.splitlines() if "doc_id=" in line]
    return {"label": "YES", "confidence": 0.9, "supporting_doc_ids": ids,
            "_usage": {"tokens_in": 10, "tokens_out": 5}}


@pytest.fixture(autouse=True)
def mock_llm(monkeypatch):
    PROMPTS.clear()
    monkeypatch.setattr(infer, "chat_json", fake_chat_json)
    monkeypatch.setattr(b5, "chat_json", fake_chat_json)


ROW = {
    "pair_id": "p1", "gold": "YES", "product_attribute": "a", "risk_theory": "t",
    "query_date": "2024-06-15", "is_stale_distractor": False,
    "passages": [
        {"doc_id": "open1", "decision_date": "2023-01-01", "text": "x", "validity_status": "open"},
        {"doc_id": "narrow1", "decision_date": "2022-01-01", "text": "x", "validity_status": "narrowed"},
        {"doc_id": "closed1", "decision_date": "2019-01-01", "text": "x", "validity_status": "closed"},
        {"doc_id": "future1", "decision_date": "2025-01-01", "text": "x", "validity_status": "open"},
    ],
}


def test_vigil_full_drops_closed_and_shows_labels():
    rec = infer.run_one(ROW, "vigil_full", 0)
    assert "closed1" not in rec["shown_doc_ids"]
    assert "validity=narrowed" in PROMPTS[-1][1]


def test_gate_only_drops_closed_and_hides_labels():
    rec = infer.run_one(ROW, "gate_only", 0)
    assert "closed1" not in rec["shown_doc_ids"]
    assert "validity=" not in PROMPTS[-1][1]


def test_no_gate_is_really_ungated():
    rec = infer.run_one(ROW, "vigil_no_gate", 0)
    system, user = PROMPTS[-1]
    assert "closed1" in rec["shown_doc_ids"]
    assert "validity=" not in user
    assert "closed" not in system.lower() and "overrul" not in system.lower()


def test_date_filter_uses_dates_only():
    rec = infer.run_one(ROW, "date_filter", 0)
    assert "future1" not in rec["shown_doc_ids"] and "closed1" in rec["shown_doc_ids"]
    assert "validity=" not in PROMPTS[-1][1]


def test_posthoc_filter_regenerates_after_citing_closed():
    rec = infer.run_one(ROW, "posthoc_filter", 0)
    assert rec["regenerated"] and rec["flagged_closed_ids"] == ["closed1"]
    assert "closed1" not in rec["shown_doc_ids"] and len(PROMPTS) == 2
    assert all("validity=" not in u for _, u in PROMPTS)


def test_b5_is_ungated_and_records_citations():
    rec = b5.run_b5(ROW, 0)
    assert all("validity=" not in u for _, u in PROMPTS)
    assert "closed1" in rec["supporting_doc_ids"]


def test_stale_is_measured_from_citations_not_self_report():
    closed = cm.closed_ids_by_pair([ROW])
    gated = dict(infer.run_one(ROW, "vigil_full", 0), stale_cited=True)  # bogus self-report
    ungated = infer.run_one(ROW, "vigil_no_gate", 0)
    g, u = cm.annotate([gated, ungated], closed)
    assert "stale_cited" not in g
    assert g["stale_pair"] is False and g["n_stale_cited"] == 0
    assert u["stale_pair"] is True and u["n_stale_cited"] == 1


def test_bootstrap_identical_systems_gives_zero():
    rows = [{"pair_id": f"p{i}", "gold": "YES" if i % 2 else "NO", "pred": "YES",
             "stale_pair": bool(i % 3 == 0)} for i in range(40)]
    res = cm.paired_bootstrap(rows, rows, n_boot=200, seed=0)
    assert res["d_f1"] == 0 and res["f1_ci"] == (0, 0) and res["d_stale"] == 0


def test_bootstrap_rejects_mismatched_gold():
    a = [{"pair_id": "p", "gold": "YES", "pred": "YES", "stale_pair": False}]
    b = [{"pair_id": "p", "gold": "NO", "pred": "YES", "stale_pair": False}]
    with pytest.raises(ValueError):
        cm.paired_bootstrap(a, b, n_boot=10, seed=0)


def test_f1_matches_hand_count():
    y = np.array([1, 1, 0, 0, 1]); p = np.array([1, 0, 1, 0, 1])
    prec, rec, f1 = cm.f1_arrays(y, p)
    assert (prec, rec) == (2 / 3, 2 / 3) and abs(f1 - 2 / 3) < 1e-12
