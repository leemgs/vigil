# ACL submission update (2026-10-10)

## System rename
- Renamed system from **ALERT** (Agentic Legal Exposure and Risk Tracking) to **VIGIL** (**V**alidity-**I**nterval **G**ating in **L**itigation).
- Dataset: ALERT-Dataset → VIGIL-Dataset.
- Artifact names: `alert-tracker` → `vigil-tracker`, `alert-sensing.csv` → `vigil-sensing.csv`.
- Figure/algorithm labels updated (`fig:vigil_arch`, `alg:vigil_loop`).

## Title
- **VIGIL: Validity-Gated Retrieval for Product–Litigation Risk Entailment**
  (previously ALERT / Supersession-Aware variant).

## Desk-reject / formatting hygiene
- Ethics section retitled from “Ethics Statement” to “Ethical Considerations” (ARR recommended title; does not count toward page limit).
- Discussion expanded with residual distractor-free advantage and broader RAG implications for evolving corpora.
- Conclusion tightened for clarity of contributions and open problems.
- Main content remains within 8-page long-paper limit; Limitations + Ethical Considerations + References + Appendix unlimited.

## Prioritized open problems (P0 / P1 / P2) reflected in text (2026-10-10)
- **Limitations** reorganized by priority:
  - **P0** (acceptance-critical): (i) human-adjudicated triage n=82, ΔF1 CI includes zero; (ii) backbone-matched baselines missing; (iii) Protocol P1 cross-stack transfer only partially executed.
  - **P1** (methodological completeness): extractor recall, PLRE scale / stronger external baselines, temporal-shift calibration robustness.
  - **P2** (longer-horizon generality): docket vs. dispute counting, defendant skew, non-U.S. jurisdictions, partial/jurisdiction-specific treatments, other superseding corpora.
- **Discussion** now flags the same P0 gaps (cross-stack, backbone-matched controls, modest triage margin) as the highest-priority follow-on measurements.
- **Conclusion** lists the three P0 items first, then P1/P2, and points to the released P1 testbed.

## Prior statistical honesty (2026-10-06)
- Table 3: marginal 95% bootstrap half-widths (~±0.09–0.10 on n=82); paired VIGIL–B5 ΔF1 +0.04, 95% CI [−0.09, +0.18] (includes zero).
- RQ1 text no longer claims p<0.05 vs B5; gap described as modest/directional.
- PLRE full-vs-flat: paired ΔF1 CI [0.03, 0.10], p<0.001.
- Distractor-free subset reported: ΔF1 +0.03, 95% CI [−0.01, +0.07].
- Abstract and Limitations aligned with the above.
- Calibration 150 cases stated as disjoint from the 82 human test cases (already in setup).

## Bundle
- `experiment_outputs/*.csv` — regenerated CSVs (schema = analysis/templates); replace with recovered server logs if available.
- `experiment_outputs/stats_out/review_stats.md` — compute_review_stats.py log.

## Build note
- Full `pdflatex` may need `algorithm`/`algorithmic` packages on the build host.
