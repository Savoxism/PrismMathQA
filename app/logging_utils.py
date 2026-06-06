"""Per-session text logging for CLI demos."""

from __future__ import annotations

from datetime import datetime

from app.paths import LOG_DIR
from app.rag.retrieve import RetrievedExample


class ConversationLogger:
    def __init__(self, student_id: str) -> None:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        self.started_at = datetime.now().astimezone()
        safe_student_id = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in student_id)
        timestamp = self.started_at.strftime("%Y%m%d_%H%M%S")
        self.path = LOG_DIR / f"{safe_student_id}_{timestamp}.log"
        self.write("SESSION_START", f"student_id={student_id}\nstarted_at={self.started_at.isoformat()}")

    def write(self, section: str, text: str) -> None:
        now = datetime.now().astimezone().isoformat()
        with self.path.open("a", encoding="utf-8") as file:
            file.write(f"\n[{now}] {section}\n")
            file.write(text.rstrip() + "\n")

    def log_profile(self, profile_text: str) -> None:
        self.write("PROFILE", profile_text)

    def log_turn(
        self,
        turn_index: int,
        question: str,
        examples: list[RetrievedExample],
        answer: str,
        tool_calls: list[dict],
    ) -> None:
        example_blocks = []
        for index, example in enumerate(examples, start=1):
            example_blocks.append(
                f"ICL Example {index}\n"
                f"id: {example.example_id}\n"
                f"score: {example.score:.4f}\n"
                f"question: {example.question}\n"
                f"answer: {example.answer}"
            )
        body = "\n\n".join(
            [
                f"turn: {turn_index}",
                f"USER:\n{question}",
                "RETRIEVED_ICL_EXAMPLES:\n" + ("\n\n".join(example_blocks) if example_blocks else "none"),
                f"TOOL_CALLS:\n{tool_calls if tool_calls else 'none'}",
                f"ASSISTANT:\n{answer}",
            ]
        )
        self.write("TURN", body)

    def close(self) -> None:
        self.write("SESSION_END", "Conversation closed.")
