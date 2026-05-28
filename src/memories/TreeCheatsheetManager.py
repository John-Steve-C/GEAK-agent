import json
import math
import re
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple, Union

EmbeddingInput = Union[str, Sequence[str]]
EmbeddingOutput = Union[List[float], List[List[float]]]
Extractor = Optional[Callable[[str], Any]]
Embedder = Optional[Callable[[EmbeddingInput], EmbeddingOutput]]
Clusterer = Optional[Callable[[List[Dict[str, Any]], Dict[str, Any]], List[List[Dict[str, Any]]]]]
Summarizer = Optional[Callable[[List[Dict[str, Any]]], Dict[str, str]]]
Chunker = Optional[Callable[[str, Dict[str, Any]], List[Dict[str, Any]]]]


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

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TreeCheatsheetManager:
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

    def _empty_tree_state(self) -> Dict[str, Any]:
        root_id = self._generate_id()
        return {
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
                    "stats": {
                        "access_count": 0,
                        "last_access_iter": -1,
                        "created_iter": 0,
                    },
                }
            },
            "items": {},
            "metadata": {
                "version": 1,
                "update_rounds": 0,
                "last_retrieval_context": None,
                "config": self.config.to_dict(),
            },
        }

    def _load_state(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if self._is_tree_state(state):
            loaded = {
                "root_node_id": state["root_node_id"],
                "nodes": state.get("nodes", {}),
                "items": state.get("items", {}),
                "metadata": state.get("metadata", {}),
            }
            loaded["metadata"].setdefault("version", 1)
            loaded["metadata"].setdefault("update_rounds", 0)
            loaded["metadata"].setdefault("config", self.config.to_dict())
            self._last_retrieval_context = loaded["metadata"].get("last_retrieval_context")
            return loaded
        return self._import_flat_state(state)

    @staticmethod
    def _is_tree_state(state: Dict[str, Any]) -> bool:
        return isinstance(state, dict) and {"root_node_id", "nodes", "items"}.issubset(state.keys())

    def _import_flat_state(self, state: Dict[str, Any]) -> Dict[str, Any]:
        imported = self._empty_tree_state()
        root_id = imported["root_node_id"]
        root = imported["nodes"][root_id]

        sections = [
            "meta_reasoning",
            "solutions_and_patterns",
            "failed_attempts",
        ]
        for section_name in sections:
            section_items = state.get(section_name, [])
            if not section_items:
                continue
            node_id = self._generate_id()
            imported["nodes"][node_id] = {
                "node_id": node_id,
                "name": section_name.replace("_", " ").title(),
                "description": f"Imported legacy section for {section_name}.",
                "parent_id": root_id,
                "child_ids": [],
                "item_ids": [],
                "embedding": [],
                "depth": 1,
                "stats": {
                    "access_count": 0,
                    "last_access_iter": -1,
                    "created_iter": 0,
                },
            }
            root["child_ids"].append(node_id)
            for old_item in section_items:
                item_id = old_item.get("id", self._generate_id())
                item = self._build_item_record(
                    {
                        "item_id": item_id,
                        "key_concept": old_item.get("content", "")[:80] or section_name,
                        "short_description": old_item.get("content", ""),
                        "code_snippet": "",
                        "source_doc": "legacy_import",
                        "source_chunk_id": section_name,
                        "leaf_node_id": node_id,
                        "embedding": [],
                        "utility": 0.0,
                        "usage_count": old_item.get("usage_count", 0),
                        "last_used_iter": old_item.get("last_used_iter", -1),
                        "created_iter": old_item.get("created_iter", 0),
                    }
                )
                imported["items"][item_id] = item
                imported["nodes"][node_id]["item_ids"].append(item_id)
        self._refresh_all_embeddings()
        return imported

    def _generate_id(self) -> str:
        return str(uuid.uuid4())[:8]

    def _build_item_record(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        item_id = candidate.get("item_id") or self._generate_id()
        return {
            "item_id": item_id,
            "key_concept": candidate.get("key_concept", "").strip(),
            "short_description": candidate.get("short_description", "").strip(),
            "code_snippet": candidate.get("code_snippet", "").strip(),
            "source_doc": candidate.get("source_doc"),
            "source_chunk_id": candidate.get("source_chunk_id"),
            "leaf_node_id": candidate.get("leaf_node_id"),
            "embedding": self._normalize_embedding(candidate.get("embedding")),
            "utility": float(candidate.get("utility", 0.0)),
            "usage_count": int(candidate.get("usage_count", 0)),
            "last_used_iter": int(candidate.get("last_used_iter", -1)),
            "created_iter": int(candidate.get("created_iter", self.current_iteration)),
        }

    def to_json(self) -> str:
        self.data["metadata"]["last_retrieval_context"] = self._last_retrieval_context
        self.data["metadata"]["config"] = self.config.to_dict()
        return json.dumps(self.data, indent=4)

    def get_stats(self) -> str:
        node_count = len(self.data["nodes"])
        item_count = len(self.data["items"])
        leaf_count = sum(1 for node in self.data["nodes"].values() if not node["child_ids"])
        total_length = len(self.to_string_for_prompt())
        return (
            f"Nodes: {node_count} | Leaves: {leaf_count} | Items: {item_count} | "
            f"Updates: {self.data['metadata'].get('update_rounds', 0)} | "
            f"Prompt Length: {total_length} characters"
        )

    def build_bootstrap_extraction_prompt(self, chunk: str, include_code_snippet: bool = False) -> str:
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
      "key_concept": "short concept name",
      "short_description": "2-5 sentences covering the rule, when to use it, key constraints, and why it matters",
      "code_snippet": "optional short code example"
    }
  ]
}
""".strip()
        return f"""
