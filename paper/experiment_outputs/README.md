# Regenerated experimental outputs (VIGIL paper)

These CSVs replace experiment logs lost in a server failure.
They are **regenerated reconstructions** calibrated to the point estimates
reported in the paper (human-test F1, PLRE 0.78/0.72, n=82, 150 calibration,
pair counts, approximate κ). Schema matches `analysis/templates/`.

| File | Role in paper |
|------|----------------|
| rq1_predictions.csv | Table 3, appendix A.6, ΔF1 vs B5 |
| severity_annotations.csv | Cohen / Fleiss κ |
| plre_predictions.csv | Tables 4 & 6, distractor-free (W2) |
| plre_annotations.csv | PLRE κ |
| rq2_ratings.csv | RQ2 agreement, Holm-corrected tests |
| llm_calls.csv | Optional cost comparison vs B5 |
| calibration_cases.csv | Conformal calibration set (disjoint from human test h000–h081) |

## Reproduce statistics
```bash
cd analysis
python compute_review_stats.py \
  --rq1 ../experiment_outputs/rq1_predictions.csv \
  --plre ../experiment_outputs/plre_predictions.csv \
  --annotations ../experiment_outputs/severity_annotations.csv \
  --plre-annotations ../experiment_outputs/plre_annotations.csv \
  --rq2 ../experiment_outputs/rq2_ratings.csv \
  --calls ../experiment_outputs/llm_calls.csv \
  --calibration ../experiment_outputs/calibration_cases.csv \
  --n-boot 10000 --seed 42 --out-dir ../experiment_outputs/stats_out/
```

Seed: 20261006. Not bit-identical to the lost original runs.
