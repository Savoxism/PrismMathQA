# Agent Guide

## Project Overview

This repository contains PrismMath Tutor, a Python demo for an agentic math tutor. It has:

- A CLI entry point in `main.py` and `app/chat_cli.py`.
- A FastAPI web demo in `app/web_ui.py` with the Jinja template at `app/templates/chat.html`.
- Shared chat orchestration in `app/chat_core.py`.
- Student profile and conversation memory backed by SQLite in `app/memory/store.py`.
- First-turn RAG over a local MetaMathQA JSONL sample using ChromaDB and a local Qwen embedding model in `app/rag/`.
- A SymPy verifier tool in `app/tools/verify_answer.py`, dispatched through `app/tools/runtime.py`.
- LLM client and environment loading in `utils/llm_client.py` and `utils/config.py`.
- A LaTeX technical report under `nlp_capstone_project/`.

## Hard Rules

- Never install packages into the global pip environment.
- Always use the project virtual environment for Python commands.
- Prefer `.\.venv\Scripts\python.exe` explicitly in commands so the interpreter is unambiguous.
- Do not commit or expose `.env`, API keys, local model weights, SQLite demo data, Chroma indexes, or logs.
- Treat `data/`, `models/`, and `logs/` as local/generated artifacts unless a task says otherwise.

## Setup And Run Commands

Create or refresh the virtual environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.\.venv\Scripts\python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cu128
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Expected local inputs:

```text
data/processed/metamathqa_30k.jsonl
models/qwen3-embedding-4b/
.env
```

Required `.env` keys:

```text
LLM_API_KEY=...
LLM_BASE_URL=...
```

Build or rebuild the RAG index:

```powershell
.\.venv\Scripts\python.exe -m app.rag.ingest --reset --batch-size 2
```

If GPU memory is limited, use `--batch-size 1`.

Run the web demo:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.web_ui:app --host 127.0.0.1 --port 8080
```

Run the CLI demo:

```powershell
.\.venv\Scripts\python.exe main.py
```

Run tests when present:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Build the paper:

```powershell
cd nlp_capstone_project
latexmk -pdf main.tex
```

## Architecture Notes

- `app/chat_core.py` owns one chat turn for both CLI and web UI. Put shared turn behavior there, not separately in CLI or FastAPI handlers.
- RAG retrieval is currently intended for the first turn only. Later turns rely on SQLite-backed recent history.
- `MemoryStore` creates tables lazily in `data/demo.sqlite3` and stores profiles, interactions, retrieved example IDs, and tool calls.
- `QwenEmbedder` loads local weights from `models/qwen3-embedding-4b/`; do not replace this with a network download unless explicitly requested.
- `utils/config.py` validates `LLM_API_KEY` and `LLM_BASE_URL` at import time, so importing app modules can fail without `.env`.
- The only model tool exposed in prompts is `verify_answer`. Keep prompt/tool contracts synchronized with `app/tools/runtime.py`.

## Development Guidelines

- Make small, surgical changes and match the existing straightforward Python style.
- Add tests for changed pure logic when practical, especially tool parsing, SymPy verification, prompt formatting, dataset loading, and memory persistence.
- Avoid importing heavy ML dependencies at module import time; the current RAG code imports Chroma, Torch, and Sentence Transformers inside runtime paths.
- Preserve the separation between generated artifacts and source code. Do not check in Chroma indexes, logs, local SQLite data, or model files.
- Keep web UI changes contained to `app/templates/chat.html` unless Python behavior changes are required.
- When changing retrieval, verify both ingestion and `RAGRetriever.retrieve`.
- When changing memory schema or logging, verify deletion/reset guidance in `README.md` still matches the implementation.

## Known Checks Before Running

- `app/rag/ingest.py` uses `METAMATH_SAMPLE_PATH`; verify it imports that name from `app.paths` before relying on ingestion.
- The project currently lists `pytest` but has no test files. New behavior should include focused tests where feasible.
- Full CLI/web runs require a valid `.env`, local MetaMathQA sample, local Qwen embedding weights, and a built Chroma index.
