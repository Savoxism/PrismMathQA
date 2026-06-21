"""Qwen3 embedding loader."""

from __future__ import annotations

from pathlib import Path

from app.paths import MODEL_DIR


class QwenEmbedder:
    def __init__(
        self,
        model_dir: Path = MODEL_DIR,
        batch_size: int = 4,
        device: str | None = None,
    ) -> None:
        import torch
        from sentence_transformers import SentenceTransformer

        if not model_dir.exists() or not any(model_dir.iterdir()):
            raise FileNotFoundError(
                f"Missing Qwen3 embedding weights at {model_dir}. "
                "Download Qwen/Qwen3-Embedding-0.6B into this project directory first."
            )

        self.batch_size = batch_size
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        dtype = torch.float16 if self.device == "cuda" else torch.float32
        self.model = SentenceTransformer(
            str(model_dir),
            device=self.device,
            model_kwargs={"torch_dtype": dtype},
        )

    def encode(self, texts: list[str]) -> list[list[float]]:
        vectors = self.model.encode(
            texts,
            batch_size=self.batch_size,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=len(texts) > self.batch_size,
        )
        return vectors.astype("float32").tolist()
