"""Local MetaMathQA sample loader."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.paths import METAMATH_SAMPLE_PATH


def load_examples(path: Path = METAMATH_SAMPLE_PATH) -> dict[str, dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing local corpus: {path}. Put the downloaded MetaMathQA sample JSONL there first."
        )
    examples: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            item = json.loads(line)
            missing = {"id", "question", "answer"} - set(item)
            if missing:
                raise ValueError(f"{path}:{line_number} missing required fields: {sorted(missing)}")
            examples[item["id"]] = item
    return examples
