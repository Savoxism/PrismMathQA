"""CLI for embedding and indexing the local MetaMathQA sample."""

from __future__ import annotations

import argparse
from itertools import islice

from app.paths import CHROMA_DIR, RAG_COLLECTION
from app.rag.dataset import load_examples
from app.rag.embedder import QwenEmbedder


def batched(items: list[dict], size: int):
    if size < 1:
        raise ValueError("batch size must be >= 1")
    iterator = iter(items)
    while batch := list(islice(iterator, size)):
        yield batch


def ingest(batch_size: int = 16, reset: bool = False) -> int:
    import chromadb

    examples = list(load_examples(METAMATH_SAMPLE_PATH).values())
    embedder = QwenEmbedder(batch_size=batch_size)
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    if reset:
        try:
            client.delete_collection(RAG_COLLECTION)
        except Exception:
            pass
    collection = client.get_or_create_collection(name=RAG_COLLECTION, metadata={"hnsw:space": "cosine"})

    for batch in batched(examples, batch_size):
        ids = [item["id"] for item in batch]
        questions = [item["question"] for item in batch]
        embeddings = embedder.encode(questions)
        metadatas = [
            {"source": item["source"], "type": item.get("type", ""), "answer_len": len(item["answer"])}
            for item in batch
        ]
        collection.upsert(ids=ids, documents=questions, metadatas=metadatas, embeddings=embeddings)
    return collection.count()


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare MetaMathQA ChromaDB index.")
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--batch-size", type=int, default=4)
    args = parser.parse_args()

    print(f"Indexed {ingest(batch_size=args.batch_size, reset=args.reset)} examples into {RAG_COLLECTION}")


if __name__ == "__main__":
    main()
