#!/usr/bin/env python3
"""Run the single-call PLRE conditions on held-out pairs.

Systems (all share one LLM call per pair, so they are compared under the same
harness; this is a controlled re-run, not the full agentic VIGIL pipeline):

  vigil_full      drop closed passages; show open/narrowed/cautionary labels
  gate_only       drop closed passages; hide the remaining labels
                  (analogue of "- treatment weighting" in Table 4)
  vigil_no_gate   keep every passage; hide all labels
  date_filter     keep passages with decision_date <= query_date; hide labels
  posthoc_filter  run vigil_no_gate; if the answer cites a closed passage,
                  drop closed passages and regenerate once (post-hoc check)

Usage:
  export OPENAI_API_KEY=sk-...
  python run_plre_infer.py --input ../data/plre_test.jsonl \
      --systems vigil_full,gate_only,vigil_no_gate,date_filter,posthoc_filter

Output:
  ../outputs/preds_{system}_seed{seed}.jsonl
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from config import DATA_DIR, OUT_DIR, SEEDS, TEMP_CTRL
from llm_client import chat_json, extract_label
from prompts import (
    SYSTEM_PLRE_DATE_ONLY,
    SYSTEM_PLRE_GATE_ONLY,
    SYSTEM_PLRE_GATED,
    SYSTEM_PLRE_UNGATED,
    user_plre,
)

SYSTEMS = ("vigil_full", "gate_only", "vigil_no_gate", "date_filter", "posthoc_filter")


def load_jsonl(path: Path) -> list[dict]:
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def drop_closed(passages: list[dict]) -> list[dict]:
    return [p for p in passages if p.get("validity_status") != "closed"]


def date_filter(passages: list[dict], query_date: str) -> list[dict]:
    # ISO dates (YYYY-MM-DD) compare correctly as strings.
    return [p for p in passages if str(p.get("decision_date", "")) <= str(query_date)]


def cited_ids(obj: dict) -> list[str]:
    ids = obj.get("supporting_doc_ids") or []
    return [str(i) for i in ids] if isinstance(ids, list) else []


def call(system_prompt: str, row: dict, passages: list[dict], include_validity: bool, seed: int):
    obj = chat_json(system_prompt, user_plre(row, passages, include_validity), temperature=TEMP_CTRL, seed=seed)
    usage = obj.pop("_usage", {})
    return obj, usage


def run_one(row: dict, system: str, seed: int) -> dict:
    passages = row.get("passages", [])
    extra: dict = {}

    if system == "vigil_full":
        shown = drop_closed(passages)
        obj, usage = call(SYSTEM_PLRE_GATED, row, shown, True, seed)
    elif system == "gate_only":
        shown = drop_closed(passages)
        obj, usage = call(SYSTEM_PLRE_GATE_ONLY, row, shown, False, seed)
    elif system == "vigil_no_gate":
        shown = passages
        obj, usage = call(SYSTEM_PLRE_UNGATED, row, shown, False, seed)
    elif system == "date_filter":
        shown = date_filter(passages, row["query_date"])
        obj, usage = call(SYSTEM_PLRE_DATE_ONLY, row, shown, False, seed)
    elif system == "posthoc_filter":
        shown = passages
        obj, usage = call(SYSTEM_PLRE_UNGATED, row, shown, False, seed)
        closed = {str(p.get("doc_id")) for p in passages if p.get("validity_status") == "closed"}
        first_ids = cited_ids(obj)
        flagged = sorted(set(first_ids) & closed)
        extra = {"first_pass_label": extract_label(obj), "first_pass_ids": first_ids,
                 "flagged_closed_ids": flagged, "regenerated": bool(flagged)}
        if flagged:
            shown = drop_closed(passages)
            obj, usage2 = call(SYSTEM_PLRE_UNGATED, row, shown, False, seed)
            usage = {k: (usage.get(k) or 0) + (usage2.get(k) or 0) for k in set(usage) | set(usage2)}
    else:
        raise ValueError(f"unknown system {system!r}; choose from {SYSTEMS}")

    return {
        "experiment": "plre_infer",
        "system": system,
        "pair_id": row["pair_id"],
        "dispute_id": row.get("dispute_id"),
        "seed": seed,
        "gold": str(row["gold"]).upper(),
        "pred": extract_label(obj),
        "confidence": obj.get("confidence"),
        "supporting_doc_ids": cited_ids(obj),
        "shown_doc_ids": [str(p.get("doc_id")) for p in shown],
        "is_stale_distractor": bool(row.get("is_stale_distractor", False)),
        **extra,
        **usage,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, default=DATA_DIR / "plre_test.jsonl")
    ap.add_argument("--systems", default="vigil_full,vigil_no_gate", help=f"Comma list from {SYSTEMS}")
    ap.add_argument("--limit", type=int, default=0, help="If >0, only the first N pairs (smoke test)")
    args = ap.parse_args()

    rows = load_jsonl(args.input)
    if args.limit > 0:
        rows = rows[: args.limit]
    systems = [s.strip() for s in args.systems.split(",") if s.strip()]
    for s in systems:
        if s not in SYSTEMS:
            raise SystemExit(f"unknown system {s!r}; choose from {SYSTEMS}")

    for system in systems:
        for seed in SEEDS:
            out_path = OUT_DIR / f"preds_{system}_seed{seed}.jsonl"
            done = set()
            if out_path.exists():
                done = {json.loads(line)["pair_id"] for line in out_path.open() if line.strip()}
            with out_path.open("a" if done else "w") as out:
                for row in rows:
                    if row["pair_id"] in done:
                        continue
                    out.write(json.dumps(run_one(row, system, seed), ensure_ascii=False) + "\n")
                    out.flush()
            print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
