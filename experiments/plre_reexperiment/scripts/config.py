"""Shared configuration. Override via environment variables."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.environ.get("PLRE_DATA_DIR", ROOT / "data"))
OUT_DIR = Path(os.environ.get("PLRE_OUT_DIR", ROOT / "outputs"))
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Model
MODEL = os.environ.get("PLRE_MODEL", "gpt-4o-2024-08-06")
# Edge / deterministic classification
TEMP_EDGE = float(os.environ.get("PLRE_TEMP_EDGE", "0"))
# Controller-style generation
TEMP_CTRL = float(os.environ.get("PLRE_TEMP_CTRL", "0.2"))

SEEDS = [int(x) for x in os.environ.get("PLRE_SEEDS", "0,1,2,3,4").split(",") if x.strip() != ""]

# B5 budget
B5_MAX_ITERS = int(os.environ.get("PLRE_B5_MAX_ITERS", "3"))
# Optional token budget for token-matched run (None = iteration-only)
B5_MAX_COMPLETION_TOKENS = os.environ.get("PLRE_B5_MAX_TOKENS")
B5_MAX_COMPLETION_TOKENS = int(B5_MAX_COMPLETION_TOKENS) if B5_MAX_COMPLETION_TOKENS else None

MAX_RETRIES = int(os.environ.get("PLRE_MAX_RETRIES", "5"))
SLEEP_ON_ERROR = float(os.environ.get("PLRE_SLEEP_ON_ERROR", "2.0"))
