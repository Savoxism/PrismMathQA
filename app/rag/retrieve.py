"""ChromaDB retrieval for ICL examples."""

from __future__ import annotations

from dataclasses import dataclass

from app.paths import CHROMA_DIR, METAMATH_SAMPLE_PATH, RAG_COLLECTION
from app.rag.dataset import load_examples
from app.rag.embedder import QwenEmbedder


@dataclass(frozen=True)
class RetrievedExample:
    example_id: str
    question: str
    answer: str
    score: float


class RAGRetriever:
    def __init__(self, top_k: int = 3) -> None:
        import chromadb

        if not CHROMA_DIR.exists():
            raise FileNotFoundError("Missing Chroma index. Run `python -m app.rag.ingest` first.")
        self.top_k = top_k
        self.examples = load_examples(METAMATH_SAMPLE_PATH)
        self.embedder = QwenEmbedder()
        self.collection = chromadb.PersistentClient(path=str(CHROMA_DIR)).get_collection(RAG_COLLECTION)

    def retrieve(self, question: str) -> list[RetrievedExample]:
        query_embedding = self.embedder.encode([question])[0]
        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=self.top_k,
            include=["distances"],
        )
        ids = result["ids"][0]
        distances = result.get("distances", [[0.0] * len(ids)])[0]
        examples: list[RetrievedExample] = []
        for example_id, distance in zip(ids, distances):
            item = self.examples[example_id]
            examples.append(
                RetrievedExample(
                    example_id=example_id,
                    question=item["question"],
                    answer=item["answer"],
                    score=1.0 - float(distance),
                )
            )
        return examples