You are a master curator of long-term technical knowledge. Your task is to determine what new or refined insights should be added to an existing cheatsheet based on the context.

For the chunk below, return JSON only as:
{response_schema}

Rules:
- Extract concrete technical rules, not page summaries.
- Prefer mechanism-level concepts over broad topics.
- Make each `short_description` materially informative, not a one-line tag.
- Include enough detail to preserve the practical condition, constraint, or tradeoff from the source chunk.
- Prefer one high-quality item with context over several shallow items.
- Mention parameter ranges, boundary conditions, tensor/layout assumptions, or API requirements when present.
- Keep `key_concept` compact, but let `short_description` carry the substantive content.
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
        return f"""
You are extracting new reusable insights after a successful generation.

Return JSON only as:
{{
  "items": [
    {{
      "key_concept": "short concept name",
      "short_description": "new rule, bug fix, or optimization worth remembering",
      "code_snippet": "optional short code example"
    }}
  ]
}}

Reject generic advice. Only keep task-specific insights that transfer to future tasks.

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
                    chunks.append(
                        {
                            "chunk_id": self._generate_id(),
                            "text": "\n\n".join(current),
                        }
                    )
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

        descriptions = [candidate["short_description"] for candidate in candidates]
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
        cfg = {**self.config.to_dict(), **(config or {})}
        self.data = self._empty_tree_state()
        normalized_items = [self._build_item_record(item) for item in items]
        if not normalized_items:
            return self.data

        missing_embeddings = [
            item["short_description"] for item in normalized_items if self._is_empty_embedding(item["embedding"])
        ]
        generated = self._embed_texts(missing_embeddings, embedder)
        generated_iter = iter(generated)
        for item in normalized_items:
            if self._is_empty_embedding(item["embedding"]):
                item["embedding"] = next(generated_iter, [])

        root_id = self.data["root_node_id"]
        leaf_groups = self._cluster_records(
            normalized_items,
            clusterer=clusterer,
            config=cfg,
            target_group_size=max(1, cfg["leaf_cluster_size"]),
        )

        current_level_node_ids: List[str] = []
        for group in leaf_groups:
            node_id = self._create_node_from_item_group(
                group,
                parent_id=root_id,
                depth=1,
                summarizer=summarizer,
            )
            current_level_node_ids.append(node_id)

        self.data["nodes"][root_id]["child_ids"] = current_level_node_ids
        self._rebuild_branch_levels(
            starting_nodes=current_level_node_ids,
            root_id=root_id,
            clusterer=clusterer,
            summarizer=summarizer,
            config=cfg,
        )
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
        item_scores: Dict[str, float] = {}

        for query, query_embedding in zip(queries, query_embeddings):
            leaf_id, path, path_scores = self._traverse_for_query(query_embedding, threshold)
            matched_paths.append(path)
            if leaf_id not in leaf_node_ids:
                leaf_node_ids.append(leaf_id)
            for node_id, score in path_scores.items():
                node_scores[f"{query}:{node_id}"] = score

        retrieved_items: List[Dict[str, Any]] = []
        seen_item_ids = set()
        scored_items: List[Tuple[float, Dict[str, Any]]] = []
        for leaf_id in leaf_node_ids:
            for item_id in self.data["nodes"][leaf_id]["item_ids"]:
                item = self.data["items"][item_id]
                item_similarity = max(
                    self._cosine_similarity(item.get("embedding", []), query_embedding)
                    for query_embedding in query_embeddings
                )
                item_scores[item_id] = item_similarity
                scored_items.append((item_similarity, item))
        scored_items.sort(key=lambda pair: pair[0], reverse=True)
        for score, item in scored_items[:top_k_items]:
            if item["item_id"] in seen_item_ids:
                continue
            seen_item_ids.add(item["item_id"])
            retrieved_items.append(self._serialize_prompt_item(item, score))

        result = {
            "queries": queries,
            "matched_paths": matched_paths,
            "leaf_node_ids": leaf_node_ids,
            "items": retrieved_items,
            "scores": {
                "nodes": node_scores,
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
        embedding = self._normalize_embedding(item.get("embedding"))
        if self._is_empty_embedding(embedding):
            embedding = self._embed_texts([item.get("short_description", "")], embedder)[0]
        leaf_id, path, path_scores = self._traverse_for_query(embedding, threshold)
        final_score = path_scores.get(leaf_id, 0.0)
        return {
            "leaf_node_id": leaf_id,
            "matched_path": path,
            "score": final_score,
            "embedding": embedding,
        }

    def integrate_reflection(
        self,
        reflection_text: str,
        extractor: Extractor,
        embedder: Embedder,
        summarizer: Summarizer,
        config: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        cfg = {**self.config.to_dict(), **(config or {})}
        candidates = self._extract_candidates_from_chunk(
            reflection_text,
            extractor=extractor,
            source_doc="reflection",
            source_chunk_id=self._generate_id(),
        )
        if not candidates:
            return []

        embeddings = self._embed_texts([candidate["short_description"] for candidate in candidates], embedder)
        for candidate, embedding in zip(candidates, embeddings):
            candidate["embedding"] = embedding

        integrated: List[Dict[str, Any]] = []
        for candidate in candidates:
            route = self.route_item_to_leaf(candidate, embedder, cfg["append_threshold"])
            leaf_id = route["leaf_node_id"]
            candidate["embedding"] = route["embedding"]
            global_item_id, global_similarity = self._best_global_item_match(candidate["embedding"])
            if global_item_id and global_similarity >= cfg["merge_threshold"]:
                updated_item = self._merge_item(global_item_id, candidate, global_similarity)
                integrated.append(
                    {"action": "merge", "item_id": global_item_id, "score": global_similarity, "item": updated_item}
                )
                continue
            target_item_id, similarity = self._best_item_match(leaf_id, candidate["embedding"])
            if target_item_id and similarity >= cfg["merge_threshold"]:
                updated_item = self._merge_item(target_item_id, candidate, similarity)
                integrated.append({"action": "merge", "item_id": target_item_id, "score": similarity, "item": updated_item})
                continue
            if route["score"] < cfg["append_threshold"] and leaf_id != self.data["root_node_id"]:
                leaf_id = self._create_leaf_under_root(candidate, summarizer)
            appended_item = self._append_item_to_leaf(candidate, leaf_id)
            integrated.append({"action": "append", "item_id": appended_item["item_id"], "score": similarity, "item": appended_item})
            if len(self.data["nodes"][leaf_id]["item_ids"]) > cfg["leaf_capacity"]:
                self.split_leaf(leaf_id, summarizer=summarizer, embedder=embedder, clusterer=None, config=cfg)

        self.data["metadata"]["update_rounds"] += 1
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
        cfg = {**self.config.to_dict(), **(config or {})}
        node = self.data["nodes"].get(node_id)
        if not node or node["child_ids"]:
            return []
        item_ids = list(node["item_ids"])
        if len(item_ids) <= cfg["leaf_capacity"]:
            return []

        items = [self.data["items"][item_id] for item_id in item_ids]
        groups = self._cluster_records(
            items,
            clusterer=clusterer,
            config=cfg,
            target_group_size=max(2, math.ceil(len(items) / max(2, cfg["branching_factor"]))),
        )
        if len(groups) <= 1:
            return []

        node["item_ids"] = []
        created_children: List[str] = []
        for group in groups:
            child_id = self._create_node_from_item_group(
                group,
                parent_id=node_id,
                depth=node["depth"] + 1,
                summarizer=summarizer,
            )
            created_children.append(child_id)
        node["child_ids"] = created_children
        node["embedding"] = self._mean_embedding(
            [self.data["nodes"][child_id]["embedding"] for child_id in created_children]
        )
        self._refresh_ancestors(node_id)
        return created_children

    def prune(self, config: Optional[Dict[str, Any]] = None) -> List[str]:
        cfg = {**self.config.to_dict(), **(config or {})}
        removed_item_ids: List[str] = []
        for item_id, item in list(self.data["items"].items()):
            relevance = max(0.0, self._vector_norm(item.get("embedding", [])))
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
                if leaf_id and leaf_id in self.data["nodes"]:
                    if item_id in self.data["nodes"][leaf_id]["item_ids"]:
                        self.data["nodes"][leaf_id]["item_ids"].remove(item_id)
                del self.data["items"][item_id]
                removed_item_ids.append(item_id)
        if removed_item_ids:
            self._remove_empty_nodes()
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
                output.extend(self._render_prompt_item(self.data["items"][item["item_id"]], item.get("score")))
            return "\n".join(output).strip()

        output.append("=== TREE OVERVIEW ===")
        root = self.data["nodes"][self.data["root_node_id"]]
        output.append(f"{root['name']}: {root['description']}")
        leaf_nodes = [node for node in self.data["nodes"].values() if not node["child_ids"]]
        leaf_nodes.sort(
            key=lambda node: (
                node["stats"].get("access_count", 0),
                len(node["item_ids"]),
            ),
            reverse=True,
        )
        if top_k_hot != -1:
            leaf_nodes = leaf_nodes[:top_k_hot]
        for node in leaf_nodes:
            output.append("")
            output.append(f"[Leaf {node['node_id']}] {node['name']}: {node['description']}")
            items = [self.data["items"][item_id] for item_id in node["item_ids"]]
            items.sort(key=lambda item: item.get("usage_count", 0), reverse=True)
            if top_k_hot != -1:
                items = items[:top_k_hot]
            for item in items:
                output.extend(self._render_prompt_item(item))
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
                    "key_concept": op.get("section", "insight").replace("_", " "),
                    "short_description": op.get("content", ""),
                    "code_snippet": "",
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
                    self.data["items"][target_id]["short_description"] = op.get("content", "")
            elif op_type in {"VARIATION", "EXPAND"}:
                target_id = op.get("target_id")
                if target_id in self.data["items"]:
                    extra = op.get("content", "")
                    snippet = self.data["items"][target_id].get("code_snippet", "")
                    self.data["items"][target_id]["code_snippet"] = "\n".join(
                        part for part in [snippet, extra] if part
                    )
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
            normalized.append(
                {
                    "key_concept": candidate.get("key_concept", "").strip(),
                    "short_description": candidate.get("short_description", "").strip(),
                    "code_snippet": candidate.get("code_snippet", "").strip(),
                    "source_doc": candidate.get("source_doc", source_doc),
                    "source_chunk_id": candidate.get("source_chunk_id", source_chunk_id),
                }
            )
        return [candidate for candidate in normalized if candidate["short_description"]]

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
        return {
            "key_concept": first_line or "Document chunk",
            "short_description": cleaned[: self.config.max_chunk_chars],
            "code_snippet": "",
        }

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

    def _cluster_records(
        self,
        records: Sequence[Dict[str, Any]],
        clusterer: Clusterer,
        config: Dict[str, Any],
        target_group_size: int,
    ) -> List[List[Dict[str, Any]]]:
        if not records:
            return []
        if clusterer:
            groups = clusterer(list(records), config)
            if groups:
                return groups
        ordered = sorted(
            records,
            key=lambda record: record.get("key_concept", "") or record.get("name", ""),
        )
        size = max(1, target_group_size)
        return [ordered[index : index + size] for index in range(0, len(ordered), size)]

    def _create_node_from_item_group(
        self,
        items: Sequence[Dict[str, Any]],
        parent_id: str,
        depth: int,
        summarizer: Summarizer,
    ) -> str:
        node_id = self._generate_id()
        summary = self._summarize_group(items, summarizer)
        self.data["nodes"][node_id] = {
            "node_id": node_id,
            "name": summary["name"],
            "description": summary["description"],
            "parent_id": parent_id,
            "child_ids": [],
            "item_ids": [],
            "embedding": [],
            "depth": depth,
            "stats": {
                "access_count": 0,
                "last_access_iter": -1,
                "created_iter": self.current_iteration,
            },
        }
        for item in items:
            item["leaf_node_id"] = node_id
            self.data["items"][item["item_id"]] = item
            self.data["nodes"][node_id]["item_ids"].append(item["item_id"])
        self.data["nodes"][node_id]["embedding"] = self._mean_embedding(
            [item.get("embedding", []) for item in items]
        )
        return node_id

    def _summarize_group(
        self,
        items: Sequence[Dict[str, Any]],
        summarizer: Summarizer,
    ) -> Dict[str, str]:
        if summarizer:
            summary = summarizer(list(items))
            if summary and summary.get("name") and summary.get("description"):
                return {
                    "name": summary["name"],
                    "description": summary["description"],
                }
        concepts = [item.get("key_concept", "").strip() for item in items if item.get("key_concept")]
        descriptions = [item.get("short_description", "").strip() for item in items if item.get("short_description")]
        name = ", ".join(concepts[:2]) or "Cheatsheet Group"
        description = " / ".join(descriptions[:2])[:240] or "Grouped technical cheatsheet items."
        return {"name": name, "description": description}

    def _rebuild_branch_levels(
        self,
        starting_nodes: List[str],
        root_id: str,
        clusterer: Clusterer,
        summarizer: Summarizer,
        config: Dict[str, Any],
    ):
        current_nodes = list(starting_nodes)
        current_depth = 1
        while len(current_nodes) > config["branching_factor"] and current_depth < config["max_depth"]:
            parent = self.data["nodes"][root_id]
            for node_id in current_nodes:
                self.data["nodes"][node_id]["parent_id"] = None
            node_records = [
                {
                    "item_id": node_id,
                    "key_concept": self.data["nodes"][node_id]["name"],
                    "short_description": self.data["nodes"][node_id]["description"],
                    "embedding": self.data["nodes"][node_id]["embedding"],
                    "child_node_id": node_id,
                }
                for node_id in current_nodes
            ]
            grouped = self._cluster_records(
                node_records,
                clusterer=clusterer,
                config=config,
                target_group_size=max(2, config["branching_factor"]),
            )
            new_parent_ids: List[str] = []
            for group in grouped:
                parent_id = self._generate_id()
                summary = self._summarize_group(group, summarizer)
                self.data["nodes"][parent_id] = {
                    "node_id": parent_id,
                    "name": summary["name"],
                    "description": summary["description"],
                    "parent_id": root_id,
                    "child_ids": [record["child_node_id"] for record in group],
                    "item_ids": [],
                    "embedding": self._mean_embedding([record.get("embedding", []) for record in group]),
                    "depth": current_depth,
                    "stats": {
                        "access_count": 0,
                        "last_access_iter": -1,
                        "created_iter": self.current_iteration,
                    },
                }
                for record in group:
                    self.data["nodes"][record["child_node_id"]]["parent_id"] = parent_id
                new_parent_ids.append(parent_id)
            current_nodes = new_parent_ids
            current_depth += 1
            parent["child_ids"] = current_nodes

    def _traverse_for_query(
        self,
        query_embedding: List[float],
        threshold: float,
    ) -> Tuple[str, List[str], Dict[str, float]]:
        current_id = self.data["root_node_id"]
        path = [current_id]
        path_scores = {current_id: 1.0}
        while True:
            node = self.data["nodes"][current_id]
            if not node["child_ids"]:
                return current_id, path, path_scores
            scored_children = []
            for child_id in node["child_ids"]:
                child = self.data["nodes"][child_id]
                score = self._cosine_similarity(query_embedding, child.get("embedding", []))
                scored_children.append((score, child_id))
            scored_children.sort(key=lambda pair: pair[0], reverse=True)
            best_score, best_child = scored_children[0]
            if best_score < threshold:
                return current_id, path, path_scores
            current_id = best_child
            path.append(current_id)
            path_scores[current_id] = best_score

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
        if candidate.get("short_description") and candidate["short_description"] not in item["short_description"]:
            item["short_description"] = f"{item['short_description']} {candidate['short_description']}".strip()
        if candidate.get("code_snippet"):
            existing = item.get("code_snippet", "")
            if candidate["code_snippet"] not in existing:
                item["code_snippet"] = "\n".join(part for part in [existing, candidate["code_snippet"]] if part)
        item["utility"] = max(item.get("utility", 0.0), similarity)
        item["embedding"] = self._mean_embedding([item.get("embedding", []), candidate.get("embedding", [])])
        return item

    def _append_item_to_leaf(self, candidate: Dict[str, Any], leaf_id: str) -> Dict[str, Any]:
        item = self._build_item_record(candidate)
        item["leaf_node_id"] = leaf_id
        self.data["items"][item["item_id"]] = item
        self.data["nodes"][leaf_id]["item_ids"].append(item["item_id"])
        self._refresh_ancestors(leaf_id)
        return item

    def _create_leaf_under_root(self, candidate: Dict[str, Any], summarizer: Summarizer) -> str:
        root_id = self.data["root_node_id"]
        summary = self._summarize_group([candidate], summarizer)
        node_id = self._generate_id()
        self.data["nodes"][node_id] = {
            "node_id": node_id,
            "name": summary["name"],
            "description": summary["description"],
            "parent_id": root_id,
            "child_ids": [],
            "item_ids": [],
            "embedding": list(candidate.get("embedding", []) or []),
            "depth": 1,
            "stats": {
                "access_count": 0,
                "last_access_iter": -1,
                "created_iter": self.current_iteration,
            },
        }
        self.data["nodes"][root_id]["child_ids"].append(node_id)
        return node_id

    def _serialize_prompt_item(self, item: Dict[str, Any], score: Optional[float] = None) -> Dict[str, Any]:
        payload = {
            "item_id": item["item_id"],
            "key_concept": item["key_concept"],
            "short_description": item["short_description"],
        }
        if score is not None:
            payload["score"] = score
        return payload

    def _render_prompt_item(self, item: Dict[str, Any], score: Optional[float] = None) -> List[str]:
        lines = [f"[ID: {item['item_id']}] {item['key_concept']}: {item['short_description']}"]
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
            child_embeddings = [refresh(child_id) for child_id in node["child_ids"]]
            item_embeddings = [self.data["items"][item_id].get("embedding", []) for item_id in node["item_ids"]]
            node["embedding"] = self._mean_embedding(child_embeddings + item_embeddings)
            return node["embedding"]

        refresh(self.data["root_node_id"])

    def _refresh_ancestors(self, node_id: Optional[str]):
        while node_id and node_id in self.data["nodes"]:
            node = self.data["nodes"][node_id]
            embeddings = [self.data["items"][item_id].get("embedding", []) for item_id in node["item_ids"]]
            embeddings.extend(self.data["nodes"][child_id].get("embedding", []) for child_id in node["child_ids"])
            node["embedding"] = self._mean_embedding(embeddings)
            node_id = node.get("parent_id")

    def _remove_empty_nodes(self):
        root_id = self.data["root_node_id"]
        removed = True
        while removed:
            removed = False
            for node_id, node in list(self.data["nodes"].items()):
                if node_id == root_id:
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

    @staticmethod
    def _vector_norm(vector: Sequence[float]) -> float:
        return math.sqrt(sum(value * value for value in vector))

    def _cosine_similarity(self, lhs: Sequence[float], rhs: Sequence[float]) -> float:
        if self._is_empty_embedding(lhs) or self._is_empty_embedding(rhs):
            return 0.0
        limit = min(len(lhs), len(rhs))
        numerator = sum(lhs[index] * rhs[index] for index in range(limit))
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
