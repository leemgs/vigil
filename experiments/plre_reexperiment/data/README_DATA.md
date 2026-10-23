# Data file templates

## Quick start

1. Copy templates to working names:
   ```bash
   cp plre_test.template.jsonl plre_test.jsonl
   # edit plre_test.jsonl with your 372 held-out pairs
   ```
2. Keep **one JSON object per line** (no pretty-printed multi-line JSON).
3. Ensure every `pair_id` is unique within a file.
4. Set `validity_status` from your treatment graph for VIGIL runs.
5. Set `is_stale_distractor` consistently with how the pair was constructed.

## Minimal viable row

```json
{
  "pair_id": "plre_00001",
  "gold": "YES",
  "product_attribute": "...",
  "risk_theory": "...",
  "query_date": "2024-06-15",
  "is_stale_distractor": false,
  "passages": [
    {
      "doc_id": "op_1",
      "decision_date": "2023-01-01",
      "text": "...",
      "validity_status": "open"
    }
  ]
}
```

## Validation checklist

- [ ] `gold` is exactly `YES` or `NO`
- [ ] `query_date` and `decision_date` are `YYYY-MM-DD`
- [ ] At least one passage per pair
- [ ] `vigil_full` will drop passages with `validity_status == "closed"`
- [ ] About 19.7% of test pairs marked `is_stale_distractor: true` if matching the paper
- [ ] No API keys or real PII beyond public docket text

## Optional: empty shell generator

```bash
python - <<'PY'
import json
from pathlib import Path
# create N empty shells to fill
N = 10
out = Path("plre_test_shells.jsonl")
with out.open("w") as f:
    for i in range(1, N + 1):
        row = {
            "pair_id": f"plre_{i:05d}",
            "dispute_id": "",
            "split": "test",
            "gold": "YES",
            "product_attribute": "",
            "risk_theory": "",
            "query_date": "2024-01-01",
            "product_archetype": "",
            "is_stale_distractor": False,
            "year": 2024,
            "passages": [
                {
                    "doc_id": "",
                    "case_name": "",
                    "decision_date": "2023-01-01",
                    "court": "",
                    "text": "",
                    "validity_status": "open",
                    "rank": 1,
                    "score": 0.0,
                }
            ],
        }
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
print("wrote", out)
PY
```
