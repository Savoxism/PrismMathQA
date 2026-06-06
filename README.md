# PrismMath Tutor Demo

## Run Demo

Use the project virtual environment only. Do not install packages into global pip.

```powershell
cd D:\Github\NLP-Capstone-Project-20252
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.\.venv\Scripts\python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cu128
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Create `.env`:

```text
LLM_API_KEY=your_key_here
LLM_BASE_URL=https://your-openai-compatible-endpoint/v1
```

Expected local files:

```text
data/processed/metamathqa_30k.jsonl
models/qwen3-embedding-4b/
```

Build or rebuild the RAG index:

```powershell
.\.venv\Scripts\python.exe -m app.rag.ingest --reset --batch-size 2
```

If GPU memory is tight:

```powershell
.\.venv\Scripts\python.exe -m app.rag.ingest --reset --batch-size 1
```

Start the web demo:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.web_ui:app --host 127.0.0.1 --port 8080
```

Open:

```text
http://127.0.0.1:8080
```

Run the CLI demo:

```powershell
.\.venv\Scripts\python.exe main.py
```

## Delete User Details

User details are stored in:

```text
data/demo.sqlite3
logs/<student_id>_<timestamp>.log
```

Delete one student profile, memory, tool-call rows, retrieved-example rows, and logs:

```powershell
$env:STUDENT_ID = "s01"
@'
import os

from app.memory.store import MemoryStore
from app.paths import LOG_DIR

student_id = os.environ["STUDENT_ID"]
safe_student_id = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in student_id)

store = MemoryStore()
with store.connect() as conn:
    interaction_ids = [
        row["id"]
        for row in conn.execute(
            "SELECT id FROM interactions WHERE student_id = ?",
            (student_id,),
        ).fetchall()
    ]

    for interaction_id in interaction_ids:
        conn.execute("DELETE FROM tool_calls WHERE interaction_id = ?", (interaction_id,))
        conn.execute("DELETE FROM retrieved_examples WHERE interaction_id = ?", (interaction_id,))

    conn.execute("DELETE FROM interactions WHERE student_id = ?", (student_id,))
    conn.execute("DELETE FROM memory_summaries WHERE student_id = ?", (student_id,))
    conn.execute("DELETE FROM student_profiles WHERE student_id = ?", (student_id,))
    conn.execute("DELETE FROM students WHERE student_id = ?", (student_id,))

for path in LOG_DIR.glob(f"{safe_student_id}_*.log"):
    path.unlink()

print(f"Deleted details for {student_id}")
'@ | .\.venv\Scripts\python.exe -
```

Delete all demo user details and logs:

```powershell
Remove-Item -LiteralPath .\data\demo.sqlite3 -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath .\logs -Recurse -Force -ErrorAction SilentlyContinue
```

This does not delete the RAG index, dataset, or embedding model.
