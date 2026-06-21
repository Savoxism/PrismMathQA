# PrismMath Tutor Demo

## 1. Install dependencies

```bash
cd /Users/savoxism/Documents/GitHub/NLP-Capstone-Project-20252
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip setuptools wheel
.venv/bin/python -m pip install -r requirements.txt
```

## 2. Create .env

```bash
cat > .env <<'EOF'
LLM_API_KEY=your_key_here
LLM_BASE_URL=https://your-openai-compatible-endpoint/v1
EOF
```

## 3. Expected Local files

```bash
test -f data/processed/metamathqa_30k.jsonl
test -d models/qwen3-embedding-0.6b
test -f .env
```

## 4. Build or rebuild the RAG index:

```bash
.venv/bin/python -m app.rag.ingest --reset --batch-size 1
```

## 5. Start the web demo

```bash
.venv/bin/python -m uvicorn app.web_ui:app --host 127.0.0.1 --port 8080
```

Open:

```text
http://127.0.0.1:8080
```

## 6. Delete user database (all records)

```bash
rm -f data/demo.sqlite3
```
