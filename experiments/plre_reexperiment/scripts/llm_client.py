"""Thin OpenAI / Azure OpenAI client."""
from __future__ import annotations

import json
import os
import re
import time
from typing import Any

from config import MAX_RETRIES, MODEL, SLEEP_ON_ERROR

def _client():
    from openai import OpenAI, AzureOpenAI

    if os.environ.get("AZURE_OPENAI_API_KEY") and os.environ.get("AZURE_OPENAI_ENDPOINT"):
        return AzureOpenAI(
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        )
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError(
            "Set OPENAI_API_KEY or AZURE_OPENAI_API_KEY + AZURE_OPENAI_ENDPOINT"
        )
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def _model_name() -> str:
    if os.environ.get("AZURE_OPENAI_API_KEY"):
        return os.environ.get("AZURE_OPENAI_DEPLOYMENT", MODEL)
    return MODEL


def chat_json(
    system: str,
    user: str,
    temperature: float,
    seed: int | None = None,
) -> dict[str, Any]:
    """Call chat completion and parse a JSON object from the response."""
    client = _client()
    kwargs: dict[str, Any] = {
        "model": _model_name(),
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "response_format": {"type": "json_object"},
    }
    # seed is supported on OpenAI API for many models; ignore if rejected
    if seed is not None:
        kwargs["seed"] = seed

    last_err: Exception | None = None
    for attempt in range(MAX_RETRIES):
        try:
            resp = client.chat.completions.create(**kwargs)
            text = resp.choices[0].message.content or "{}"
            usage = {
                "tokens_in": getattr(resp.usage, "prompt_tokens", None),
                "tokens_out": getattr(resp.usage, "completion_tokens", None),
            }
            data = json.loads(text)
            data["_usage"] = usage
            return data
        except Exception as e:  # noqa: BLE001
            last_err = e
            # retry without seed if unsupported
            if "seed" in kwargs and "seed" in str(e).lower():
                kwargs.pop("seed", None)
            time.sleep(SLEEP_ON_ERROR * (attempt + 1))
    raise RuntimeError(f"LLM call failed after {MAX_RETRIES} retries: {last_err}")


def extract_label(obj: dict[str, Any]) -> str:
    lab = str(obj.get("label", "")).strip().upper()
    if lab in {"YES", "NO"}:
        return lab
    # fallback
    m = re.search(r"\b(YES|NO)\b", lab)
    return m.group(1) if m else "NO"
