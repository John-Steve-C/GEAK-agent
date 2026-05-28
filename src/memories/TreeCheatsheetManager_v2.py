import json
import math
import re
import uuid
from dataclasses import asdict, dataclass
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple, Union

EmbeddingInput = Union[str, Sequence[str]]
EmbeddingOutput = Union[List[float], List[List[float]]]
Extractor = Optional[Callable[[str], Any]]
Embedder = Optional[Callable[[EmbeddingInput], EmbeddingOutput]]
Clusterer = Optional[Callable[[List[Dict[str, Any]], Dict[str, Any]], List[List[Dict[str, Any]]]]]
Summarizer = Optional[Callable[[List[Dict[str, Any]]], Dict[str, str]]]
Chunker = Optional[Callable[[str, Dict[str, Any]], List[Dict[str, Any]]]]


FIXED_CATEGORY_DESCRIPTIONS = {
    "Kernel Pattern": "Kernel implementation patterns learned from docs and training examples.",
    "Correctness Rule": "Rules that preserve correctness, masking semantics, indexing safety, and numerical behavior.",
    "Performance Rule": "Optimization rules that improve throughput, memory behavior, and autotuning decisions.",
    "Debugging Rule": "Debugging and failure-recovery rules for compile, runtime, correctness, and resource issues.",
}

CATEGORY_HINTS = {
    "Kernel Pattern": [
        "kernel",
        "elementwise",
        "reduction",
        "softmax",
        "layernorm",
        "rmsnorm",
        "matmul",
        "attention",
        "quant",
        "dequant",
        "scan",
        "copy",
        "gather",
        "scatter",
        "tiling",
    ],
    "Correctness Rule": [
        "correctness",
        "mask",
        "index",
        "boundary",
        "stride",
        "layout",
        "stability",
        "precision",
        "overflow",
        "underflow",
        "nan",
        "broadcast",
        "shape",
        "oob",
        "out of bounds",
    ],
    "Performance Rule": [
        "performance",
        "coalescing",
        "cache",
        "reuse",
        "vectorization",
        "autotuning",
        "throughput",
        "latency",
        "occupancy",
        "block size",
        "pipeline",
        "prefetch",
        "parallelism",
    ],
    "Debugging Rule": [
        "debug",
        "compile error",
        "launch error",
        "runtime error",
        "wrong answer",
        "timeout",
        "oom",
        "illegal memory",
        "traceback",
        "assert",
        "failure",
        "mismatch",
    ],
}

DEFAULT_SUBCATEGORY_BY_CATEGORY = {
    "Kernel Pattern": "General Kernel Pattern",
    "Correctness Rule": "General Correctness Rule",
    "Performance Rule": "General Performance Rule",
    "Debugging Rule": "General Debugging Rule",
}

TAXONOMY_VERSION = 2
TAXONOMY_NAME = "fixed_top_level_dynamic_tags_v1"


