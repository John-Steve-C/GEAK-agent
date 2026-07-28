from __future__ import annotations

import copy
import json
import re
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from memories.CheatsheetManager import CheatsheetManager
from memories.TreeCheatsheetManager_v3 import TreeCheatsheetManager

from .config import MemoryConfig
from .embedding import LocalQwenEmbedder


def _atomic_json(path: str, payload: Dict[str, Any]) -> None:
    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    temporary = path_obj.with_suffix(path_obj.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
    temporary.replace(path_obj)


@dataclass
class MemoryRead:
    text: str
    item_ids: List[str] = field(default_factory=list)
    tree_paths: List[str] = field(default_factory=list)


class MemoryBackend:
    kind = "none"

    def read(self, query: str, top_k: int) -> MemoryRead:
        return MemoryRead(text="")

    def build_update_prompt(self, question: str, answer: str, reflection: str) -> str:
        return ""

    def update(self, response: str) -> None:
        raise RuntimeError("none memory does not accept updates")

    def apply_update(self, response: str) -> None:
        self.update(response)

    def record_usage(
        self,
        model_thought: str,
        current_iter: int,
        *,
        pass_call: bool = False,
        pass_correctness: bool = False,
    ) -> None:
        return None

    def prune(self, threshold: float, age_threshold: int) -> None:
        return None

    def snapshot(self, path: str) -> None:
        _atomic_json(path, {"kind": self.kind, "frozen": True})

    def freeze(self) -> None:
        return None

    def snapshot_view(self) -> "MemoryBackend":
        """Return an immutable view of the memory's current epoch state."""
        return ReadOnlyMemoryBackend(kind=self.kind)

    def has_commit(self, commit_key: str) -> bool:
        return False

    def mark_commit(self, commit_key: str) -> None:
        return None

    @property
    def frozen(self) -> bool:
        return True

    def stats(self) -> str:
        return "No persistent memory"


class ReadOnlyMemoryBackend(MemoryBackend):
    """An immutable memory snapshot safe to share between task workers.

    Snapshot state is stored as JSON rather than as a live manager object. Each
    read gets an isolated manager, so retrieval helpers may populate temporary
    embeddings or retrieval metadata without changing the epoch-start state.
    The embedder is intentionally shared (not copied) and access to it is
    serialized because local model/cache implementations commonly own locks and
    other non-copyable resources.
    """

    def __init__(
        self,
        *,
        kind: str,
        state: Optional[Dict[str, Any]] = None,
        embedder=None,
        current_iteration: int = 0,
        use_fixed_categories: bool = True,
    ):
        if kind not in {"none", "flat", "tree"}:
            raise ValueError(f"unsupported read-only memory kind: {kind}")
        self.kind = kind
        self._state_json = (
            json.dumps(state, ensure_ascii=False) if state is not None else None
        )
        self._embedder = embedder
        self._current_iteration = current_iteration
        self._use_fixed_categories = use_fixed_categories
        self._read_lock = threading.RLock()

    @classmethod
    def from_backend(
        cls, backend: "ManagedMemoryBackend"
    ) -> "ReadOnlyMemoryBackend":
        return cls(
            kind=backend.kind,
            state=backend.manager.data,
            embedder=backend.manager.embedder,
            current_iteration=backend.manager.current_iteration,
            use_fixed_categories=getattr(
                backend.manager, "use_fixed_categories", True
            ),
        )

    def _require_mutable(self) -> None:
        raise RuntimeError("memory snapshot is read-only")

    def _new_manager(self):
        if self._state_json is None:
            return None
        state = json.loads(self._state_json)
        if self.kind == "flat":
            manager = CheatsheetManager(initial_state=state, embedder=self._embedder)
        else:
            manager = TreeCheatsheetManager(
                initial_state=state,
                use_fixed_categories=self._use_fixed_categories,
                embedder=self._embedder,
            )
        manager.current_iteration = self._current_iteration
        return manager

    def read(self, query: str, top_k: int) -> MemoryRead:
        if self.kind == "none":
            return MemoryRead(text="")
        # The manager is per-read; the lock protects only the shared embedder and
        # its cache/model state. It also makes custom embedders safe by default.
        with self._read_lock:
            manager = self._new_manager()
            return _read_manager(manager, self.kind, query, top_k)

    def build_update_prompt(self, question: str, answer: str, reflection: str) -> str:
        self._require_mutable()

    def update(self, response: str) -> None:
        self._require_mutable()

    def record_usage(
        self,
        model_thought: str,
        current_iter: int,
        *,
        pass_call: bool = False,
        pass_correctness: bool = False,
    ) -> None:
        self._require_mutable()

    def prune(self, threshold: float, age_threshold: int) -> None:
        self._require_mutable()

    def snapshot(self, path: str) -> None:
        if self._state_json is None:
            return super().snapshot(path)
        _atomic_json(path, json.loads(self._state_json))

    def freeze(self) -> None:
        return None

    def snapshot_view(self) -> "ReadOnlyMemoryBackend":
        return self

    def mark_commit(self, commit_key: str) -> None:
        self._require_mutable()

    @property
    def frozen(self) -> bool:
        return True

    def stats(self) -> str:
        if self.kind == "none":
            return super().stats()
        with self._read_lock:
            return self._new_manager().get_stats()


def _read_manager(manager, kind: str, query: str, top_k: int) -> MemoryRead:
    text = manager.to_string_for_prompt(top_k_hot=top_k, query=query)
    context = manager.data.get("metadata", {}).get("last_retrieval_context") or {}
    item_ids = list(context.get("item_ids", []))
    if not item_ids:
        item_ids = re.findall(r"\[ID:\s*([^\]]+)\]", text)
    tree_paths = []
    if kind == "tree":
        for line in text.splitlines():
            if line.startswith("- Path: "):
                tree_paths.append(line.removeprefix("- Path: "))
    return MemoryRead(text=text, item_ids=item_ids, tree_paths=tree_paths)


class ManagedMemoryBackend(MemoryBackend):
    def __init__(self, manager, kind: str, frozen: bool = False):
        self.manager = manager
        self.kind = kind
        self._frozen = frozen

    @property
    def frozen(self) -> bool:
        return self._frozen

    def _require_mutable(self) -> None:
        if self._frozen:
            raise RuntimeError("memory is frozen during held-out evaluation")

    def read(self, query: str, top_k: int) -> MemoryRead:
        original_data = copy.deepcopy(self.manager.data) if self._frozen else None
        try:
            return _read_manager(self.manager, self.kind, query, top_k)
        finally:
            if original_data is not None:
                self.manager.data = original_data

    def build_update_prompt(self, question: str, answer: str, reflection: str) -> str:
        self._require_mutable()
        return self.manager.build_prompt(question, answer, reflection)

    def update(self, response: str) -> None:
        self._require_mutable()
        self.manager.apply_operations(response)

    def record_usage(
        self,
        model_thought: str,
        current_iter: int,
        *,
        pass_call: bool = False,
        pass_correctness: bool = False,
    ) -> None:
        self._require_mutable()
        self.manager.record_usage(
            model_thought,
            current_iter,
            pass_call=pass_call,
            pass_exe=pass_correctness,
        )

    def prune(self, threshold: float, age_threshold: int) -> None:
        self._require_mutable()
        self.manager.prune_by_utility(
            min_usage_ratio=threshold,
            age_threshold=age_threshold,
        )

    def snapshot(self, path: str) -> None:
        _atomic_json(path, self.manager.data)

    def freeze(self) -> None:
        self._frozen = True

    def snapshot_view(self) -> ReadOnlyMemoryBackend:
        return ReadOnlyMemoryBackend.from_backend(self)

    def has_commit(self, commit_key: str) -> bool:
        commits = self.manager.data.get("metadata", {}).get("experiment_commit_keys", [])
        return commit_key in commits

    def mark_commit(self, commit_key: str) -> None:
        self._require_mutable()
        metadata = self.manager.data.setdefault("metadata", {})
        commits = metadata.setdefault("experiment_commit_keys", [])
        if commit_key not in commits:
            commits.append(commit_key)

    def stats(self) -> str:
        return self.manager.get_stats()

    def precompute_embeddings(self) -> None:
        if self.kind == "tree":
            items = list(self.manager.data.get("items", {}).values())
        else:
            items = [
                item
                for section in self.manager.sections
                for item in self.manager.data.get(section, [])
            ]
        for item in items:
            self.manager._ensure_embedding(item)


def _load_state(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def create_memory_backend(
    kind: str,
    dsl: str,
    config: MemoryConfig,
    *,
    state_path: Optional[str] = None,
    embedder=None,
    precompute_embeddings: bool = True,
) -> MemoryBackend:
    if kind == "none":
        return MemoryBackend()
    source_path = state_path or config.initial_files[dsl]
    state = _load_state(source_path)
    embedder = embedder or LocalQwenEmbedder(
        model_path=config.embedding_model,
        cache_path=config.embedding_cache,
    )
    if kind == "flat":
        manager = CheatsheetManager(initial_state=state, embedder=embedder)
    elif kind == "tree":
        manager = TreeCheatsheetManager(
            initial_state=state,
            use_fixed_categories=config.use_fixed_categories,
            embedder=embedder,
        )
    else:
        raise ValueError(f"unsupported memory backend: {kind}")
    backend = ManagedMemoryBackend(manager=manager, kind=kind)
    if precompute_embeddings:
        backend.precompute_embeddings()
    return backend
