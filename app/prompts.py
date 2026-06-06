"""Prompt templates for the Math Tutor demo."""

from __future__ import annotations

from app.memory.store import StudentProfile
from app.rag.retrieve import RetrievedExample

SYSTEM_PROMPT = """You are a math tutor for middle and high school students.
Teach step by step, keep the conversation connected across turns, and adapt to the student's profile.
Use retrieved MetaMathQA examples as in-context examples, but answer the student's exact current question.
Reply in the same language as the student unless the student explicitly asks for another language.

You have access to one calculator/verifier tool. Before answering, decide whether the current question is:
- DIRECT: you can answer accurately without external computation;
- TOOL: exact computation or symbolic verification would materially improve correctness.

If you choose TOOL, output only a JSON request inside a fenced block exactly like this, then stop:
```tool
{"action": "verify_answer", "args": {"problem": "...", "expected_answer": "..."}}
```

Tool argument contract:
- `problem` must contain only the mathematical expression or equation to parse.
- Do not put natural language in `problem`: no "solve for", "verify", "compute", explanations, units, or prose.
- Use explicit multiplication: write `987654321*x`, not `987654321x`.
- Put a proposed answer in `expected_answer` only when the student gave one or when you need to verify a candidate; otherwise use an empty string.
- Valid: `{"problem": "987654321*x - 123456789 = 555555555", "expected_answer": ""}`
- Invalid: `{"problem": "Solve for x in 987654321*x - 123456789 = 555555555", "expected_answer": ""}`

Prefer using `verify_answer` for exact verification, large arithmetic, nontrivial fractions, equation solving, symbolic simplification, derivatives, integrals, or any intermediate computation where a small arithmetic mistake would change the final answer.
Do not use the tool for simple mental arithmetic or purely conceptual explanations.

The only available tool is `verify_answer`. Do not invent tool names.
If no tool is needed, answer normally.
"""


def profile_block(profile: StudentProfile | None) -> str:
    if profile is None:
        return "No saved student profile yet."
    return (
        f"Student profile:\n"
        f"- student_id: {profile.student_id}\n"
        f"- nickname: {profile.nickname or 'unknown'}\n"
        f"- grade: {profile.grade or 'unknown'}\n"
        f"- weak areas: {profile.weak_areas or 'unknown'}\n"
        f"- strong areas: {profile.strong_areas or 'unknown'}\n"
        f"- preferred style: {profile.preferred_style or 'step-by-step'}"
    )


def history_block(history: list[dict[str, str]], limit: int = 6) -> str:
    if not history:
        return "No prior conversation turns."
    recent = history[-limit:]
    lines = ["Recent conversation:"]
    for item in recent:
        lines.append(f"User: {item['query']}")
        lines.append(f"Tutor: {item['answer']}")
    return "\n".join(lines)


def examples_block(examples: list[RetrievedExample]) -> str:
    if not examples:
        return "No retrieved examples available."
    blocks = ["Retrieved MetaMathQA examples:"]
    for index, example in enumerate(examples, start=1):
        blocks.append(
            f"[Example {index} | id={example.example_id} | score={example.score:.4f}]\n"
            f"Question: {example.question}\n"
            f"Solution: {example.answer}"
        )
    return "\n\n".join(blocks)


def build_user_prompt(
    question: str,
    profile: StudentProfile | None,
    history: list[dict[str, str]],
    examples: list[RetrievedExample],
) -> str:
    return "\n\n".join(
        [
            profile_block(profile),
            history_block(history),
            examples_block(examples),
            f"Current student question:\n{question}",
            "Answer as a helpful tutor. Decide DIRECT or TOOL internally. If TOOL is needed, emit only the fenced `tool` JSON block in the required syntax.",
        ]
    )


def build_tool_followup_prompt(question: str, draft_answer: str, tool_result: dict) -> str:
    return (
        "A calculator/verifier tool was used. Use the verified tool result below to produce "
        "the final student-facing answer in the same language as the student's question.\n\n"
        f"Student question:\n{question}\n\n"
        f"Draft answer/tool request:\n{draft_answer}\n\n"
        f"Tool result:\n{tool_result}"
    )
