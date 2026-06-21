"""Shared chat turn logic for CLI and web UI."""

from __future__ import annotations

from dataclasses import dataclass

from app.memory.store import MemoryStore, StudentProfile
from app.prompts import (
    SYSTEM_PROMPT,
    build_protocol_retry_prompt,
    build_tool_followup_prompt,
    build_user_prompt,
    looks_like_incomplete_tool_intent,
)
from app.rag.retrieve import RAGRetriever, RetrievedExample
from app.tools.runtime import extract_tool_request, run_tool
from utils.llm_client import chat_completion

DEFAULT_MAX_TOKENS = 4096


@dataclass
class ChatTurnResult:
    answer: str
    examples: list[RetrievedExample]
    tool_calls: list[dict]


def run_chat_turn(
    question: str,
    student_id: str,
    profile: StudentProfile,
    store: MemoryStore,
    turn_index: int,
    retriever: RAGRetriever | None,
) -> ChatTurnResult:
    history = store.recent_interactions(student_id)
    if turn_index == 1:
        if retriever is None:
            raise ValueError("retriever is required for the first turn")
        examples = retriever.retrieve(question)
    else:
        examples = []

    prompt = build_user_prompt(question, profile, history, examples)
    draft = chat_completion(
        [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
        max_tokens=DEFAULT_MAX_TOKENS,
    )

    tool_calls: list[dict] = []
    answer = str(draft)
    try:
        request = extract_tool_request(answer)
    except ValueError as exc:
        request = None
        tool_calls.append({"action": "unsupported_tool", "args": {}, "result": {"error": str(exc)}})

    if request is None and looks_like_incomplete_tool_intent(answer):
        retry_prompt = build_protocol_retry_prompt(prompt, answer)
        answer = str(
            chat_completion(
                [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": retry_prompt}],
                max_tokens=DEFAULT_MAX_TOKENS,
            )
        )
        try:
            request = extract_tool_request(answer)
        except ValueError as exc:
            tool_calls.append({"action": "unsupported_tool", "args": {}, "result": {"error": str(exc)}})
            request = None

    if request is not None:
        result = run_tool(request)
        request["result"] = result
        tool_calls.append(request)
        followup = build_tool_followup_prompt(question, answer, result)
        answer = str(
            chat_completion(
                [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": followup}],
                max_tokens=DEFAULT_MAX_TOKENS,
            )
        )

    store.save_interaction(student_id, question, answer, examples, tool_calls)
    return ChatTurnResult(answer=answer, examples=examples, tool_calls=tool_calls)
