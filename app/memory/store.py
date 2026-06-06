"""SQLite-backed student memory."""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterator

from app.paths import SQLITE_PATH


@dataclass(frozen=True)
class StudentProfile:
    student_id: str
    nickname: str = ""
    grade: str = ""
    weak_areas: str = ""
    strong_areas: str = ""
    preferred_style: str = "step-by-step"


class MemoryStore:
    def __init__(self, db_path: Path = SQLITE_PATH) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self.connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS student_profiles (
                    student_id TEXT PRIMARY KEY,
                    nickname TEXT,
                    grade TEXT,
                    weak_areas TEXT,
                    strong_areas TEXT,
                    preferred_style TEXT,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    query TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    retrieved_example_ids TEXT NOT NULL,
                    tool_calls TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS tool_calls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    interaction_id INTEGER,
                    tool_name TEXT NOT NULL,
                    args_json TEXT NOT NULL,
                    result_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS retrieved_examples (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    interaction_id INTEGER,
                    example_id TEXT NOT NULL,
                    score REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS memory_summaries (
                    student_id TEXT PRIMARY KEY,
                    summary TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                """
            )

    def upsert_profile(self, profile: StudentProfile) -> None:
        now = datetime.now(UTC).isoformat()
        with self.connect() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO students(student_id, created_at) VALUES (?, ?)",
                (profile.student_id, now),
            )
            conn.execute(
                """
                INSERT INTO student_profiles(
                    student_id, nickname, grade, weak_areas, strong_areas, preferred_style, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(student_id) DO UPDATE SET
                    nickname=excluded.nickname,
                    grade=excluded.grade,
                    weak_areas=excluded.weak_areas,
                    strong_areas=excluded.strong_areas,
                    preferred_style=excluded.preferred_style,
                    updated_at=excluded.updated_at
                """,
                (
                    profile.student_id,
                    profile.nickname,
                    profile.grade,
                    profile.weak_areas,
                    profile.strong_areas,
                    profile.preferred_style,
                    now,
                ),
            )

    def get_profile(self, student_id: str) -> StudentProfile | None:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM student_profiles WHERE student_id = ?", (student_id,)
            ).fetchone()
        if row is None:
            return None
        return StudentProfile(
            student_id=row["student_id"],
            nickname=row["nickname"] or "",
            grade=row["grade"] or "",
            weak_areas=row["weak_areas"] or "",
            strong_areas=row["strong_areas"] or "",
            preferred_style=row["preferred_style"] or "step-by-step",
        )

    def recent_interactions(self, student_id: str, limit: int = 6) -> list[dict[str, str]]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT query, answer FROM interactions
                WHERE student_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (student_id, limit),
            ).fetchall()
        return [{"query": row["query"], "answer": row["answer"]} for row in reversed(rows)]

    def save_interaction(
        self,
        student_id: str,
        query: str,
        answer: str,
        retrieved_examples: list[Any],
        tool_calls: list[dict[str, Any]],
    ) -> int:
        now = datetime.now(UTC).isoformat()
        retrieved_ids = [item.example_id for item in retrieved_examples]
        with self.connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO interactions(
                    student_id, query, answer, retrieved_example_ids, tool_calls, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    student_id,
                    query,
                    answer,
                    json.dumps(retrieved_ids),
                    json.dumps(tool_calls, ensure_ascii=False),
                    now,
                ),
            )
            interaction_id = int(cursor.lastrowid)
            for item in retrieved_examples:
                conn.execute(
                    "INSERT INTO retrieved_examples(interaction_id, example_id, score) VALUES (?, ?, ?)",
                    (interaction_id, item.example_id, item.score),
                )
            for call in tool_calls:
                conn.execute(
                    """
                    INSERT INTO tool_calls(interaction_id, tool_name, args_json, result_json, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        interaction_id,
                        call["action"],
                        json.dumps(call.get("args", {}), ensure_ascii=False),
                        json.dumps(call.get("result", {}), ensure_ascii=False),
                        now,
                    ),
                )
        return interaction_id

    def update_summary(self, student_id: str, summary: str) -> None:
        now = datetime.now(UTC).isoformat()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO memory_summaries(student_id, summary, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(student_id) DO UPDATE SET
                    summary=excluded.summary,
                    updated_at=excluded.updated_at
                """,
                (student_id, summary, now),
            )

    def checkpoint_saver(self):
        from langgraph.checkpoint.sqlite import SqliteSaver

        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        return SqliteSaver(conn)


def profile_from_answers(student_id: str, answers: dict[str, str]) -> StudentProfile:
    return StudentProfile(student_id=student_id, **{k: v.strip() for k, v in answers.items()})
