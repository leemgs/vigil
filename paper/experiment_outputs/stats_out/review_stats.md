# Review statistics

Bootstrap resamples: 2000; seed: 42; CIs are 95% percentile intervals.

## RQ1: severity labels (W-A, W3, W-C)

- Test cases: 250 (human: 82, retained: 168)
- Human-adjudicated cases by split: {'test': 82, 'train': 25, 'validation': 15}
  - NOTE: some human-adjudicated cases are in train/validation. If Table 3 uses all human cases, those used for few-shot examples or threshold tuning overlap the evaluation (possible leakage).

**human-adjudicated test (n=82)**

| System | F1 | 95% CI | P | R | Δ vs VIGIL | p (paired bootstrap) |
|---|---|---|---|---|---|---|
| VIGIL | 0.790 | [0.687, 0.875] | 0.789 | 0.798 | — | — |
| VIGIL-noGoalChecker | 0.758 | [0.654, 0.850] | 0.753 | 0.773 | +0.032 | 0.6800 |
| VIGIL-noPlanner | 0.782 | [0.685, 0.864] | 0.777 | 0.789 | +0.008 | 0.9100 |
| VIGIL-noQueryExpand | 0.794 | [0.695, 0.874] | 0.800 | 0.809 | -0.004 | 0.9650 |
| B1 | 0.555 | [0.440, 0.663] | 0.554 | 0.556 | +0.235 | 0.0010 |
| B2 | 0.698 | [0.586, 0.786] | 0.700 | 0.708 | +0.092 | 0.1560 |
| B3 | 0.715 | [0.611, 0.812] | 0.717 | 0.715 | +0.074 | 0.2940 |
| B4 | 0.741 | [0.632, 0.837] | 0.742 | 0.741 | +0.049 | 0.4810 |
| B5 | 0.746 | [0.636, 0.840] | 0.746 | 0.748 | +0.044 | 0.5550 |

**full test (n=250)**

| System | F1 | 95% CI | P | R | Δ vs VIGIL | p (paired bootstrap) |
|---|---|---|---|---|---|---|
| VIGIL | 0.802 | [0.749, 0.852] | 0.799 | 0.806 | — | — |
| VIGIL-noGoalChecker | 0.762 | [0.705, 0.814] | 0.756 | 0.775 | +0.041 | 0.2860 |
| VIGIL-noPlanner | 0.783 | [0.726, 0.832] | 0.776 | 0.794 | +0.020 | 0.5760 |
| VIGIL-noQueryExpand | 0.788 | [0.734, 0.839] | 0.786 | 0.794 | +0.014 | 0.6890 |
| B1 | 0.602 | [0.539, 0.661] | 0.603 | 0.612 | +0.200 | <0.0005 |
| B2 | 0.712 | [0.652, 0.766] | 0.708 | 0.721 | +0.090 | 0.0180 |
| B3 | 0.735 | [0.676, 0.787] | 0.730 | 0.745 | +0.068 | 0.0780 |
| B4 | 0.751 | [0.692, 0.803] | 0.746 | 0.758 | +0.052 | 0.1930 |
| B5 | 0.762 | [0.704, 0.812] | 0.755 | 0.777 | +0.041 | 0.2600 |

## PLRE (W-A/W1, W2, W-F)

- Pairs (all splits): 1856; test pairs: 1484
- Test positive rate: 0.290 (430/1484)
- Test stale-authority distractor share: 0.196 (291/1484)
- Test pairs per archetype: {'A1': 371, 'A2': 371, 'A3': 371, 'A4': 371}

**all test pairs (n=1484)**

| System | F1 | 95% CI | P | R | Stale-cite % | Δ vs VIGIL | p |
|---|---|---|---|---|---|---|---|
| VIGIL | 0.785 | [0.754, 0.813] | 0.730 | 0.849 | 1.5 | — | — |
| VIGIL-flat | 0.719 | [0.685, 0.751] | 0.638 | 0.823 | 4.6 | +0.066 | 0.0010 |
| COLIEE-retrieval | 0.694 | [0.661, 0.726] | 0.613 | 0.800 | 4.0 | +0.091 | <0.0005 |
| LegalBERT-NLI | 0.669 | [0.634, 0.703] | 0.591 | 0.770 | 4.0 | +0.116 | <0.0005 |
| RAG-only | 0.728 | [0.695, 0.760] | 0.662 | 0.809 | 3.5 | +0.057 | 0.0080 |
| cosine | 0.662 | [0.628, 0.696] | 0.573 | 0.784 | 4.5 | +0.123 | <0.0005 |

**without stale-authority distractors (W2) (n=1193)**

