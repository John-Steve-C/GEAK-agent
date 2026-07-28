from __future__ import annotations

import hashlib
import json
import os
import threading
from pathlib import Path
from typing import Dict, List, Optional


DEFAULT_RETRIEVAL_INSTRUCTION = (
    "Given a GPU kernel optimization task, retrieve relevant reusable optimization, "
    "correctness, and debugging guidance"
)


class LocalQwenEmbedder:
    """Lazy local Qwen3 embedding model with query-aware disk caching."""

    def __init__(
        self,
        model_path: str,
        cache_path: str,
        *,
        device: Optional[str] = None,
        max_length: int = 8192,
        query_instruction: str = DEFAULT_RETRIEVAL_INSTRUCTION,
        local_files_only: bool = True,
    ):
        self.model_path = model_path
        self.cache_path = Path(cache_path)
        self.device = device or os.environ.get("GEAK_EMBEDDING_DEVICE", "cpu")
        self.max_length = max_length
        self.query_instruction = query_instruction
        self.local_files_only = local_files_only
        self._tokenizer = None
        self._model = None
        self._model_lock = threading.Lock()
        self._cache_lock = threading.Lock()
        self._cache: Dict[str, List[float]] = self._load_cache()

    def _load_cache(self) -> Dict[str, List[float]]:
        if not self.cache_path.exists():
            return {}
        with self.cache_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}

    def _load_model(self):
        if self._model is not None and self._tokenizer is not None:
            return self._tokenizer, self._model
        with self._model_lock:
            if self._model is not None and self._tokenizer is not None:
                return self._tokenizer, self._model
            try:
                import torch
                from transformers import AutoModel, AutoTokenizer
            except ImportError as exc:
                raise RuntimeError(
                    "torch and transformers are required for local Qwen3 embeddings"
                ) from exc

            if self.device.startswith("cuda") and not torch.cuda.is_available():
                raise RuntimeError(
                    f"embedding device {self.device!r} was requested but CUDA is unavailable"
                )
            try:
                tokenizer = AutoTokenizer.from_pretrained(
                    self.model_path,
                    padding_side="left",
                    local_files_only=self.local_files_only,
                )
                model = AutoModel.from_pretrained(
                    self.model_path,
                    local_files_only=self.local_files_only,
                )
            except Exception as exc:
                raise RuntimeError(
                    f"unable to load local Qwen3 embedding model {self.model_path!r}; "
                    "provide a local path or pre-download Qwen/Qwen3-Embedding-0.6B"
                ) from exc
            model.to(self.device)
            model.eval()
            self._tokenizer = tokenizer
            self._model = model
        return self._tokenizer, self._model

    def __call__(self, text: str) -> List[float]:
        return self.embed_document(text)

    def embed_query(self, text: str) -> List[float]:
        formatted = f"Instruct: {self.query_instruction}\nQuery:{text}"
        return self._embed(formatted, mode="query")

    def embed_document(self, text: str) -> List[float]:
        return self._embed(text, mode="document")

    def _embed(self, text: str, *, mode: str) -> List[float]:
        key = self._key(text, mode)
        with self._cache_lock:
            cached = self._cache.get(key)
        if cached is not None:
            return cached

        result = self._encode_uncached(text)
        with self._cache_lock:
            self._cache[key] = result
            self._save_cache()
        return result

    def _encode_uncached(self, text: str) -> List[float]:
        import torch
        import torch.nn.functional as functional

        tokenizer, model = self._load_model()
        batch = tokenizer(
            [text],
            padding=True,
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt",
        )
        batch = batch.to(model.device)
        with torch.inference_mode():
            output = model(**batch)
            embedding = self._last_token_pool(
                output.last_hidden_state,
                batch["attention_mask"],
            )
            embedding = functional.normalize(embedding, p=2, dim=1)
        return [float(value) for value in embedding[0].detach().cpu().tolist()]

    @staticmethod
    def _last_token_pool(last_hidden_state, attention_mask):
        import torch

        if bool((attention_mask[:, -1].sum() == attention_mask.shape[0]).item()):
            return last_hidden_state[:, -1]
        sequence_lengths = attention_mask.sum(dim=1) - 1
        batch_size = last_hidden_state.shape[0]
        return last_hidden_state[
            torch.arange(batch_size, device=last_hidden_state.device),
            sequence_lengths,
        ]

    def _key(self, text: str, mode: str) -> str:
        payload = json.dumps(
            {
                "model": self.model_path,
                "mode": mode,
                "max_length": self.max_length,
                "text": text,
            },
            sort_keys=True,
            ensure_ascii=False,
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def _save_cache(self) -> None:
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.cache_path.with_suffix(self.cache_path.suffix + ".tmp")
        with tmp_path.open("w", encoding="utf-8") as handle:
            json.dump(self._cache, handle)
        os.replace(tmp_path, self.cache_path)


# Compatibility for code importing the original adapter name.
LocalJinaEmbedder = LocalQwenEmbedder
