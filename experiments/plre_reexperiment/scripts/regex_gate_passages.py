#!/usr/bin/env python3
"""Optional: rewrite validity_status using a keyword heuristic on passage text.

Usage:
  python regex_gate_passages.py --input ../data/plre_test.jsonl --output ../data/plre_test_regex.jsonl

Then:
  python run_plre_infer.py --input ../data/plre_test_regex.jsonl --systems vigil_full
  # (vigil_full filter drops validity_status==closed from regex)
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

NEG = re.compile(
    r"\b(overruled|superseded|abrogated|overturned|no longer good law)\b",
    re.I,
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    with args.input.open() as fin, args.output.open("w") as fout:
        for line in fin:
            if not line.strip():
                continue
            row = json.loads(line)
            new_passages = []
            for p in row.get("passages", []):
                p = dict(p)
                if NEG.search(str(p.get("text", ""))):
                    p["validity_status"] = "closed"
                else:
                    # keep open unless previously closed and you prefer stricter logic
                    p["validity_status"] = p.get("validity_status") or "open"
                new_passages.append(p)
            row["passages"] = new_passages
            fout.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