| System | F1 | 95% CI | P | R | Stale-cite % | Δ vs VIGIL | p |
|---|---|---|---|---|---|---|---|
| VIGIL | 0.805 | [0.776, 0.830] | 0.765 | 0.849 | 0.0 | — | — |
| VIGIL-flat | 0.773 | [0.742, 0.801] | 0.728 | 0.823 | 0.0 | +0.032 | 0.0820 |
| COLIEE-retrieval | 0.739 | [0.704, 0.770] | 0.687 | 0.800 | 0.0 | +0.066 | 0.0010 |
| LegalBERT-NLI | 0.711 | [0.675, 0.742] | 0.661 | 0.770 | 0.0 | +0.094 | <0.0005 |
| RAG-only | 0.770 | [0.739, 0.800] | 0.734 | 0.809 | 0.0 | +0.035 | 0.0690 |
| cosine | 0.709 | [0.675, 0.741] | 0.647 | 0.784 | 0.0 | +0.096 | <0.0005 |

**Per-archetype F1 (W-F)**

| Archetype | n | VIGIL | VIGIL-flat |
|---|---|---|---|
| A1 | 371 | 0.800 | 0.705 |
| A2 | 371 | 0.792 | 0.739 |
| A3 | 371 | 0.754 | 0.661 |
| A4 | 371 | 0.794 | 0.762 |

## Severity-label agreement (W-E)

- Items: 82; annotators: 3; items rated by all: 82
- Cohen's κ ann1–ann2: 0.814 (n=82)
- Cohen's κ ann1–ann3: 0.758 (n=82)
- Cohen's κ ann2–ann3: 0.774 (n=82)
- Fleiss' κ (items rated by all): 0.782
- Krippendorff's α (nominal): 0.783

## PLRE-label agreement (W1)

- Items: 300; annotators: 3; items rated by all: 300
- Cohen's κ ann1–ann2: 0.578 (n=300)
- Cohen's κ ann1–ann3: 0.613 (n=300)
- Cohen's κ ann2–ann3: 0.490 (n=300)
- Fleiss' κ (items rated by all): 0.559
- Krippendorff's α (nominal): 0.560

## RQ2: report ratings (W5)

- Krippendorff's α (interval), Accuracy: 0.827
- Krippendorff's α (interval), Actionability: 0.785
- Krippendorff's α (interval), Clarity: 0.827
- Krippendorff's α (interval), Completeness: 0.843
- Krippendorff's α (interval), EvidenceSufficiency: 0.810
- Krippendorff's α (interval), all dimensions pooled: 0.821 (2 raters)

| Dimension | Baseline | p (raw) | p (Holm, all comparisons) |
|---|---|---|---|
| Accuracy | B2 | 0.0030 | 0.0534 |
| Accuracy | B3 | 0.0023 | 0.0434 |
| Accuracy | B4 | 0.0103 | 0.0929 |
| Accuracy | B5 | 0.1401 | 0.2802 |
| Actionability | B2 | 0.0047 | 0.0668 |
| Actionability | B3 | 0.0050 | 0.0668 |
| Actionability | B4 | 0.0158 | 0.0929 |
| Actionability | B5 | 0.0083 | 0.0830 |
| Clarity | B2 | 0.0036 | 0.0609 |
| Clarity | B3 | 0.0749 | 0.2247 |
| Clarity | B4 | 0.0131 | 0.0929 |
| Clarity | B5 | 0.1408 | 0.2802 |
| Completeness | B2 | 0.0067 | 0.0732 |
| Completeness | B3 | 0.0005 | 0.0103 |
| Completeness | B4 | 0.0105 | 0.0929 |
| Completeness | B5 | 0.0103 | 0.0929 |
| EvidenceSufficiency | B2 | 0.0045 | 0.0668 |
| EvidenceSufficiency | B3 | 0.0167 | 0.0929 |
| EvidenceSufficiency | B4 | 0.0036 | 0.0609 |
| EvidenceSufficiency | B5 | 0.0050 | 0.0668 |

- Comparisons significant after Holm correction: 2/20

## LLM calls and tokens per case (W-B)

| System | cases | mean calls | median calls | mean tokens | median tokens |
|---|---|---|---|---|---|
| VIGIL | 82 | 10.0 | 10.5 | 19,184 | 19,182 |
| B2 | 82 | 1.0 | 1.0 | 4,075 | 4,067 |
| B4 | 82 | 6.2 | 7.0 | 12,637 | 12,634 |
| B5 | 82 | 3.0 | 3.0 | 5,559 | 5,490 |

## Conformal calibration set (W4)

- Calibration cases: 150
