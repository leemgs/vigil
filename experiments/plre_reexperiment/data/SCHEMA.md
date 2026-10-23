# PLRE re-experiment data schema

All files are **JSON Lines** (`.jsonl`): one JSON object per line, UTF-8.

## Required for the four priority experiments

| File | Required? | Purpose |
|------|-----------|---------|
| `plre_test.jsonl` | **Yes** | Held-out PLRE pairs (main evaluation) |
| `plre_train.jsonl` | Optional | Few-shot exemplars / threshold tuning |
| `plre_val.jsonl` | Optional | Threshold selection |
| `dispute_map.csv` | Optional | Dispute-level split audit |
| `triage_test.jsonl` | Optional | Severity triage $n{=}82$ (secondary) |

## `validity_status` values

| Value | Meaning |
|-------|---------|
| `open` | Still fully operative |
| `closed` | Overruled / superseded (hard-exclude under `vigil_full`) |
| `narrowed` | Material narrowing (down-weight; still allowed as support) |
| `cautionary` | Distinguishes / weak negative (down-weight) |
| `unknown` | No treatment info (treat as open unless you prefer stricter rules) |

## `gold` / `pred` labels

- PLRE: `YES` or `NO` (uppercase)
- Triage severity (if used): `High` | `Medium` | `Low`
