from __future__ import annotations

import json
import sys
import tempfile
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from experiments.config import MemoryConfig  # noqa: E402
from experiments.memory import ReadOnlyMemoryBackend, create_memory_backend  # noqa: E402


class NonCopyableEmbedder:
    """Small local embedder that also detects concurrent access."""

    def __init__(self):
        self.lock = threading.Lock()
        self.calls = 0
        self.active = 0
        self.max_active = 0

    def __deepcopy__(self, memo):
        raise AssertionError("the shared embedder must not be copied")

    def _embed(self, text):
        with self.lock:
            self.calls += 1
            self.active += 1
            self.max_active = max(self.max_active, self.active)
        time.sleep(0.001)
        try:
            return [float(sum(ord(character) for character in text) % 17), 1.0]
        finally:
            with self.lock:
                self.active -= 1

    def embed_query(self, text):
        return self._embed(text)

    def embed_document(self, text):
        return self._embed(text)


class MemorySnapshotViewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        initial_path = Path(self.tmp.name) / "initial.json"
        initial_path.write_text(
            json.dumps(
                {
                    "meta_reasoning": [],
                    "solutions_and_patterns": [
                        {
                            "id": "11111111",
                            "content": "Use coalesced memory loads for contiguous tiles",
                        }
                    ],
                    "failed_attempts": [],
                }
            )
        )
        self.config = MemoryConfig(
            initial_files={
                "triton": str(initial_path),
                "tilelang": str(initial_path),
            }
        )

    def tearDown(self):
        self.tmp.cleanup()

    def _backend(self, kind, embedder):
        return create_memory_backend(
            kind,
            "triton",
            self.config,
            embedder=embedder,
            precompute_embeddings=True,
        )

    def test_flat_and_tree_views_are_epoch_fixed_and_thread_safe(self):
        for kind in ("flat", "tree"):
            with self.subTest(kind=kind):
                embedder = NonCopyableEmbedder()
                memory = self._backend(kind, embedder)
                calls_before_snapshot = embedder.calls

                view = memory.snapshot_view()
                state_at_epoch_start = view._state_json

                self.assertIsInstance(view, ReadOnlyMemoryBackend)
                self.assertIs(view._embedder, embedder)
                self.assertEqual(embedder.calls, calls_before_snapshot)

                if kind == "flat":
                    memory.manager.data["solutions_and_patterns"][0]["content"] = "changed later"
                else:
                    memory.manager.data["items"]["11111111"]["content"] = "changed later"

                with ThreadPoolExecutor(max_workers=8) as executor:
                    reads = list(
                        executor.map(
                            lambda query: view.read(query, 3),
                            ["optimize coalesced loads"] * 16,
                        )
                    )

                self.assertTrue(all(read.item_ids == ["11111111"] for read in reads))
                self.assertTrue(all("coalesced memory loads" in read.text for read in reads))
                self.assertTrue(all("changed later" not in read.text for read in reads))
                self.assertEqual(view._state_json, state_at_epoch_start)
                self.assertEqual(embedder.max_active, 1)

    def test_snapshot_views_reject_every_mutation_api(self):
        views = [
            create_memory_backend("none", "triton", self.config).snapshot_view(),
            self._backend("flat", NonCopyableEmbedder()).snapshot_view(),
            self._backend("tree", NonCopyableEmbedder()).snapshot_view(),
        ]
        for view in views:
            with self.subTest(kind=view.kind):
                self.assertTrue(view.frozen)
                self.assertIs(view.snapshot_view(), view)
                for mutate in (
                    lambda: view.build_update_prompt("q", "a", "r"),
                    lambda: view.update("{}"),
                    lambda: view.apply_update("{}"),
                    lambda: view.record_usage("[11111111]", 1),
                    lambda: view.prune(0.5, 2),
                ):
                    with self.assertRaisesRegex(RuntimeError, "read-only"):
                        mutate()

        self.assertEqual(views[0].read("anything", 20).text, "")
        self.assertEqual(views[0].stats(), "No persistent memory")

    def test_serialized_snapshot_is_unchanged_by_retrieval(self):
        memory = self._backend("tree", NonCopyableEmbedder())
        view = memory.snapshot_view()
        before = json.loads(view._state_json)

        view.read("coalesced tile load", 3)
        snapshot_path = Path(self.tmp.name) / "snapshot.json"
        view.snapshot(str(snapshot_path))

        self.assertEqual(json.loads(snapshot_path.read_text()), before)
        self.assertIsNone(before["metadata"]["last_retrieval_context"])


if __name__ == "__main__":
    unittest.main()
