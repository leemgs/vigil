#!/usr/bin/env bash
# Run every single-call PLRE condition, B5, and the metrics.
set -euo pipefail
cd "$(dirname "$0")"

INPUT="${1:-../data/plre_test.jsonl}"
if [[ ! -f "$INPUT" ]]; then
  echo "Missing $INPUT: put the 372 held-out pairs there (see ../data/README_DATA.md)." >&2
  exit 1
fi

python run_plre_infer.py --input "$INPUT" \
  --systems vigil_full,gate_only,vigil_no_gate,date_filter,posthoc_filter
python run_b5_plre.py --input "$INPUT"
python compute_metrics.py --data "$INPUT" --pred-glob "../outputs/preds_*.jsonl" \
  --reference vigil_full --seed 0 --n-boot 10000 | tee ../outputs/metrics_seed0.txt
