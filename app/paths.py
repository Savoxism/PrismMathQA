"""Shared local paths for generated demo artifacts."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
CHROMA_DIR = DATA_DIR / "chroma"
MODEL_DIR = PROJECT_ROOT / "models" / "qwen3-embedding-4b"
LOG_DIR = PROJECT_ROOT / "logs"
SQLITE_PATH = DATA_DIR / "demo.sqlite3"
METAMATH_SAMPLE_PATH = PROCESSED_DIR / "metamathqa_30k.jsonl"

RAG_COLLECTION = "metamathqa_questions_qwen3_4b"
