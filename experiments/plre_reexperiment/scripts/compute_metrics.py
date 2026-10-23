#!/usr/bin/env python3
"""PLRE metrics with paired bootstrap CIs, from per-instance prediction files.

Stale citations are measured, not self-reported: a citation is stale when the
cited doc_id has validity_status == "closed" in the input data (the paper's
definition, t_q >= e_v). Two rates are reported:
  stale_pair  share of pairs whose decision cites at least one closed passage
  stale_cite  share of all citations that point to a closed passage

Usage:
  python compute_metrics.py --data ../data/plre_test.jsonl \
      --pred-glob "../outputs/preds_*.jsonl" --reference vigil_full

Prints, per system: P/R/F1 (positive class YES), stale rates, and unknown
citations (doc_ids that were not shown to the system), on all pairs and on the
non-distractor subset; F1 mean/std over seeds; and paired bootstrap 95% CIs of
F1 and stale_pair differences between the reference system and every other.
"""
from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path

import numpy as np


def load_jsonl(path: Path) -> list[dict]:
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def closed_ids_by_pair(data: list[dict]) -> dict[str, set[str]]:
    return {
        r["pair_id"]: {str(p.get("doc_id")) for p in r.get("passages", []) if p.get("validity_status") == "closed"}
        for r in data
    }


def annotate(rows: list[dict], closed: dict[str, set[str]]) -> list[dict]:
    """Add measured stale flags; drop the model's own stale_cited if present."""
    out = []
    for r in rows:
        r = dict(r)
        r.pop("stale_cited", None)
        ids = [str(i) for i in r.get("supporting_doc_ids") or []]
        cl = closed.get(r["pair_id"], set())
        shown = set(r.get("shown_doc_ids") or [])
        r["n_cited"] = len(ids)
        r["n_stale_cited"] = sum(i in cl for i in ids)
        r["stale_pair"] = r["n_stale_cited"] > 0
        r["n_unknown_cited"] = sum(i not in shown for i in ids) if shown else 0
        out.append(r)
    return out


def f1_arrays(y: np.ndarray, p: np.ndarray) -> tuple[float, float, float]:
    tp = float(np.sum((y == 1) & (p == 1)))
    fp = float(np.sum((y == 0) & (p == 1)))
    fn = float(np.sum((y == 1) & (p == 0)))
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return prec, rec, f1


def yp(rows: list[dict]) -> tuple[np.ndarray, np.ndarray]:
    return (np.array([r["gold"] == "YES" for r in rows], dtype=int),
            np.array([r["pred"] == "YES" for r in rows], dtype=int))


def summarize(rows: list[dict]) -> str:
    if not rows:
        return "n=0"
    y, p = yp(rows)
    prec, rec, f1 = f1_arrays(y, p)
    cites = sum(r["n_cited"] for r in rows)
    stale_cite = sum(r["n_stale_cited"] for r in rows) / cites if cites else 0.0
    stale_pair = float(np.mean([r["stale_pair"] for r in rows]))
    unknown = sum(r["n_unknown_cited"] for r in rows)
    return (f"n={len(rows)} P={prec:.3f} R={rec:.3f} F1={f1:.3f} "
            f"stale_pair={stale_pair:.3f} stale_cite={stale_cite:.3f} unknown_cited={unknown}")


