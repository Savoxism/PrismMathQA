"""Tool request parsing and dispatch."""

from __future__ import annotations

import json
import re
from typing import Any

from app.tools.verify_answer import verify_answer

TOOL_BLOCK_RE = re.compile(r"```tool\s*(\{.*?\})\s*```", re.DOTALL)


def extract_tool_request(text: str) -> dict[str, Any] | None:
    match = TOOL_BLOCK_RE.search(text)
    if match is None:
        return None
    request = json.loads(match.group(1))
    if request.get("action") != "verify_answer":
        raise ValueError(f"Unsupported tool action: {request.get('action')}")
    return request


def run_tool(request: dict[str, Any]) -> dict[str, Any]:
    action = request["action"]
    args = request.get("args", {})
    if action == "verify_answer":
        return verify_answer(**args)
    raise ValueError(f"Unsupported tool action: {action}")
