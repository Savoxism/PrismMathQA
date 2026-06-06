"""CLI demo for the Math Tutor Agentic RAG core."""

from __future__ import annotations

import sys

from app.chat_core import run_chat_turn
from app.logging_utils import ConversationLogger
from app.memory.store import MemoryStore, StudentProfile
from app.prompts import profile_block
from app.rag.retrieve import RAGRetriever


def prompt_profile(student_id: str, store: MemoryStore) -> StudentProfile:
    existing = store.get_profile(student_id)
    if existing is not None:
        print(f"Loaded profile for {student_id}: {existing}")
        return existing
    print("Create student profile for this demo session.")
    profile = StudentProfile(
        student_id=student_id,
        nickname=input("Nickname: ").strip(),
        grade=input("Grade: ").strip(),
        weak_areas=input("Weak areas: ").strip(),
        strong_areas=input("Strong areas: ").strip(),
        preferred_style=input("Preferred style [step-by-step]: ").strip() or "step-by-step",
    )
    store.upsert_profile(profile)
    return profile


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    store = MemoryStore()
    retriever: RAGRetriever | None = None
    student_id = input("Student ID [s01]: ").strip() or "s01"
    profile = prompt_profile(student_id, store)
    logger = ConversationLogger(student_id)
    logger.log_profile(profile_block(profile))
    print(f"Conversation log: {logger.path}")

    print("Type a math question. Use /quit to exit.")
    turn_index = 0
    while True:
        question = input("\nStudent: ").strip()
        if question in {"/quit", "/exit"}:
            logger.close()
            break
        turn_index += 1
        if turn_index == 1:
            retriever = retriever or RAGRetriever(top_k=3)
        result = run_chat_turn(question, student_id, profile, store, turn_index, retriever)
        logger.log_turn(turn_index, question, result.examples, result.answer, result.tool_calls)
        print(f"\nTutor: {result.answer}")


if __name__ == "__main__":
    main()