def paired_bootstrap(rows_a: list[dict], rows_b: list[dict], n_boot: int, seed: int) -> dict:
    """Paired by pair_id. Returns differences a - b for F1 and stale_pair with 95% CIs."""
    a = {r["pair_id"]: r for r in rows_a}
    b = {r["pair_id"]: r for r in rows_b}
    ids = sorted(set(a) & set(b))
    if not ids:
        raise ValueError("no overlapping pair_ids")
    if any(a[i]["gold"] != b[i]["gold"] for i in ids):
        raise ValueError("gold labels differ between systems for the same pair_id")
    y = np.array([a[i]["gold"] == "YES" for i in ids], dtype=int)
    pa = np.array([a[i]["pred"] == "YES" for i in ids], dtype=int)
    pb = np.array([b[i]["pred"] == "YES" for i in ids], dtype=int)
    sa = np.array([a[i]["stale_pair"] for i in ids], dtype=float)
    sb = np.array([b[i]["stale_pair"] for i in ids], dtype=float)

    def stats(idx):
        return f1_arrays(y[idx], pa[idx])[2] - f1_arrays(y[idx], pb[idx])[2], sa[idx].mean() - sb[idx].mean()

    point = stats(np.arange(len(ids)))
    rng = np.random.default_rng(seed)
    boots = np.array([stats(rng.integers(0, len(ids), size=len(ids))) for _ in range(n_boot)])
    lo, hi = np.percentile(boots, [2.5, 97.5], axis=0)
    return {"n": len(ids), "d_f1": point[0], "f1_ci": (lo[0], hi[0]),
            "d_stale": point[1], "stale_ci": (lo[1], hi[1])}


def select(rows: list[dict], system: str, seed: int | None) -> list[dict]:
    return [r for r in rows if r["system"] == system and (seed is None or r.get("seed") == seed)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, required=True, help="Input pairs with passage validity_status")
    ap.add_argument("--pred-glob", default="../outputs/preds_*.jsonl")
    ap.add_argument("--reference", default="vigil_full")
    ap.add_argument("--seed", type=int, default=0, help="Seed used for point estimates and CIs")
    ap.add_argument("--n-boot", type=int, default=10_000)
    ap.add_argument("--boot-seed", type=int, default=0)
    args = ap.parse_args()

    paths = [Path(p) for p in sorted(glob.glob(args.pred_glob))]
    if not paths:
        raise SystemExit(f"No prediction files matched {args.pred_glob}")
    data = load_jsonl(args.data)
    rows = annotate([r for p in paths for r in load_jsonl(p)], closed_ids_by_pair(data))
    systems = sorted({r["system"] for r in rows})
    print("Systems:", systems)

    for label, keep in (("all pairs", lambda r: True), ("non-distractor pairs", lambda r: not r["is_stale_distractor"])):
        print(f"\n== Point estimates, {label}, seed={args.seed}")
        for s in systems:
            print(f"  {s:15s} {summarize([r for r in select(rows, s, args.seed) if keep(r)])}")

    print("\n== F1 over seeds (mean +/- std; decoding/exemplar variation only, not a CI)")
    for s in systems:
        f1s = [f1_arrays(*yp(select(rows, s, sd)))[2] for sd in sorted({r.get('seed') for r in select(rows, s, None)})]
        print(f"  {s:15s} {np.mean(f1s):.3f} +/- {np.std(f1s):.3f} over {len(f1s)} seed(s)")

    if args.reference not in systems:
        print(f"\nReference system {args.reference!r} not found; skipping paired CIs.")
        return
    for label, keep in (("all pairs", lambda r: True), ("non-distractor pairs", lambda r: not r["is_stale_distractor"])):
        print(f"\n== Paired bootstrap 95% CI, {args.reference} minus other, {label} (n_boot={args.n_boot})")
        ref = [r for r in select(rows, args.reference, args.seed) if keep(r)]
        for s in systems:
            if s == args.reference:
                continue
            other = [r for r in select(rows, s, args.seed) if keep(r)]
            res = paired_bootstrap(ref, other, args.n_boot, args.boot_seed)
            print(f"  vs {s:15s} n={res['n']}  dF1={res['d_f1']:+.3f} [{res['f1_ci'][0]:+.3f}, {res['f1_ci'][1]:+.3f}]"
                  f"  dStale_pair={res['d_stale']:+.3f} [{res['stale_ci'][0]:+.3f}, {res['stale_ci'][1]:+.3f}]")


if __name__ == "__main__":
    main()
