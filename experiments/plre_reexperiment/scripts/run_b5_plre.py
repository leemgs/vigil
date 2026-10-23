#!/usr/bin/env python3
"""Iteration-matched self-refinement baseline (B5) on PLRE.

B5 sees every passage without validity metadata (flat RAG) and revises its
answer for up to PLRE_B5_MAX_ITERS iterations. Set PLRE_B5_MAX_TOKENS to
stop on a completion-token budget instead (token-matched variant).

Usage:
  python run_b5_plre.py --input ../data/plre_test.jsonl
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from config import B5_MAX_COMPLETION_TOKENS, B5_MAX_ITERS, DATA_DIR, OUT_DIR, SEEDS, TEMP_CTRL
from llm_client import chat_json, extract_label
from prompts import SYSTEM_B5, format_passages


def load_jsonl(path: Path) -> list[dict]:
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def run_b5(row: dict, seed: int) -> dict:
    passages = row.get("passages", [])
    system = SYSTEM_B5.format(max_iters=B5_MAX_ITERS)
    history = []
    total_out = 0
    last: dict = {}

    for it in range(1, B5_MAX_ITERS + 1):
        user = (
            f"Iteration {it}/{B5_MAX_ITERS}\n"
            f"product_attribute: {row['product_attribute']}\n"
            f"risk_theory: {row['risk_theory']}\n"
            f"query_date: {row['query_date']}\n\n"
            f"passages:\n{format_passages(passages, include_validity=False)}\n\n"
        )
        if history:
            user += "Previous draft/critique:\n" + json.dumps(history[-1]["draft"], ensure_ascii=False) + "\n"
        user += "Produce an updated JSON decision. On the final iteration, finalize label."
        obj = chat_json(system, user, temperature=TEMP_CTRL, seed=seed + it)
        usage = obj.pop("_usage", {})
        total_out += int(usage.get("tokens_out") or 0)
        last = obj
        history.append({"iteration": it, "draft": obj, "usage": usage})
        if B5_MAX_COMPLETION_TOKENS and total_out >= B5_MAX_COMPLETION_TOKENS:
            break

    ids = last.get("supporting_doc_ids") or []
    return {
        "experiment": "b5_plre",
        "system": "b5",
        "pair_id": row["pair_id"],
        "dispute_id": row.get("dispute_id"),
        "seed": seed,
        "gold": str(row["gold"]).upper(),
        "pred": extract_label(last),
        "confidence": last.get("confidence"),
        "supporting_doc_ids": [str(i) for i in ids] if isinstance(ids, list) else [],
        "shown_doc_ids": [str(p.get("doc_id")) for p in passages],
        "is_stale_distractor": bool(row.get("is_stale_distractor", False)),
        "iterations_used": len(history),
        "tokens_out_total": total_out,
        "history": history,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, default=DATA_DIR / "plre_test.jsonl")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    rows = load_jsonl(args.input)
    if args.limit > 0:
        rows = rows[: args.limit]

    for seed in SEEDS:
        out_path = OUT_DIR / f"preds_b5_seed{seed}.jsonl"
        done = set()
        if out_path.exists():
            done = {json.loads(line)["pair_id"] for line in out_path.open() if line.strip()}
        with out_path.open("a" if done else "w") as out:
            for row in rows:
                if row["pair_id"] in done:
                    continue
                out.write(json.dumps(run_b5(row, seed), ensure_ascii=False) + "\n")
                out.flush()
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
