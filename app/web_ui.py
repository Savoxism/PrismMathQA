"""FastAPI web UI for PrismMath Tutor."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.chat_core import run_chat_turn
from app.logging_utils import ConversationLogger
from app.memory.store import MemoryStore, StudentProfile
from app.prompts import profile_block
from app.rag.retrieve import RAGRetriever

app = FastAPI(title="PrismMath Tutor")
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))

store = MemoryStore()
retriever: RAGRetriever | None = None
sessions: dict[str, dict[str, Any]] = {}


def _session_id(student_id: str) -> str:
    return student_id.strip() or "s01"


def _get_retriever() -> RAGRetriever:
    global retriever
    if retriever is None:
        retriever = RAGRetriever(top_k=3)
    return retriever


def _render(request: Request, **context: Any) -> HTMLResponse:
    defaults = {
        "student_id": "s01",
        "nickname": "",
        "grade": "",
        "weak_areas": "",
        "strong_areas": "",
        "preferred_style": "step-by-step",
        "turn_index": 0,
        "answer": "",
        "examples": [],
        "tool_calls": [],
        "log_path": "",
        "error": "",
    }
    defaults.update(context)
    return templates.TemplateResponse(request, "chat.html", defaults)


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return _render(request)


@app.post("/chat", response_class=HTMLResponse)
def chat(
    request: Request,
    student_id: str = Form("s01"),
    nickname: str = Form(""),
    grade: str = Form(""),
    weak_areas: str = Form(""),
    strong_areas: str = Form(""),
    preferred_style: str = Form("step-by-step"),
    question: str = Form(""),
    turn_index: int = Form(0),
) -> HTMLResponse:
    if not question.strip():
        return _render(
            request,
            student_id=student_id,
            nickname=nickname,
            grade=grade,
            weak_areas=weak_areas,
            strong_areas=strong_areas,
            preferred_style=preferred_style,
            turn_index=turn_index,
            error="Please enter a math question.",
        )

    sid = _session_id(student_id)
    profile = StudentProfile(
        student_id=sid,
        nickname=nickname.strip(),
        grade=grade.strip(),
        weak_areas=weak_areas.strip(),
        strong_areas=strong_areas.strip(),
        preferred_style=preferred_style.strip() or "step-by-step",
    )
    store.upsert_profile(profile)

    session = sessions.get(sid)
    if session is None:
        logger = ConversationLogger(sid)
        logger.log_profile(profile_block(profile))
        session = {"turn_index": 0, "logger": logger}
        sessions[sid] = session

    next_turn = int(session["turn_index"]) + 1
    turn_retriever = _get_retriever() if next_turn == 1 else None
    try:
        result = run_chat_turn(question.strip(), sid, profile, store, next_turn, turn_retriever)
    except Exception as exc:
        return _render(
            request,
            **asdict(profile),
            turn_index=session["turn_index"],
            error=str(exc),
            log_path=str(session["logger"].path),
        )

    session["turn_index"] = next_turn
    session["logger"].log_turn(next_turn, question.strip(), result.examples, result.answer, result.tool_calls)

    return _render(
        request,
        **asdict(profile),
        turn_index=next_turn,
        answer=result.answer,
        examples=result.examples,
        tool_calls=result.tool_calls,
        log_path=str(session["logger"].path),
    )
