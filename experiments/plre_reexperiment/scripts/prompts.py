"""Prompt templates for PLRE re-experiments.

Every prompt asks for ``supporting_doc_ids`` so that stale citations are
measured from the cited documents' validity status (compute_metrics.py),
not from the model's own report.

Only gated systems see validity labels. Ungated systems (vigil_no_gate,
date_filter, posthoc_filter's first pass, b5) see neither labels nor an
instruction about closed authority; otherwise the "no gate" condition would
still be gated through the prompt.
"""
from __future__ import annotations

from typing import Any

_JSON_SPEC = (
    'Respond with a single JSON object only:\n'
    '{"label": "YES"|"NO", "confidence": 0.0-1.0, "supporting_doc_ids": ["..."]}\n'
    "supporting_doc_ids lists every passage doc_id your decision relies on."
)

SYSTEM_PLRE_GATED = f"""You are a legal-risk entailment classifier for AI products.

Decide whether a product_attribute entails exposure to a risk_theory under
authorities that are legally operative at query_date.

Each passage carries a validity label from a treatment graph:
open (fully operative), narrowed (materially narrowed; weaker support),
cautionary (distinguished or weakly questioned; weaker support).
Closed (overruled or superseded) authorities have already been removed.
If evidence is insufficient, answer NO.

{_JSON_SPEC}
"""

SYSTEM_PLRE_GATE_ONLY = f"""You are a legal-risk entailment classifier for AI products.

Decide whether a product_attribute entails exposure to a risk_theory under
authorities that are legally operative at query_date.
Overruled or superseded authorities have already been removed from the passages.
If evidence is insufficient, answer NO.

{_JSON_SPEC}
"""

SYSTEM_PLRE_UNGATED = f"""You are a legal-risk entailment classifier for AI products.

Decide whether a product_attribute entails exposure to a risk_theory at query_date,
using the retrieved passages.
If evidence is insufficient, answer NO.

{_JSON_SPEC}
"""

SYSTEM_PLRE_DATE_ONLY = f"""You are a legal-risk entailment classifier for AI products.

Passages were filtered only by document date (decision_date <= query_date).
There is no overruling or supersession metadata beyond what appears in the text.
Decide whether product_attribute entails exposure to risk_theory at query_date.
If evidence is insufficient, answer NO.

{_JSON_SPEC}
"""

SYSTEM_B5 = """You are a self-refining legal-risk analyst (Reflexion-style).

You will run up to {max_iters} iterations. Each iteration:
1) Propose YES/NO on whether product_attribute entails risk_theory at query_date.
2) Critique gaps (missing evidence, possibly outdated authority, weak alignment).
3) Revise.

Retrieved passages are provided without validity metadata.

After the final iteration, respond with JSON only:
{{"label": "YES"|"NO", "confidence": 0.0-1.0, "iterations_used": <int>,
 "supporting_doc_ids": ["..."], "rationale": "<one sentence>"}}
supporting_doc_ids lists every passage doc_id your decision relies on.
"""


def format_passages(passages: list[dict[str, Any]], include_validity: bool) -> str:
    lines = []
    for i, p in enumerate(passages, 1):
        header = f"[{i}] doc_id={p.get('doc_id')} date={p.get('decision_date')}"
        if include_validity:
            header += f" validity={p.get('validity_status', 'unknown')}"
        lines.append(header)
        lines.append(str(p.get("text", ""))[:2000])
        lines.append("")
    return "\n".join(lines).strip()


def user_plre(row: dict[str, Any], passages: list[dict[str, Any]], include_validity: bool) -> str:
    return (
        f"product_attribute: {row['product_attribute']}\n"
        f"risk_theory: {row['risk_theory']}\n"
        f"query_date: {row['query_date']}\n\n"
        f"passages:\n{format_passages(passages, include_validity=include_validity)}"
    )