@dataclass
class TreeCheatsheetConfig:
    leaf_capacity: int = 10
    traversal_threshold: float = 0.35
    merge_threshold: float = 0.80
    append_threshold: float = 0.55
    prune_every: int = 20
    prune_threshold: float = -0.1
    utility_alpha: float = 1.0
    utility_beta: float = 0.2
    utility_gamma: float = 0.15
    max_chunk_chars: int = 3200
    fallback_chunk_chars: int = 1800
    leaf_cluster_size: int = 3
    branching_factor: int = 3
    max_depth: int = 6
    max_leaf_nodes_per_subcategory: int = 12
    category_top_k: int = 2
    subcategory_top_k: int = 4
    leaf_score_top_n: int = 3

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TreeCheatsheetManager:
    SCORE_WEIGHTS = {
        "usage": 0.30,
        "relevance": 0.35,
        "performance": 0.20,
        "penalty": 0.15,
    }

    def __init__(
        self,
        initial_state: Optional[Dict[str, Any]] = None,
        config: Optional[Union[TreeCheatsheetConfig, Dict[str, Any]]] = None,
    ):
        self.config = self._coerce_config(config)
        self.current_iteration = 0
        self._last_retrieval_context: Optional[Dict[str, Any]] = None
        self.data = self._empty_tree_state()
        if initial_state:
            self.data = self._load_state(initial_state)

    @staticmethod
    def _coerce_config(config: Optional[Union[TreeCheatsheetConfig, Dict[str, Any]]]) -> TreeCheatsheetConfig:
        if isinstance(config, TreeCheatsheetConfig):
            return config
        if isinstance(config, dict):
            base = TreeCheatsheetConfig()
            for key, value in config.items():
                if hasattr(base, key):
                    setattr(base, key, value)
            return base
        return TreeCheatsheetConfig()

    def _generate_id(self) -> str:
        return str(uuid.uuid4())[:8]

    def _empty_tree_state(self) -> Dict[str, Any]:
        root_id = self._generate_id()
        state = {
            "root_node_id": root_id,
            "nodes": {
                root_id: {
                    "node_id": root_id,
                    "name": "Technical Cheatsheet",
                    "description": "Root of the hierarchical technical cheatsheet.",
                    "parent_id": None,
                    "child_ids": [],
                    "item_ids": [],
                    "embedding": [],
                    "depth": 0,
                    "node_type": "root",
                    "fixed": True,
                    "slug": "technical-cheatsheet",
                    "stats": {
                        "access_count": 0,
                        "last_access_iter": -1,
                        "created_iter": 0,
                    },
                }
            },
            "items": {},
            "metadata": {
                "version": TAXONOMY_VERSION,
                "taxonomy": {
                    "name": TAXONOMY_NAME,
                    "fixed_categories": list(FIXED_CATEGORY_DESCRIPTIONS.keys()),
                },
                "update_rounds": 0,
                "last_retrieval_context": None,
                "config": self.config.to_dict(),
            },
        }
        self._initialize_fixed_categories(state)
        return state

    def _initialize_fixed_categories(self, state: Dict[str, Any]):
        root_id = state["root_node_id"]
        root = state["nodes"][root_id]
        root["child_ids"] = []
        for name, description in FIXED_CATEGORY_DESCRIPTIONS.items():
            node_id = self._generate_id()
            state["nodes"][node_id] = {
                "node_id": node_id,
                "name": name,
                "description": description,
                "parent_id": root_id,
                "child_ids": [],
                "item_ids": [],
                "embedding": [],
                "depth": 1,
                "node_type": "category",
                "fixed": True,
                "slug": self._slugify(name),
                "stats": {
                    "access_count": 0,
                    "last_access_iter": -1,
                    "created_iter": 0,
                },
            }
            root["child_ids"].append(node_id)

    def _load_state(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if self._is_taxonomy_state(state):
            loaded = {
                "root_node_id": state["root_node_id"],
                "nodes": state.get("nodes", {}),
                "items": state.get("items", {}),
                "metadata": state.get("metadata", {}),
            }
            self._normalize_loaded_taxonomy_state(loaded)
            self._last_retrieval_context = loaded["metadata"].get("last_retrieval_context")
            return loaded
        if self._is_tree_state(state):
            return self._migrate_legacy_tree_state(state)
        return self._import_flat_state(state)

    @staticmethod
    def _is_tree_state(state: Dict[str, Any]) -> bool:
        return isinstance(state, dict) and {"root_node_id", "nodes", "items"}.issubset(state.keys())

    @staticmethod
    def _is_taxonomy_state(state: Dict[str, Any]) -> bool:
        if not isinstance(state, dict):
            return False
        metadata = state.get("metadata", {})
        taxonomy = metadata.get("taxonomy", {})
        return metadata.get("version", 0) >= TAXONOMY_VERSION and taxonomy.get("name") == TAXONOMY_NAME

    def _normalize_loaded_taxonomy_state(self, state: Dict[str, Any]):
        state["metadata"].setdefault("version", TAXONOMY_VERSION)
        state["metadata"].setdefault(
            "taxonomy",
            {"name": TAXONOMY_NAME, "fixed_categories": list(FIXED_CATEGORY_DESCRIPTIONS.keys())},
        )
        state["metadata"].setdefault("update_rounds", 0)
        state["metadata"].setdefault("config", self.config.to_dict())
        for item_id, item in list(state.get("items", {}).items()):
            normalized = self._build_item_record(item)
            normalized["item_id"] = item_id
            state["items"][item_id] = normalized
        for node_id, node in state.get("nodes", {}).items():
            node.setdefault("node_id", node_id)
            node.setdefault("child_ids", [])
            node.setdefault("item_ids", [])
            node.setdefault("embedding", [])
            node.setdefault("depth", 0)
            node.setdefault("node_type", "leaf")
            node.setdefault("fixed", node.get("node_type") in {"root", "category"})
            node.setdefault("slug", self._slugify(node.get("name", node_id)))
            node.setdefault(
                "stats",
                {"access_count": 0, "last_access_iter": -1, "created_iter": 0},
            )
        self._ensure_taxonomy_skeleton(state)
        self.data = state
        self._refresh_all_embeddings()

    def _ensure_taxonomy_skeleton(self, state: Optional[Dict[str, Any]] = None):
        target = state if state is not None else self.data
        if not target["nodes"]:
            root = self._empty_tree_state()
            target.update(root)
            return
        root_id = target["root_node_id"]
        root = target["nodes"][root_id]
        root["node_type"] = "root"
        root["fixed"] = True
        root["slug"] = self._slugify(root.get("name", "Technical Cheatsheet"))
        category_ids_by_name = {}
        for child_id in list(root.get("child_ids", [])):
            node = target["nodes"].get(child_id)
            if node and node.get("node_type") == "category":
                category_ids_by_name[node["name"]] = child_id
        ordered_children = []
        for name, description in FIXED_CATEGORY_DESCRIPTIONS.items():
            node_id = category_ids_by_name.get(name)
            if node_id is None:
                node_id = self._generate_id()
                target["nodes"][node_id] = {
                    "node_id": node_id,
                    "name": name,
                    "description": description,
                    "parent_id": root_id,
                    "child_ids": [],
                    "item_ids": [],
                    "embedding": [],
                    "depth": 1,
                    "node_type": "category",
                    "fixed": True,
                    "slug": self._slugify(name),
                    "stats": {"access_count": 0, "last_access_iter": -1, "created_iter": 0},
                }
            else:
                node = target["nodes"][node_id]
                node["description"] = description
                node["parent_id"] = root_id
                node["depth"] = 1
                node["node_type"] = "category"
                node["fixed"] = True
                node["slug"] = self._slugify(name)
            ordered_children.append(node_id)
        root["child_ids"] = ordered_children

    def _import_flat_state(self, state: Dict[str, Any]) -> Dict[str, Any]:
        imported = self._empty_tree_state()
        self.data = imported
        sections = ["meta_reasoning", "solutions_and_patterns", "failed_attempts"]
        for section_name in sections:
            for old_item in state.get(section_name, []) or []:
                candidate = {
                    "item_id": old_item.get("id", self._generate_id()),
                    "key_concept": old_item.get("content", "")[:80] or section_name,
                    "short_description": old_item.get("content", ""),
                    "code_snippet": "",
                    "source_doc": "legacy_import",
                    "source_chunk_id": section_name,
                    "embedding": old_item.get("embedding", []),
                    "usage_count": old_item.get("usage_count", 0),
                    "last_used_iter": old_item.get("last_used_iter", -1),
                    "created_iter": old_item.get("created_iter", 0),
                }
                normalized = self._normalize_candidate(candidate, ancestry=[section_name.replace("_", " ")])
                self._append_candidate_to_taxonomy(normalized, allow_new_leaf=True)
        self._refresh_all_embeddings()
        return self.data

    def _migrate_legacy_tree_state(self, state: Dict[str, Any]) -> Dict[str, Any]:
        migrated = self._empty_tree_state()
        self.data = migrated
        legacy_items = list((state.get("items") or {}).values())
        if not legacy_items:
            return self._import_flat_state(state)
        for legacy_item in legacy_items:
            candidate = self._legacy_item_to_candidate(legacy_item, state)
            self._append_candidate_to_taxonomy(candidate, allow_new_leaf=True)
        self.data["metadata"]["update_rounds"] = state.get("metadata", {}).get("update_rounds", 0)
        self._refresh_all_embeddings()
        self._cleanup_dynamic_nodes()
        return self.data

    def _legacy_item_to_candidate(self, item: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        item_id = item.get("item_id") or item.get("id") or self._generate_id()
        key_concept = item.get("key_concept") or item.get("content", "")[:80] or "Legacy Item"
        short_description = item.get("short_description") or item.get("content", "")
        code_snippet = item.get("code_snippet", "")
        ancestry = self._collect_legacy_ancestry(item.get("leaf_node_id"), state)
        candidate = {
            "item_id": item_id,
            "key_concept": key_concept,
            "short_description": short_description,
            "code_snippet": code_snippet,
            "source_doc": item.get("source_doc", "legacy_tree"),
            "source_chunk_id": item.get("source_chunk_id"),
            "embedding": item.get("embedding", []),
            "utility": item.get("utility", 0.0),
            "usage_count": item.get("usage_count", 0),
            "last_used_iter": item.get("last_used_iter", -1),
            "created_iter": item.get("created_iter", 0),
            "performance_gain": item.get("performance_gain", 0.5),
            "conflict_count": item.get("conflict_count", 0),
        }
        return self._normalize_candidate(candidate, ancestry=ancestry)

    def _collect_legacy_ancestry(self, node_id: Optional[str], state: Dict[str, Any]) -> List[str]:
        names: List[str] = []
        nodes = state.get("nodes", {})
        current_id = node_id
        while current_id and current_id in nodes:
            node = nodes[current_id]
            name = node.get("name", "").strip()
            if name and name != "Technical Cheatsheet":
                names.append(name)
            current_id = node.get("parent_id")
        names.reverse()
        return names

    def _build_item_record(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        item_id = candidate.get("item_id") or self._generate_id()
        normalized = self._normalize_candidate(candidate)
        return {
            "item_id": item_id,
            "category": normalized["category"],
            "subcategory": normalized["subcategory"],
            "leaf_name": normalized["leaf_name"],
            "key_concept": normalized["key_concept"],
            "short_description": normalized["short_description"],
            "code_snippet": normalized["code_snippet"],
            "source_doc": normalized.get("source_doc"),
            "source_chunk_id": normalized.get("source_chunk_id"),
            "leaf_node_id": candidate.get("leaf_node_id"),
            "embedding": self._normalize_embedding(candidate.get("embedding")),
            "utility": float(candidate.get("utility", 0.0)),
            "usage_count": int(candidate.get("usage_count", 0)),
            "last_used_iter": int(candidate.get("last_used_iter", -1)),
            "created_iter": int(candidate.get("created_iter", self.current_iteration)),
            "performance_gain": self._clamp_score(candidate.get("performance_gain", 0.5)),
            "conflict_count": max(0, int(candidate.get("conflict_count", 0))),
        }

    def to_json(self) -> str:
        self.data["metadata"]["last_retrieval_context"] = self._last_retrieval_context
        self.data["metadata"]["config"] = self.config.to_dict()
        self.data["metadata"]["version"] = TAXONOMY_VERSION
        self.data["metadata"]["taxonomy"] = {
            "name": TAXONOMY_NAME,
            "fixed_categories": list(FIXED_CATEGORY_DESCRIPTIONS.keys()),
        }
        return json.dumps(self.data, indent=4)

    def get_stats(self) -> str:
        node_count = len(self.data["nodes"])
        item_count = len(self.data["items"])
        leaf_count = sum(1 for node in self.data["nodes"].values() if node.get("node_type") == "leaf")
        total_length = len(self.to_string_for_prompt())
        return (
            f"Nodes: {node_count} | Leaves: {leaf_count} | Items: {item_count} | "
            f"Updates: {self.data['metadata'].get('update_rounds', 0)} | "
            f"Prompt Length: {total_length} characters"
        )

    def build_bootstrap_extraction_prompt(self, chunk: str, include_code_snippet: bool = False) -> str:
        category_lines = "\n".join(f'  - "{name}"' for name in FIXED_CATEGORY_DESCRIPTIONS.keys())
        code_snippet_instructions = (
            '- Include "code_snippet" only when a short snippet is essential for the rule.\n'
            '- If code_snippet is not essential, omit the field entirely.'
            if include_code_snippet
            else '- Do not include "code_snippet" unless it is absolutely necessary. Omit it by default.'
        )
        response_schema = """
{
  "items": [
    {
      "category": "one fixed top-level category",
      "subcategory": "dynamic semantic tag such as Softmax or Masking",
      "leaf_name": "specific leaf name such as Row-wise Softmax",
      "key_concept": "short concept name",
      "short_description": "2-5 sentences covering the rule, when to use it, key constraints, and why it matters"
    }
  ]
}
""".strip()
        if include_code_snippet:
            response_schema = """
{
  "items": [
    {
      "category": "one fixed top-level category",
      "subcategory": "dynamic semantic tag such as Softmax or Masking",
      "leaf_name": "specific leaf name such as Row-wise Softmax",
      "key_concept": "short concept name",
      "short_description": "2-5 sentences covering the rule, when to use it, key constraints, and why it matters",
      "code_snippet": "optional short code example"
    }
  ]
}
""".strip()
        return f"""
You are curating a hierarchical technical cheatsheet for Triton kernels.

Return JSON only as:
{response_schema}

Allowed values for `category`:
{category_lines}

Rules:
- `category` must be exactly one allowed top-level category.
- `subcategory` is dynamic and should be a concrete semantic tag such as `Softmax`, `Masking`, `Compile Error`, or `Memory Coalescing`.
- `leaf_name` should be a more specific leaf under the subcategory, such as `Row-wise Softmax` or `Masked Max with -inf`.
- Extract concrete technical rules, not summaries of the page.
- Prefer mechanism-level concepts over broad topics.
- Make each `short_description` materially informative.
- Keep `key_concept` compact, but let `short_description` carry the substance.
- Reuse the source code only when it materially clarifies the rule.
{code_snippet_instructions}

Chunk:
{chunk}
""".strip()

    def build_reflection_update_prompt(
        self,
        question: str,
        model_answer: str,
        model_reflection: str,
        retrieved_context: Optional[Dict[str, Any]] = None,
    ) -> str:
        context_json = json.dumps(retrieved_context or {}, indent=2)
        category_lines = "\n".join(f'  - "{name}"' for name in FIXED_CATEGORY_DESCRIPTIONS.keys())
        return f"""
You are extracting reusable cheatsheet updates from a successful or failed generation attempt.

Return JSON only as:
{{
  "items": [
    {{
      "category": "one fixed top-level category",
      "subcategory": "dynamic semantic tag such as Softmax or Masking",
      "leaf_name": "specific leaf name such as Row-wise Softmax",
      "key_concept": "short concept name",
      "short_description": "new rule, bug fix, or optimization worth remembering",
      "code_snippet": "optional short code example"
    }}
  ]
}}

Allowed values for `category`:
{category_lines}

Rules:
- Keep only reusable technical insights.
- `category` must be one allowed top-level category.
- `subcategory` should be a concrete semantic tag.
- `leaf_name` should be more specific than `subcategory` when possible.
- Reject generic advice.
- Include `code_snippet` only when it captures the essential trick.

Question:
{question}

Model Answer:
{model_answer}

Model Reflection:
{model_reflection}

Retrieved Context:
{context_json}
""".strip()

    def clean_document(self, raw_text: str) -> str:
        text = re.sub(r"<script.*?>.*?</script>", " ", raw_text, flags=re.S | re.I)
        text = re.sub(r"<style.*?>.*?</style>", " ", text, flags=re.S | re.I)
        text = re.sub(r"<[^>]+>", " ", text)
        lines = []
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped:
                lines.append("")
                continue
            lowered = stripped.lower()
            if lowered in {"navigation", "table of contents", "previous", "next", "edit on github"}:
                continue
            if len(stripped) < 3 and stripped in {"|", "-", "*"}:
                continue
            lines.append(stripped)
        cleaned = "\n".join(lines)
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        return cleaned.strip()

    def chunk_document(self, raw_text: str, config: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        cfg = {**self.config.to_dict(), **(config or {})}
        max_chunk_chars = cfg["max_chunk_chars"]
        fallback_chunk_chars = cfg["fallback_chunk_chars"]
        text = self.clean_document(raw_text)
        if not text:
            return []

        blocks = re.split(r"(?=^#{1,6}\s)|(?=^```)|(?=^(?:def|class)\s+\w+)", text, flags=re.M)
        chunks: List[Dict[str, Any]] = []
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            if len(block) <= max_chunk_chars:
                chunks.append({"chunk_id": self._generate_id(), "text": block})
                continue
            paragraphs = [p.strip() for p in re.split(r"\n\s*\n", block) if p.strip()]
            current: List[str] = []
            current_len = 0
            for paragraph in paragraphs:
                para_len = len(paragraph)
                if current and current_len + para_len > max_chunk_chars:
                    chunks.append({"chunk_id": self._generate_id(), "text": "\n\n".join(current)})
                    current = []
                    current_len = 0
                if para_len > max_chunk_chars:
                    slices = [
                        paragraph[i : i + fallback_chunk_chars]
                        for i in range(0, len(paragraph), fallback_chunk_chars)
                    ]
                    for slice_text in slices:
                        chunks.append({"chunk_id": self._generate_id(), "text": slice_text})
                    continue
                current.append(paragraph)
                current_len += para_len
            if current:
                chunks.append({"chunk_id": self._generate_id(), "text": "\n\n".join(current)})
        return chunks

    def ingest_document(
        self,
        raw_text: str,
        source_doc: str,
        chunker: Chunker = None,
        extractor: Extractor = None,
        embedder: Embedder = None,
    ) -> List[Dict[str, Any]]:
        chunk_fn = chunker or (lambda text, cfg: self.chunk_document(text, cfg))
        chunks = chunk_fn(raw_text, self.config.to_dict())
        candidates: List[Dict[str, Any]] = []
        for chunk in chunks:
            extracted = self._extract_candidates_from_chunk(
                chunk["text"],
                extractor=extractor,
                source_doc=source_doc,
                source_chunk_id=chunk["chunk_id"],
            )
            candidates.extend(extracted)

        descriptions = [self._candidate_text_for_embedding(candidate) for candidate in candidates]
        embeddings = self._embed_texts(descriptions, embedder)
        for candidate, embedding in zip(candidates, embeddings):
            candidate["embedding"] = embedding
        return candidates

    def bootstrap_from_documents(
        self,
        documents: Sequence[Union[str, Dict[str, Any]]],
        extractor: Extractor,
        embedder: Embedder,
        clusterer: Clusterer,
        config: Optional[Dict[str, Any]] = None,
        summarizer: Summarizer = None,
        chunker: Chunker = None,
    ) -> Dict[str, Any]:
        all_items: List[Dict[str, Any]] = []
        for index, document in enumerate(documents):
            if isinstance(document, dict):
                raw_text = document.get("text", "")
                source_doc = document.get("source_doc", f"document_{index}")
            else:
                raw_text = document
                source_doc = f"document_{index}"
            all_items.extend(
                self.ingest_document(
                    raw_text=raw_text,
                    source_doc=source_doc,
                    chunker=chunker,
                    extractor=extractor,
                    embedder=embedder,
                )
            )
        return self.build_tree_from_items(
            items=all_items,
            embedder=embedder,
            clusterer=clusterer,
            summarizer=summarizer,
            config=config,
        )

    def build_tree_from_items(
        self,
        items: Sequence[Dict[str, Any]],
        embedder: Embedder,
        clusterer: Clusterer,
        summarizer: Summarizer,
        config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        del clusterer, summarizer
        cfg = {**self.config.to_dict(), **(config or {})}
        self.data = self._empty_tree_state()
        normalized_items = [self._build_item_record(item) for item in items]
        if not normalized_items:
            return self.data

        missing_texts = [
            self._item_text_for_embedding(item)
            for item in normalized_items
            if self._is_empty_embedding(item["embedding"])
        ]
        generated = self._embed_texts(missing_texts, embedder)
        generated_iter = iter(generated)
        for item in normalized_items:
            if self._is_empty_embedding(item["embedding"]):
                item["embedding"] = next(generated_iter, [])
            self._append_candidate_to_taxonomy(item, allow_new_leaf=True, config=cfg)

        self._cleanup_dynamic_nodes(cfg)
        self._refresh_all_embeddings()
        return self.data

    def retrieve(
        self,
        query_or_queries: Union[str, Sequence[str]],
        embedder: Embedder,
        top_k_items: int = 5,
        similarity_threshold: Optional[float] = None,
    ) -> Dict[str, Any]:
        threshold = similarity_threshold if similarity_threshold is not None else self.config.traversal_threshold
        queries = [query_or_queries] if isinstance(query_or_queries, str) else list(query_or_queries)
        query_embeddings = self._embed_texts(queries, embedder)

        matched_paths: List[List[str]] = []
        leaf_node_ids: List[str] = []
        node_scores: Dict[str, float] = {}
        leaf_scores: Dict[str, float] = {}
        item_scores: Dict[str, float] = {}

        for query, query_embedding in zip(queries, query_embeddings):
            query_routes = self._route_query(query, query_embedding, threshold)
            for path in query_routes["paths"]:
                matched_paths.append(path)
            for node_id, score in query_routes["node_scores"].items():
                node_scores[node_id] = max(node_scores.get(node_id, 0.0), score)
            for node_id, score in query_routes["leaf_scores"].items():
                leaf_scores[node_id] = max(leaf_scores.get(node_id, 0.0), score)
            for leaf_id in query_routes["leaf_ids"]:
                if leaf_id not in leaf_node_ids:
                    leaf_node_ids.append(leaf_id)

        scored_items: List[Tuple[float, Dict[str, Any]]] = []
        seen_item_ids = set()
        for leaf_id in leaf_node_ids:
            leaf = self.data["nodes"].get(leaf_id)
            if not leaf:
                continue
            for item_id in leaf["item_ids"]:
                item = self.data["items"][item_id]
                score = max(
                    self.calculate_combined_score(item, query=query, query_embedding=query_embedding)
                    for query, query_embedding in zip(queries, query_embeddings)
                )
                item_scores[item_id] = max(item_scores.get(item_id, 0.0), score)
                scored_items.append((score, item))
        scored_items.sort(key=lambda pair: pair[0], reverse=True)

        retrieved_items: List[Dict[str, Any]] = []
        for score, item in scored_items:
            if item["item_id"] in seen_item_ids:
                continue
            seen_item_ids.add(item["item_id"])
            retrieved_items.append(self._serialize_prompt_item(item, score))
            if len(retrieved_items) >= top_k_items:
                break

        result = {
            "queries": queries,
            "matched_paths": matched_paths,
            "leaf_node_ids": leaf_node_ids,
            "items": retrieved_items,
            "scores": {
                "nodes": node_scores,
                "leaves": leaf_scores,
                "items": item_scores,
            },
        }
        self._last_retrieval_context = result
        self.data["metadata"]["last_retrieval_context"] = result
        return result

    def route_item_to_leaf(
        self,
        item: Dict[str, Any],
        embedder: Embedder,
        similarity_threshold: Optional[float] = None,
    ) -> Dict[str, Any]:
        threshold = similarity_threshold if similarity_threshold is not None else self.config.append_threshold
        normalized = self._normalize_candidate(item)
        embedding = self._normalize_embedding(item.get("embedding"))
        if self._is_empty_embedding(embedding):
            embedding = self._embed_texts([self._candidate_text_for_embedding(normalized)], embedder)[0]
        category_id = self._category_node_id(normalized["category"])
        subcategory_id = self._find_or_create_subcategory_node(category_id, normalized["subcategory"], create=False)
        leaf_id = None
        score = 0.0
        if subcategory_id:
            leaf_id, score = self._find_best_leaf_under_subcategory(
                subcategory_id,
                normalized["leaf_name"],
                embedding,
                threshold,
            )
        path = [self.data["root_node_id"], category_id]
        if subcategory_id:
            path.append(subcategory_id)
        if leaf_id:
            path.append(leaf_id)
        return {
            "leaf_node_id": leaf_id,
            "matched_path": path,
            "score": score,
            "embedding": embedding,
            "category": normalized["category"],
            "subcategory": normalized["subcategory"],
            "leaf_name": normalized["leaf_name"],
        }

    def integrate_reflection(
        self,
        reflection_text: str,
        extractor: Extractor,
        embedder: Embedder,
        summarizer: Summarizer,
        config: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        del summarizer
        cfg = {**self.config.to_dict(), **(config or {})}
        candidates = self._extract_candidates_from_chunk(
            reflection_text,
            extractor=extractor,
            source_doc="reflection",
            source_chunk_id=self._generate_id(),
        )
        if not candidates:
            return []

        embeddings = self._embed_texts(
            [self._candidate_text_for_embedding(candidate) for candidate in candidates],
            embedder,
        )
        for candidate, embedding in zip(candidates, embeddings):
            candidate["embedding"] = embedding

        integrated: List[Dict[str, Any]] = []
        for candidate in candidates:
            normalized = self._normalize_candidate(candidate)
            normalized["embedding"] = candidate["embedding"]
            global_item_id, global_similarity = self._best_global_item_match(normalized["embedding"])
            if global_item_id and global_similarity >= cfg["merge_threshold"]:
                updated_item = self._merge_item(global_item_id, normalized, global_similarity)
                integrated.append(
                    {"action": "merge", "item_id": global_item_id, "score": global_similarity, "item": updated_item}
                )
                continue

            category_id = self._category_node_id(normalized["category"])
            subcategory_id = self._find_or_create_subcategory_node(category_id, normalized["subcategory"], create=True)
            leaf_id = self._resolve_leaf_for_candidate(subcategory_id, normalized, cfg)
            target_item_id, similarity = self._best_item_match(leaf_id, normalized["embedding"])
            if target_item_id and similarity >= cfg["merge_threshold"]:
                updated_item = self._merge_item(target_item_id, normalized, similarity)
                integrated.append(
                    {"action": "merge", "item_id": target_item_id, "score": similarity, "item": updated_item}
                )
                continue

            appended_item = self._append_item_to_leaf(normalized, leaf_id)
            integrated.append(
                {"action": "append", "item_id": appended_item["item_id"], "score": similarity, "item": appended_item}
            )
            if len(self.data["nodes"][leaf_id]["item_ids"]) > cfg["leaf_capacity"]:
                self.split_leaf(leaf_id, summarizer=None, embedder=embedder, clusterer=None, config=cfg)

        self.data["metadata"]["update_rounds"] += 1
        self._cleanup_dynamic_nodes(cfg)
        self._refresh_all_embeddings()
        if self.data["metadata"]["update_rounds"] % max(1, cfg["prune_every"]) == 0:
            self.prune(cfg)
        return integrated

    def split_leaf(
        self,
        node_id: str,
        summarizer: Summarizer,
        embedder: Embedder,
        clusterer: Clusterer,
        config: Optional[Dict[str, Any]] = None,
    ) -> List[str]:
        del summarizer, embedder, clusterer
        cfg = {**self.config.to_dict(), **(config or {})}
        node = self.data["nodes"].get(node_id)
        if not node or node.get("node_type") != "leaf":
            return []
        if len(node["item_ids"]) <= cfg["leaf_capacity"]:
            return []
        parent_id = node.get("parent_id")
        if not parent_id or len(self.data["nodes"][parent_id]["child_ids"]) >= cfg["max_leaf_nodes_per_subcategory"]:
            return []

        item_ids = list(node["item_ids"])
        scored = sorted(
            item_ids,
            key=lambda item_id: self.calculate_usage_score(self.data["items"][item_id]),
            reverse=True,
        )
        keep_ids = scored[: cfg["leaf_capacity"]]
        overflow_ids = scored[cfg["leaf_capacity"] :]
        if not overflow_ids:
            return []

        node["item_ids"] = keep_ids
        new_leaf_name = f"{node['name']} Variant"
        new_leaf_id = self._create_leaf_node(parent_id, new_leaf_name, description=f"Overflow items for {node['name']}.")
        self.data["nodes"][new_leaf_id]["item_ids"] = overflow_ids
        for item_id in overflow_ids:
            self.data["items"][item_id]["leaf_node_id"] = new_leaf_id
        self._refresh_ancestors(new_leaf_id)
        self._refresh_ancestors(node_id)
        return [new_leaf_id]

    def prune(self, config: Optional[Dict[str, Any]] = None) -> List[str]:
        cfg = {**self.config.to_dict(), **(config or {})}
        removed_item_ids: List[str] = []
        for item_id, item in list(self.data["items"].items()):
            relevance = max(0.0, self.calculate_semantic_relevance(item))
            frequency = float(item.get("usage_count", 0))
            age = max(0, self.current_iteration - item.get("last_used_iter", -1))
            recency = 1.0 / (1.0 + age)
            utility = (
                cfg["utility_alpha"] * relevance
                - cfg["utility_beta"] * frequency
                + cfg["utility_gamma"] * recency
            )
            item["utility"] = utility
            if utility < cfg["prune_threshold"]:
                leaf_id = item.get("leaf_node_id")
                if leaf_id and leaf_id in self.data["nodes"] and item_id in self.data["nodes"][leaf_id]["item_ids"]:
                    self.data["nodes"][leaf_id]["item_ids"].remove(item_id)
                del self.data["items"][item_id]
                removed_item_ids.append(item_id)
        if removed_item_ids:
            self._cleanup_dynamic_nodes(cfg)
            self._refresh_all_embeddings()
        return removed_item_ids

    def to_string_for_prompt(self, top_k_hot: int = -1) -> str:
        output: List[str] = []
        context = self._last_retrieval_context
        if context and context.get("items"):
            output.append("=== RETRIEVED TREE PATHS ===")
            for path in context.get("matched_paths", []):
                names = [self.data["nodes"][node_id]["name"] for node_id in path if node_id in self.data["nodes"]]
                if names:
                    output.append(" > ".join(names))
            output.append("")
            output.append("=== RETRIEVED ITEMS ===")
            for item in context.get("items", []):
                stored = self.data["items"].get(item["item_id"])
                if stored:
                    output.extend(self._render_prompt_item(stored, item.get("score")))
            return "\n".join(output).strip()

        output.append("=== TREE OVERVIEW ===")
        root = self.data["nodes"][self.data["root_node_id"]]
        output.append(f"{root['name']}: {root['description']}")
        category_ids = root.get("child_ids", [])
        for category_id in category_ids:
            category = self.data["nodes"][category_id]
            output.append("")
            output.append(f"## {category['name']}")
            subcategories = [self.data["nodes"][child_id] for child_id in category["child_ids"] if child_id in self.data["nodes"]]
            subcategories.sort(
                key=lambda node: (node["stats"].get("access_count", 0), len(node["child_ids"])),
                reverse=True,
            )
            if top_k_hot != -1:
                subcategories = subcategories[:top_k_hot]
            if not subcategories:
                output.append("(Empty)")
                continue
            for subcategory in subcategories:
                output.append(f"- {subcategory['name']}")
                leaves = [self.data["nodes"][leaf_id] for leaf_id in subcategory["child_ids"] if leaf_id in self.data["nodes"]]
                leaves.sort(
                    key=lambda node: (node["stats"].get("access_count", 0), len(node["item_ids"])),
                    reverse=True,
                )
                if top_k_hot != -1:
                    leaves = leaves[:top_k_hot]
                for leaf in leaves:
                    output.append(f"  - {leaf['name']}")
                    items = [self.data["items"][item_id] for item_id in leaf["item_ids"] if item_id in self.data["items"]]
                    items.sort(key=lambda item: item.get("usage_count", 0), reverse=True)
                    if top_k_hot != -1:
                        items = items[:top_k_hot]
                    for item in items:
                        output.append(f"    - [ID: {item['item_id']}] {item['key_concept']}: {item['short_description']}")
        return "\n".join(output).strip()

    def record_usage(self, model_thought: Union[str, List[str]], current_iter: int):
        self.current_iteration = current_iter
        if isinstance(model_thought, str):
            bracket_matches = re.findall(r"\[(.*?)\]", model_thought)
            candidates = []
            for match in bracket_matches:
                candidates.extend([part.strip() for part in match.split(",")])
        elif isinstance(model_thought, list):
            candidates = model_thought
        else:
            return

        seen = set()
        for candidate in candidates:
            if re.fullmatch(r"[a-f0-9]{8}", candidate):
                seen.add(candidate)
        for item_id in seen:
            item = self.data["items"].get(item_id)
            if not item:
                continue
            item["usage_count"] += 1
            item["last_used_iter"] = current_iter
            self._bump_node_usage(item.get("leaf_node_id"), current_iter)

    def apply_operations(self, llm_response: str):
        try:
            clean_response = llm_response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:-3]
            elif clean_response.startswith("```"):
                clean_response = clean_response[3:-3]
            parsed = json.loads(clean_response)
        except Exception:
            return

        for op in parsed.get("operations", []):
            op_type = op.get("type", "").upper()
            if op_type == "ADD":
                candidate = {
                    "category": op.get("category"),
                    "subcategory": op.get("subcategory"),
                    "leaf_name": op.get("leaf_name"),
                    "key_concept": op.get("key_concept") or op.get("section", "Insight").replace("_", " "),
                    "short_description": op.get("content", ""),
                    "code_snippet": op.get("code_snippet", ""),
                    "source_doc": "legacy_operation",
                    "source_chunk_id": op.get("section", "unknown"),
                }
                self.integrate_reflection(
                    reflection_text=json.dumps({"items": [candidate]}),
                    extractor=lambda _: {"items": [candidate]},
                    embedder=None,
                    summarizer=None,
                )
            elif op_type == "UPDATE":
                target_id = op.get("target_id")
                if target_id in self.data["items"]:
                    item = self.data["items"][target_id]
                    item["short_description"] = op.get("content", item["short_description"])
                    if op.get("category") or op.get("subcategory") or op.get("leaf_name"):
                        normalized = self._normalize_candidate(
                            {
                                **item,
                                "category": op.get("category", item["category"]),
                                "subcategory": op.get("subcategory", item["subcategory"]),
                                "leaf_name": op.get("leaf_name", item["leaf_name"]),
                            }
                        )
                        item["category"] = normalized["category"]
                        item["subcategory"] = normalized["subcategory"]
                        item["leaf_name"] = normalized["leaf_name"]
            elif op_type in {"VARIATION", "EXPAND"}:
                target_id = op.get("target_id")
                if target_id in self.data["items"]:
                    extra = op.get("content", "")
                    snippet = self.data["items"][target_id].get("code_snippet", "")
                    self.data["items"][target_id]["code_snippet"] = "\n".join(
                        part for part in [snippet, extra] if part
                    )
        self._cleanup_dynamic_nodes()
        self._refresh_all_embeddings()

    def _extract_candidates_from_chunk(
        self,
        chunk_text: str,
        extractor: Extractor,
        source_doc: str,
        source_chunk_id: str,
    ) -> List[Dict[str, Any]]:
        extracted = extractor(chunk_text) if extractor else None
        candidates = self._normalize_extractor_output(extracted, chunk_text)
        normalized: List[Dict[str, Any]] = []
        for candidate in candidates:
            normalized_candidate = self._normalize_candidate(
                {
                    "category": candidate.get("category"),
                    "subcategory": candidate.get("subcategory"),
                    "leaf_name": candidate.get("leaf_name"),
                    "key_concept": candidate.get("key_concept", "").strip(),
                    "short_description": candidate.get("short_description", "").strip(),
                    "code_snippet": candidate.get("code_snippet", "").strip(),
                    "source_doc": candidate.get("source_doc", source_doc),
                    "source_chunk_id": candidate.get("source_chunk_id", source_chunk_id),
                }
            )
            if normalized_candidate["short_description"]:
                normalized.append(normalized_candidate)
        return normalized

    def _normalize_extractor_output(self, extracted: Any, fallback_text: str) -> List[Dict[str, Any]]:
        if extracted is None:
            return [self._fallback_candidate_from_text(fallback_text)]
        if isinstance(extracted, dict):
            if "items" in extracted and isinstance(extracted["items"], list):
                return [item for item in extracted["items"] if isinstance(item, dict)]
            if {"key_concept", "short_description"}.issubset(extracted.keys()):
                return [extracted]
        if isinstance(extracted, list):
            return [item for item in extracted if isinstance(item, dict)]
        if isinstance(extracted, str):
            try:
                parsed = json.loads(extracted)
                return self._normalize_extractor_output(parsed, fallback_text)
            except json.JSONDecodeError:
                return [self._fallback_candidate_from_text(extracted)]
        return [self._fallback_candidate_from_text(fallback_text)]

    def _fallback_candidate_from_text(self, text: str) -> Dict[str, Any]:
        cleaned = text.strip()
        first_line = cleaned.splitlines()[0] if cleaned else "Document chunk"
        first_line = first_line.lstrip("#").strip()[:80]
        key_concept = first_line or "Document chunk"
        return self._normalize_candidate(
            {
                "key_concept": key_concept,
                "short_description": cleaned[: self.config.max_chunk_chars],
                "code_snippet": "",
            }
        )

    def _normalize_candidate(self, candidate: Dict[str, Any], ancestry: Optional[Sequence[str]] = None) -> Dict[str, Any]:
        ancestry = list(ancestry or [])
        key_concept = (candidate.get("key_concept") or "").strip()
        short_description = (candidate.get("short_description") or candidate.get("content") or "").strip()
        code_snippet = (candidate.get("code_snippet") or "").strip()
        combined_text = "\n".join(part for part in ancestry + [key_concept, short_description, code_snippet] if part).strip()
        category = self._normalize_category(candidate.get("category"), combined_text)
        subcategory = self._normalize_dynamic_label(
            candidate.get("subcategory"),
            self._infer_subcategory(combined_text, category, ancestry),
        )
        leaf_name = self._normalize_dynamic_label(
            candidate.get("leaf_name"),
            key_concept or self._infer_leaf_name(combined_text, subcategory),
        )
        if not key_concept:
            key_concept = leaf_name or subcategory
        if not short_description:
            short_description = combined_text[: self.config.max_chunk_chars]
        return {
            "category": category,
            "subcategory": subcategory,
            "leaf_name": leaf_name or subcategory,
            "key_concept": key_concept,
            "short_description": short_description,
            "code_snippet": code_snippet,
            "source_doc": candidate.get("source_doc"),
            "source_chunk_id": candidate.get("source_chunk_id"),
            "performance_gain": candidate.get("performance_gain", 0.5),
            "conflict_count": candidate.get("conflict_count", 0),
        }

    def _normalize_category(self, category: Any, fallback_text: str) -> str:
        if isinstance(category, str):
            cleaned = " ".join(category.strip().split())
            for name in FIXED_CATEGORY_DESCRIPTIONS.keys():
                if cleaned.lower() == name.lower():
                    return name
        return self._infer_category(fallback_text)

    def _infer_category(self, text: str) -> str:
        lowered = text.lower()
        best_name = "Kernel Pattern"
        best_score = -1
        for name, keywords in CATEGORY_HINTS.items():
            score = 0
            for keyword in keywords:
                if keyword in lowered:
                    score += 1
            if score > best_score:
                best_name = name
                best_score = score
        return best_name

    def _infer_subcategory(self, text: str, category: str, ancestry: Sequence[str]) -> str:
        lowered = text.lower()
        candidates_by_category = {
            "Kernel Pattern": [
                "Softmax",
                "Matmul",
                "Attention",
                "LayerNorm / RMSNorm",
                "Reduction",
                "Elementwise",
                "Quantization / Dequantization",
            ],
            "Correctness Rule": [
                "Masking",
                "Indexing",
                "Boundary Handling",
                "Strides / Layout",
                "Numerical Stability",
            ],
            "Performance Rule": [
                "Memory Coalescing",
                "Block Size",
                "Program ID Mapping",
                "Cache / Reuse",
                "Vectorization",
                "Autotuning",
            ],
            "Debugging Rule": [
                "Compile Error",
                "Runtime Error",
                "Wrong Answer",
                "Timeout",
                "OOM",
            ],
        }
        candidates = candidates_by_category.get(category, [])
        for candidate in candidates:
            if candidate.lower().replace(" / ", " ").replace("/", " ") in lowered:
                return candidate
        for name in reversed(list(ancestry)):
            pieces = [piece.strip() for piece in re.split(r"[|,/]", name) if piece.strip()]
            for piece in pieces:
                cleaned = self._normalize_dynamic_label(piece, "")
                if 2 <= len(cleaned) <= 48 and cleaned not in FIXED_CATEGORY_DESCRIPTIONS:
                    return cleaned
        for name in reversed(list(ancestry)):
            cleaned = self._normalize_dynamic_label(name, "")
            if cleaned and cleaned not in FIXED_CATEGORY_DESCRIPTIONS:
                return cleaned
        return DEFAULT_SUBCATEGORY_BY_CATEGORY.get(category, "General Rule")

    def _infer_leaf_name(self, text: str, subcategory: str) -> str:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for line in lines:
            if len(line) <= 80:
                cleaned = self._normalize_dynamic_label(line, "")
                if cleaned and cleaned.lower() != subcategory.lower():
                    return cleaned
        return subcategory

    def _normalize_dynamic_label(self, value: Any, fallback: str) -> str:
        raw = value if isinstance(value, str) and value.strip() else fallback
        cleaned = re.sub(r"\s+", " ", str(raw or "").replace("_", " ")).strip(" -:/")
        if not cleaned:
            return "General Rule"
        tokens = []
        for token in re.split(r"(\s+|/|-)", cleaned):
            if not token or token.isspace() or token in {"/", "-"}:
                tokens.append(token)
                continue
            if token.isupper() or len(token) <= 2:
                tokens.append(token)
            else:
                tokens.append(token[0].upper() + token[1:])
        return "".join(tokens).strip()

    def _candidate_text_for_embedding(self, candidate: Dict[str, Any]) -> str:
        parts = [
            candidate.get("category", ""),
            candidate.get("subcategory", ""),
            candidate.get("leaf_name", ""),
            candidate.get("key_concept", ""),
            candidate.get("short_description", ""),
            candidate.get("code_snippet", ""),
        ]
        return "\n".join(part for part in parts if part).strip()

    def _item_text_for_embedding(self, item: Dict[str, Any]) -> str:
        return self._candidate_text_for_embedding(item)

    def _embed_texts(self, texts: Sequence[str], embedder: Embedder) -> List[List[float]]:
        if not texts:
            return []
        if embedder is None:
            return [self._normalize_embedding(self._default_embed_text(text)) for text in texts]
        embedded = embedder(list(texts))
        if self._looks_like_single_embedding(embedded):
            return [self._normalize_embedding(embedded)]
        return [self._normalize_embedding(vector) for vector in embedded]  # type: ignore[arg-type]

    def _default_embed_text(self, text: str, dims: int = 16) -> List[float]:
        try:
            from retrievers.retrieve_utils import get_embedding

            return self._normalize_embedding(get_embedding(text))  # type: ignore[arg-type]
        except Exception:
            tokens = re.findall(r"[a-zA-Z_][a-zA-Z0-9_+-]*", text.lower())
            vector = [0.0] * dims
            for token in tokens:
                index = hash(token) % dims
                vector[index] += 1.0
            norm = self._vector_norm(vector)
            if norm == 0.0:
                return vector
            return [value / norm for value in vector]

    def _append_candidate_to_taxonomy(
        self,
        candidate: Dict[str, Any],
        allow_new_leaf: bool,
        config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        cfg = {**self.config.to_dict(), **(config or {})}
        item = self._build_item_record(candidate)
        category_id = self._category_node_id(item["category"])
        subcategory_id = self._find_or_create_subcategory_node(category_id, item["subcategory"], create=True)
        leaf_id = self._resolve_leaf_for_candidate(subcategory_id, item, cfg, allow_new_leaf=allow_new_leaf)
        item["leaf_node_id"] = leaf_id
        self.data["items"][item["item_id"]] = item
        self.data["nodes"][leaf_id]["item_ids"].append(item["item_id"])
        self._refresh_ancestors(leaf_id)
        return item

    def _category_node_id(self, category_name: str) -> str:
        root = self.data["nodes"][self.data["root_node_id"]]
        for child_id in root["child_ids"]:
            node = self.data["nodes"][child_id]
            if node["name"] == category_name:
                return child_id
        raise KeyError(f"Missing category node: {category_name}")

    def _find_or_create_subcategory_node(self, category_id: str, subcategory_name: str, create: bool) -> Optional[str]:
        slug = self._slugify(subcategory_name)
        category = self.data["nodes"][category_id]
        for child_id in category["child_ids"]:
            node = self.data["nodes"].get(child_id)
            if node and node.get("node_type") == "subcategory" and node.get("slug") == slug:
                return child_id
        if not create:
            return None
        node_id = self._generate_id()
        self.data["nodes"][node_id] = {
            "node_id": node_id,
            "name": subcategory_name,
            "description": f"Dynamic semantic tag under {category['name']}.",
            "parent_id": category_id,
            "child_ids": [],
            "item_ids": [],
            "embedding": [],
            "depth": category["depth"] + 1,
            "node_type": "subcategory",
            "fixed": False,
            "slug": slug,
            "stats": {
                "access_count": 0,
                "last_access_iter": -1,
                "created_iter": self.current_iteration,
            },
        }
        category["child_ids"].append(node_id)
        return node_id

    def _create_leaf_node(self, subcategory_id: str, leaf_name: str, description: Optional[str] = None) -> str:
        parent = self.data["nodes"][subcategory_id]
        node_id = self._generate_id()
        self.data["nodes"][node_id] = {
            "node_id": node_id,
            "name": leaf_name,
            "description": description or f"Specific leaf under {parent['name']}.",
            "parent_id": subcategory_id,
            "child_ids": [],
            "item_ids": [],
            "embedding": [],
            "depth": parent["depth"] + 1,
            "node_type": "leaf",
            "fixed": False,
            "slug": self._slugify(leaf_name),
            "stats": {
                "access_count": 0,
                "last_access_iter": -1,
                "created_iter": self.current_iteration,
            },
        }
        parent["child_ids"].append(node_id)
        return node_id

    def _resolve_leaf_for_candidate(
        self,
        subcategory_id: str,
        candidate: Dict[str, Any],
        cfg: Dict[str, Any],
        allow_new_leaf: bool = True,
    ) -> str:
        exact_leaf_id = self._find_exact_leaf(subcategory_id, candidate["leaf_name"])
        if exact_leaf_id:
            return exact_leaf_id
        best_leaf_id, best_score = self._find_best_leaf_under_subcategory(
            subcategory_id,
            candidate["leaf_name"],
            candidate.get("embedding", []),
            cfg["append_threshold"],
        )
        if best_leaf_id and best_score >= cfg["append_threshold"]:
            return best_leaf_id
        leaf_children = self.data["nodes"][subcategory_id]["child_ids"]
        if allow_new_leaf and len(leaf_children) < cfg["max_leaf_nodes_per_subcategory"]:
            return self._create_leaf_node(subcategory_id, candidate["leaf_name"])
        if best_leaf_id:
            return best_leaf_id
        if leaf_children:
            return leaf_children[0]
        return self._create_leaf_node(subcategory_id, candidate["leaf_name"])

    def _find_exact_leaf(self, subcategory_id: str, leaf_name: str) -> Optional[str]:
        target_slug = self._slugify(leaf_name)
        for child_id in self.data["nodes"][subcategory_id]["child_ids"]:
            child = self.data["nodes"].get(child_id)
            if child and child.get("node_type") == "leaf" and child.get("slug") == target_slug:
                return child_id
        return None

    def _find_best_leaf_under_subcategory(
        self,
        subcategory_id: str,
        leaf_name: str,
        embedding: Sequence[float],
        threshold: float,
    ) -> Tuple[Optional[str], float]:
        best_leaf_id = None
        best_score = 0.0
        for child_id in self.data["nodes"][subcategory_id]["child_ids"]:
            child = self.data["nodes"].get(child_id)
            if not child or child.get("node_type") != "leaf":
                continue
            name_score = self._name_similarity(leaf_name, child["name"])
            embedding_score = self._cosine_similarity(embedding, child.get("embedding", []))
            score = max(name_score, embedding_score)
            if score > best_score:
                best_score = score
                best_leaf_id = child_id
        if best_score < threshold:
            return best_leaf_id, best_score
        return best_leaf_id, best_score

    def _best_item_match(self, leaf_id: str, embedding: List[float]) -> Tuple[Optional[str], float]:
        node = self.data["nodes"].get(leaf_id)
        if not node:
            return None, 0.0
        best_item_id = None
        best_score = 0.0
        for item_id in node["item_ids"]:
            score = self._cosine_similarity(embedding, self.data["items"][item_id].get("embedding", []))
            if score > best_score:
                best_score = score
                best_item_id = item_id
        return best_item_id, best_score

    def _best_global_item_match(self, embedding: List[float]) -> Tuple[Optional[str], float]:
        best_item_id = None
        best_score = 0.0
        for item_id, item in self.data["items"].items():
            score = self._cosine_similarity(embedding, item.get("embedding", []))
            if score > best_score:
                best_score = score
                best_item_id = item_id
        return best_item_id, best_score

    def _merge_item(self, target_item_id: str, candidate: Dict[str, Any], similarity: float) -> Dict[str, Any]:
        item = self.data["items"][target_item_id]
        normalized = self._normalize_candidate({**item, **candidate})
        item["category"] = normalized["category"]
        item["subcategory"] = normalized["subcategory"]
        item["leaf_name"] = normalized["leaf_name"]
        item["key_concept"] = item["key_concept"] or normalized["key_concept"]
        if candidate.get("short_description") and candidate["short_description"] not in item["short_description"]:
            item["short_description"] = f"{item['short_description']} {candidate['short_description']}".strip()
        if candidate.get("code_snippet"):
            existing = item.get("code_snippet", "")
            if candidate["code_snippet"] not in existing:
                item["code_snippet"] = "\n".join(part for part in [existing, candidate["code_snippet"]] if part)
        item["utility"] = max(item.get("utility", 0.0), similarity)
        item["performance_gain"] = max(
            self._clamp_score(item.get("performance_gain", 0.5)),
            self._clamp_score(candidate.get("performance_gain", 0.5)),
        )
        item["conflict_count"] = max(int(item.get("conflict_count", 0)), int(candidate.get("conflict_count", 0)))
        item["embedding"] = self._mean_embedding([item.get("embedding", []), candidate.get("embedding", [])])
        return item

    def _append_item_to_leaf(self, candidate: Dict[str, Any], leaf_id: str) -> Dict[str, Any]:
        item = self._build_item_record(candidate)
        item["leaf_node_id"] = leaf_id
        self.data["items"][item["item_id"]] = item
        self.data["nodes"][leaf_id]["item_ids"].append(item["item_id"])
        self._refresh_ancestors(leaf_id)
        return item

    def _route_query(self, query: str, query_embedding: List[float], threshold: float) -> Dict[str, Any]:
        root_id = self.data["root_node_id"]
        root = self.data["nodes"][root_id]
        category_scores: List[Tuple[float, str]] = []
        for category_id in root["child_ids"]:
            category = self.data["nodes"][category_id]
            score = max(
                self._cosine_similarity(query_embedding, category.get("embedding", [])),
                self._category_query_hint(query, category["name"]),
            )
            category_scores.append((score, category_id))
        category_scores.sort(key=lambda pair: pair[0], reverse=True)
        selected_categories = [
            pair for pair in category_scores if pair[0] >= threshold
        ] or category_scores[: max(1, self.config.category_top_k)]
        selected_categories = selected_categories[: max(1, self.config.category_top_k)]

        node_scores = {root_id: 1.0}
        leaf_scores: Dict[str, float] = {}
        leaf_ids: List[str] = []
        paths: List[List[str]] = []

        for category_score, category_id in selected_categories:
            node_scores[category_id] = max(node_scores.get(category_id, 0.0), category_score)
            category = self.data["nodes"][category_id]
            subcategory_scores: List[Tuple[float, str]] = []
            for subcategory_id in category["child_ids"]:
                subcategory = self.data["nodes"][subcategory_id]
                score = max(
                    self._cosine_similarity(query_embedding, subcategory.get("embedding", [])),
                    self._name_query_hint(query, subcategory["name"]),
                )
                subcategory_scores.append((score, subcategory_id))
            subcategory_scores.sort(key=lambda pair: pair[0], reverse=True)
            kept_subcategories = [
                pair for pair in subcategory_scores if pair[0] >= threshold
            ] or subcategory_scores[: max(1, self.config.subcategory_top_k)]
            kept_subcategories = kept_subcategories[: max(1, self.config.subcategory_top_k)]
            for subcategory_score, subcategory_id in kept_subcategories:
                node_scores[subcategory_id] = max(node_scores.get(subcategory_id, 0.0), subcategory_score)
                subcategory = self.data["nodes"][subcategory_id]
                for leaf_id in subcategory["child_ids"]:
                    leaf = self.data["nodes"][leaf_id]
                    score = self._score_leaf(leaf_id, query, query_embedding)
                    if score <= 0.0:
                        continue
                    leaf_scores[leaf_id] = max(leaf_scores.get(leaf_id, 0.0), score)
                    if leaf_id not in leaf_ids:
                        leaf_ids.append(leaf_id)
                    paths.append([root_id, category_id, subcategory_id, leaf_id])
        paths.sort(key=lambda path: leaf_scores.get(path[-1], 0.0), reverse=True)
        return {
            "paths": paths,
            "leaf_ids": sorted(leaf_ids, key=lambda leaf_id: leaf_scores.get(leaf_id, 0.0), reverse=True),
            "node_scores": node_scores,
            "leaf_scores": leaf_scores,
        }

    def _score_leaf(self, leaf_id: str, query: str, query_embedding: List[float]) -> float:
        leaf = self.data["nodes"].get(leaf_id)
        if not leaf:
            return 0.0
        item_scores = [
            self.calculate_combined_score(self.data["items"][item_id], query=query, query_embedding=query_embedding)
            for item_id in leaf["item_ids"]
            if item_id in self.data["items"]
        ]
        if not item_scores:
            return 0.0
        item_scores.sort(reverse=True)
        top_n = item_scores[: max(1, self.config.leaf_score_top_n)]
        return sum(top_n) / len(top_n)

    def _serialize_prompt_item(self, item: Dict[str, Any], score: Optional[float] = None) -> Dict[str, Any]:
        payload = {
            "item_id": item["item_id"],
            "category": item["category"],
            "subcategory": item["subcategory"],
            "leaf_name": item["leaf_name"],
            "key_concept": item["key_concept"],
            "short_description": item["short_description"],
        }
        if score is not None:
            payload["score"] = score
        return payload

    def _render_prompt_item(self, item: Dict[str, Any], score: Optional[float] = None) -> List[str]:
        lines = [
            f"[ID: {item['item_id']}] {item['category']} / {item['subcategory']} / {item['leaf_name']} :: "
            f"{item['key_concept']}: {item['short_description']}"
        ]
        if score is not None:
            lines.append(f"  - Score: {score:.3f}")
        lines.append(
            f"  - Usage Count: {item['usage_count']}, Last Used Iteration: {item['last_used_iter']}, Created Iteration: {item['created_iter']}"
        )
        if item.get("code_snippet"):
            lines.append(f"  - Code Snippet: {item['code_snippet']}")
        return lines

    def _bump_node_usage(self, node_id: Optional[str], current_iter: int):
        while node_id and node_id in self.data["nodes"]:
            node = self.data["nodes"][node_id]
            node["stats"]["access_count"] += 1
            node["stats"]["last_access_iter"] = current_iter
            node_id = node.get("parent_id")

    def _refresh_all_embeddings(self):
        def refresh(node_id: str) -> List[float]:
            node = self.data["nodes"][node_id]
            child_embeddings = [refresh(child_id) for child_id in node["child_ids"] if child_id in self.data["nodes"]]
            item_embeddings = [self.data["items"][item_id].get("embedding", []) for item_id in node["item_ids"] if item_id in self.data["items"]]
            node["embedding"] = self._mean_embedding(child_embeddings + item_embeddings)
            return node["embedding"]

        refresh(self.data["root_node_id"])

    def _refresh_ancestors(self, node_id: Optional[str]):
        while node_id and node_id in self.data["nodes"]:
            node = self.data["nodes"][node_id]
            embeddings = [self.data["items"][item_id].get("embedding", []) for item_id in node["item_ids"] if item_id in self.data["items"]]
            embeddings.extend(
                self.data["nodes"][child_id].get("embedding", [])
                for child_id in node["child_ids"]
                if child_id in self.data["nodes"]
            )
            node["embedding"] = self._mean_embedding(embeddings)
            node_id = node.get("parent_id")

    def _cleanup_dynamic_nodes(self, config: Optional[Dict[str, Any]] = None):
        cfg = {**self.config.to_dict(), **(config or {})}
        self._remove_empty_nodes()
        self._merge_duplicate_subcategories()
        self._merge_redundant_leaves(cfg["merge_threshold"])
        self._remove_empty_nodes()

    def _merge_duplicate_subcategories(self):
        for category_id in self.data["nodes"][self.data["root_node_id"]]["child_ids"]:
            category = self.data["nodes"][category_id]
            seen: Dict[str, str] = {}
            for child_id in list(category["child_ids"]):
                child = self.data["nodes"].get(child_id)
                if not child or child.get("node_type") != "subcategory":
                    continue
                slug = child.get("slug", self._slugify(child["name"]))
                if slug not in seen:
                    seen[slug] = child_id
                    continue
                self._merge_subcategory_nodes(seen[slug], child_id)

    def _merge_subcategory_nodes(self, target_id: str, source_id: str):
        if target_id == source_id or source_id not in self.data["nodes"]:
            return
        target = self.data["nodes"][target_id]
        source = self.data["nodes"][source_id]
        for leaf_id in source["child_ids"]:
            if leaf_id not in target["child_ids"]:
                target["child_ids"].append(leaf_id)
            if leaf_id in self.data["nodes"]:
                self.data["nodes"][leaf_id]["parent_id"] = target_id
        parent_id = source.get("parent_id")
        if parent_id and parent_id in self.data["nodes"]:
            parent = self.data["nodes"][parent_id]
            if source_id in parent["child_ids"]:
                parent["child_ids"].remove(source_id)
        del self.data["nodes"][source_id]

    def _merge_redundant_leaves(self, similarity_threshold: float):
        for node_id, node in list(self.data["nodes"].items()):
            if node.get("node_type") != "subcategory":
                continue
            children = list(node["child_ids"])
            index = 0
            while index < len(children):
                target_id = children[index]
                if target_id not in self.data["nodes"]:
                    index += 1
                    continue
                target = self.data["nodes"][target_id]
                compare_index = index + 1
                while compare_index < len(children):
                    source_id = children[compare_index]
                    source = self.data["nodes"].get(source_id)
                    if not source:
                        compare_index += 1
                        continue
                    if self._should_merge_leaf_nodes(target, source, similarity_threshold):
                        self._merge_leaf_nodes(target_id, source_id)
                        children.pop(compare_index)
                        continue
                    compare_index += 1
                index += 1

    def _should_merge_leaf_nodes(self, lhs: Dict[str, Any], rhs: Dict[str, Any], similarity_threshold: float) -> bool:
        if lhs.get("slug") == rhs.get("slug"):
            return True
        name_score = self._name_similarity(lhs.get("name", ""), rhs.get("name", ""))
        embedding_score = self._cosine_similarity(lhs.get("embedding", []), rhs.get("embedding", []))
        return max(name_score, embedding_score) >= similarity_threshold

    def _merge_leaf_nodes(self, target_id: str, source_id: str):
        if target_id == source_id or source_id not in self.data["nodes"]:
            return
        target = self.data["nodes"][target_id]
        source = self.data["nodes"][source_id]
        for item_id in source["item_ids"]:
            if item_id not in target["item_ids"]:
                target["item_ids"].append(item_id)
            if item_id in self.data["items"]:
                self.data["items"][item_id]["leaf_node_id"] = target_id
        parent_id = source.get("parent_id")
        if parent_id and parent_id in self.data["nodes"]:
            parent = self.data["nodes"][parent_id]
            if source_id in parent["child_ids"]:
                parent["child_ids"].remove(source_id)
        del self.data["nodes"][source_id]

    def _remove_empty_nodes(self):
        root_id = self.data["root_node_id"]
        removed = True
        while removed:
            removed = False
            for node_id, node in list(self.data["nodes"].items()):
                if node_id == root_id or node.get("fixed"):
                    continue
                if node["child_ids"] or node["item_ids"]:
                    continue
                parent_id = node.get("parent_id")
                if parent_id and parent_id in self.data["nodes"]:
                    parent = self.data["nodes"][parent_id]
                    if node_id in parent["child_ids"]:
                        parent["child_ids"].remove(node_id)
                del self.data["nodes"][node_id]
                removed = True

    def _score_item(self, item: Dict[str, Any], query: Optional[str] = None, query_embedding=None) -> Dict[str, float]:
        usage_score = self.calculate_usage_score(item)
        relevance_score = self.calculate_semantic_relevance(item, query_embedding=query_embedding)
        performance_score = self.calculate_performance_gain(item)
        penalty = self.calculate_penalty(item)
        combined_score = (
            self.SCORE_WEIGHTS["usage"] * usage_score
            + self.SCORE_WEIGHTS["relevance"] * relevance_score
            + self.SCORE_WEIGHTS["performance"] * performance_score
            + self.SCORE_WEIGHTS["penalty"] * (1.0 - penalty)
        )
        return {
            "usage": usage_score,
            "relevance": relevance_score,
            "performance": performance_score,
            "penalty": penalty,
            "combined": self._clamp_score(combined_score),
        }

    def _clamp_score(self, value: Any) -> float:
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            return 0.0
        return max(0.0, min(1.0, numeric))

    def calculate_usage_score(self, item: Dict[str, Any]) -> float:
        age = max(1, self.current_iteration - item.get("created_iter", 0))
        heat = item.get("usage_count", 0) / age
        return self._clamp_score(heat)

    def calculate_semantic_relevance(self, item: Dict[str, Any], query_embedding=None) -> float:
        if query_embedding is None:
            return 0.5
        item_embedding = item.get("embedding", [])
        if not item_embedding:
            return 0.5
        similarity = self._cosine_similarity(item_embedding, query_embedding)
        return self._clamp_score((similarity + 1.0) / 2.0)

    def calculate_performance_gain(self, item: Dict[str, Any]) -> float:
        return self._clamp_score(item.get("performance_gain", 0.5))

    def calculate_penalty(self, item: Dict[str, Any]) -> float:
        reference_iter = item.get("last_used_iter", -1)
        if reference_iter < 0:
            reference_iter = item.get("created_iter", 0)
        staleness_penalty = self._clamp_score(max(0, self.current_iteration - reference_iter) / 10.0)
        conflict_penalty = self._clamp_score(item.get("conflict_count", 0) / 3.0)
        penalty = 0.7 * staleness_penalty + 0.3 * conflict_penalty
        return self._clamp_score(penalty)

    def calculate_combined_score(
        self,
        item: Dict[str, Any],
        query: Optional[str] = None,
        query_embedding=None,
    ) -> float:
        if query and query_embedding is None:
            query_embedding = self._embed_texts([query], None)[0]
        return self._score_item(item, query=query, query_embedding=query_embedding)["combined"]

    def _category_query_hint(self, query: str, category_name: str) -> float:
        lowered = query.lower()
        hits = sum(1 for keyword in CATEGORY_HINTS.get(category_name, []) if keyword in lowered)
        return min(1.0, 0.15 * hits)

    def _name_query_hint(self, query: str, node_name: str) -> float:
        query_tokens = set(re.findall(r"[a-z0-9]+", query.lower()))
        name_tokens = set(re.findall(r"[a-z0-9]+", node_name.lower()))
        if not query_tokens or not name_tokens:
            return 0.0
        overlap = len(query_tokens & name_tokens) / len(name_tokens)
        return self._clamp_score(overlap)

    def _name_similarity(self, lhs: str, rhs: str) -> float:
        left = set(re.findall(r"[a-z0-9]+", lhs.lower()))
        right = set(re.findall(r"[a-z0-9]+", rhs.lower()))
        if not left or not right:
            return 0.0
        return len(left & right) / len(left | right)

    def _slugify(self, text: str) -> str:
        normalized = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        return normalized or "node"

    @staticmethod
    def _vector_norm(vector: Sequence[float]) -> float:
        return math.sqrt(sum(value * value for value in vector))

    def _cosine_similarity(self, lhs: Sequence[float], rhs: Sequence[float]) -> float:
        if self._is_empty_embedding(lhs) or self._is_empty_embedding(rhs):
            return 0.0
        limit = min(len(lhs), len(rhs))
        numerator = sum(float(lhs[index]) * float(rhs[index]) for index in range(limit))
        denominator = self._vector_norm(lhs) * self._vector_norm(rhs)
        if denominator == 0.0:
            return 0.0
        return numerator / denominator

    def _mean_embedding(self, embeddings: Iterable[Sequence[float]]) -> List[float]:
        embeddings = [
            self._normalize_embedding(embedding)
            for embedding in embeddings
            if not self._is_empty_embedding(embedding)
        ]
        if not embeddings:
            return []
        dims = max(len(embedding) for embedding in embeddings)
        total = [0.0] * dims
        for embedding in embeddings:
            for index, value in enumerate(embedding):
                total[index] += value
        return [value / len(embeddings) for value in total]

    def _normalize_embedding(self, embedding: Any) -> List[float]:
        if embedding is None:
            return []
        if hasattr(embedding, "tolist"):
            embedding = embedding.tolist()
        if isinstance(embedding, (int, float)):
            return [float(embedding)]
        if isinstance(embedding, tuple):
            embedding = list(embedding)
        if isinstance(embedding, list):
            if embedding and isinstance(embedding[0], (list, tuple)):
                return self._normalize_embedding(embedding[0])
            return [float(value) for value in embedding]
        try:
            return [float(value) for value in embedding]
        except TypeError:
            return []

    def _is_empty_embedding(self, embedding: Any) -> bool:
        return len(self._normalize_embedding(embedding)) == 0

    def _looks_like_single_embedding(self, embedded: Any) -> bool:
        if embedded is None:
            return False
        if hasattr(embedded, "ndim"):
            ndim = getattr(embedded, "ndim", None)
            if ndim == 1:
                return True
            if ndim and ndim > 1:
                return False
        if hasattr(embedded, "tolist"):
            embedded = embedded.tolist()
        if isinstance(embedded, tuple):
            embedded = list(embedded)
        return bool(embedded) and isinstance(embedded, list) and isinstance(embedded[0], (int, float))


CheatsheetManager = TreeCheatsheetManager
