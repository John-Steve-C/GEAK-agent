import copy
import json
import re
import uuid
from typing import Any, Dict, List, Optional, Tuple

from memories.CheatsheetManager import CheatsheetManager


class TreeCheatsheetManager(CheatsheetManager):
    ROOT_NODE_ID = "root"
    LEGACY_SECTIONS = [
        "meta_reasoning",
        "solutions_and_patterns",
        "failed_attempts",
    ]
    FIXED_CATEGORIES = [
        "Kernel Pattern",
        "Correctness Rule",
        "Performance Rule",
        "Debugging Rule",
    ]
    CATEGORY_NODE_IDS = {
        "Kernel Pattern": "category_kernel_pattern",
        "Correctness Rule": "category_correctness_rule",
        "Performance Rule": "category_performance_rule",
        "Debugging Rule": "category_debugging_rule",
    }
    CATEGORY_DESCRIPTIONS = {
        "Kernel Pattern": "Kernel implementation patterns for elementwise, reduction, softmax, matmul, attention, normalization, and quantization.",
        "Correctness Rule": "Correctness rules for masking, indexing, boundaries, layout, strides, and numerical stability.",
        "Performance Rule": "Performance rules for memory coalescing, block size, reuse, vectorization, autotuning, mapping, and latency.",
        "Debugging Rule": "Debugging rules for compile errors, runtime errors, wrong answers, timeouts, and OOM failures.",
    }
    DEFAULT_INTERNAL_NAMES = {
        "Kernel Pattern": "General Kernel Pattern",
        "Correctness Rule": "General Correctness Rule",
        "Performance Rule": "General Performance Rule",
        "Debugging Rule": "General Debugging Rule",
    }
    CATEGORY_KEYWORDS = {
        "Kernel Pattern": [
            "kernel",
            "softmax",
            "reduction",
            "reduce",
            "layernorm",
            "rmsnorm",
            "matmul",
            "attention",
            "quantization",
            "dequantization",
            "elementwise",
            "epilogue",
        ],
        "Correctness Rule": [
            "correctness",
            "mask",
            "masking",
            "index",
            "indexing",
            "boundary",
            "stride",
            "layout",
            "stable",
            "stability",
            "fp32",
            "precision",
            "overflow",
            "underflow",
            "nan",
        ],
        "Performance Rule": [
            "performance",
            "throughput",
            "latency",
            "coalescing",
            "coalesce",
            "block size",
            "program id",
            "reuse",
            "cache",
            "vectorization",
            "vectorize",
            "autotuning",
            "autotune",
            "occupancy",
            "memory",
            "tile",
        ],
        "Debugging Rule": [
            "debug",
            "compile",
            "compiler",
            "runtime",
            "wrong answer",
            "assert",
            "error",
            "traceback",
            "timeout",
            "oom",
            "hang",
            "failure",
            "failed",
        ],
    }
    TOPIC_KEYWORDS = {
        "Kernel Pattern": {
            "Elementwise": ["elementwise", "pointwise", "broadcast"],
            "Reduction": ["reduction", "reduce", "sum", "scan"],
            "Softmax": ["softmax", "logsumexp"],
            "LayerNorm / RMSNorm": ["layernorm", "rmsnorm", "normalization"],
            "Matmul": ["matmul", "gemm", "matrix multiply"],
            "Attention": ["attention", "qk", "kv", "flash attention"],
            "Quantization / Dequantization": ["quantization", "dequantization", "quantize", "dequantize", "int8", "fp8"],
        },
        "Correctness Rule": {
            "Masking": ["mask", "masked", "causal"],
            "Indexing": ["index", "indexing", "gather", "scatter"],
            "Boundary Handling": ["boundary", "ragged", "tail", "out of bounds", "oob"],
            "Strides / Layout": ["stride", "layout", "contiguous", "non-contiguous"],
            "Numerical Stability": ["stable", "stability", "fp32", "precision", "overflow", "underflow", "nan"],
        },
        "Performance Rule": {
            "Memory Coalescing": ["coalescing", "coalesce", "global memory", "contiguous"],
            "Block Size": ["block size", "num_warps", "num_stages", "tile size"],
            "Program ID Mapping": ["program id", "pid", "mapping", "launch order"],
            "Cache / Reuse": ["cache", "reuse", "shared", "locality"],
            "Vectorization": ["vectorization", "vectorize", "unroll"],
            "Autotuning": ["autotuning", "autotune", "config search"],
        },
        "Debugging Rule": {
            "Compile Error": ["compile", "compiler", "syntax", "type error"],
            "Runtime Error": ["runtime", "illegal memory", "segfault", "exception", "crash"],
            "Wrong Answer": ["wrong answer", "incorrect", "mismatch", "accuracy"],
            "Timeout": ["timeout", "hang", "stall"],
            "OOM": ["oom", "out of memory", "memory exhausted"],
        },
    }
    DEFAULT_LEAF_CAPACITY = 4

    def __init__(
        self,
        initial_state: Optional[Dict] = None,
        use_fixed_categories: bool = True,
        embedder=None,
    ):
        self.sections = list(self.LEGACY_SECTIONS)
        self.current_iteration = 0
        self.leaf_capacity = self.DEFAULT_LEAF_CAPACITY
        self._category_embedding_cache: Dict[str, List[float]] = {}
        self.use_fixed_categories = use_fixed_categories
        self.embedder = embedder

        if initial_state:
            raw_state = copy.deepcopy(initial_state)
            if self._is_tree_state(raw_state):
                self.data = raw_state
            else:
                self.data = self._create_empty_tree()
                self._import_legacy_state(raw_state)
        else:
            self.data = self._create_empty_tree()

        self._normalize_data()

    def _generate_id(self) -> str:
        return str(uuid.uuid4())[:8]

    def _generate_node_id(self) -> str:
        return f"node_{uuid.uuid4().hex[:8]}"

    def _create_empty_tree(self) -> Dict[str, Any]:
        data = {
            "root_node_id": self.ROOT_NODE_ID,
            "nodes": {},
            "items": {},
            "metadata": {
                "current_iteration": 0,
                "last_retrieval_context": None,
                "use_fixed_categories": self.use_fixed_categories,
            },
        }
        data["nodes"][self.ROOT_NODE_ID] = {
            "id": self.ROOT_NODE_ID,
            "name": "Root",
            "node_type": "root",
            "parent_id": None,
            "child_ids": [],
            "item_ids": [],
            "path": ["Root"],
            "stats": {"access_count": 0},
        }
        if self.use_fixed_categories:
            for category in self.FIXED_CATEGORIES:
                node_id = self.CATEGORY_NODE_IDS[category]
                data["nodes"][node_id] = {
                    "id": node_id,
                    "name": category,
                    "node_type": "category",
                    "parent_id": self.ROOT_NODE_ID,
                    "child_ids": [],
                    "item_ids": [],
                    "path": ["Root", category],
                    "stats": {"access_count": 0},
                }
                data["nodes"][self.ROOT_NODE_ID]["child_ids"].append(node_id)
        return data

    def _is_tree_state(self, state: Dict[str, Any]) -> bool:
        return isinstance(state, dict) and "root_node_id" in state and "nodes" in state and "items" in state

    def _normalize_data(self):
        if not self._is_tree_state(self.data):
            legacy_state = copy.deepcopy(self.data)
            self.data = self._create_empty_tree()
            self._import_legacy_state(legacy_state)

        self.data.setdefault("nodes", {})
        self.data.setdefault("items", {})
        self.data.setdefault("metadata", {})
        self.data["metadata"].setdefault("current_iteration", 0)
        self.data["metadata"].setdefault("last_retrieval_context", None)
        self.data["metadata"]["use_fixed_categories"] = self.use_fixed_categories
        self.current_iteration = self.data["metadata"].get("current_iteration", 0)

        canonical_tree = self._create_empty_tree()
        for required_node_id, required_node in canonical_tree["nodes"].items():
            if required_node_id not in self.data["nodes"]:
                self.data["nodes"][required_node_id] = required_node

        for node_id, node in list(self.data["nodes"].items()):
            node.setdefault("id", node_id)
            node.setdefault("name", node_id)
            node.setdefault("node_type", "internal")
            node.setdefault("parent_id", None)
            node.setdefault("child_ids", [])
            node.setdefault("item_ids", [])
            node.setdefault("path", [])
            node.setdefault("stats", {})
            node["stats"].setdefault("access_count", 0)
            node["child_ids"] = [child_id for child_id in node.get("child_ids", []) if child_id in self.data["nodes"]]
            node["item_ids"] = []

        self.data["root_node_id"] = self.ROOT_NODE_ID
        root_node = self.data["nodes"][self.ROOT_NODE_ID]
        if self.use_fixed_categories:
            root_node["child_ids"] = [self.CATEGORY_NODE_IDS[category] for category in self.FIXED_CATEGORIES]

            for category in self.FIXED_CATEGORIES:
                node_id = self.CATEGORY_NODE_IDS[category]
                category_node = self.data["nodes"][node_id]
                category_node["name"] = category
                category_node["node_type"] = "category"
                category_node["parent_id"] = self.ROOT_NODE_ID

        for node in self.data["nodes"].values():
            parent_id = node.get("parent_id")
            if parent_id and parent_id in self.data["nodes"]:
                parent = self.data["nodes"][parent_id]
                if node["id"] not in parent["child_ids"]:
                    parent["child_ids"].append(node["id"])

        items_needing_route: List[Dict[str, Any]] = []
        for item_id, item in list(self.data["items"].items()):
            item.setdefault("id", item_id)
            self._normalize_item(item)
            leaf_node_id = item.get("leaf_node_id")
            if leaf_node_id in self.data["nodes"] and self.data["nodes"][leaf_node_id]["node_type"] == "leaf":
                self.data["nodes"][leaf_node_id]["item_ids"].append(item["id"])
            else:
                items_needing_route.append(item)

        for item in items_needing_route:
            self._place_item(item, preserve_existing_leaf=False)

        self._cleanup_redundant_nodes()
        self._refresh_paths()

    def _normalize_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        super()._normalize_item(item)
        item.setdefault("content", "")
        item.setdefault("code_snippet", "")
        item.setdefault("leaf_node_id", None)
        item.setdefault("legacy_section", "")
        item.setdefault("category", "")
        item.setdefault("subcategory", "")
        item.setdefault("leaf_name", "")
        return item

    def _item_text_for_embedding(self, item: Dict[str, Any]) -> str:
        parts = [item.get("content", ""), item.get("code_snippet", "")]
        for variation in item.get("variations", []):
            parts.append(variation.get("content", ""))
        for edge_case in item.get("edge_cases", []):
            parts.append(edge_case.get("content", ""))
        return "\n".join(part for part in parts if part).strip()

    def to_json(self) -> str:
        self.data.setdefault("metadata", {})
        self.data["metadata"]["current_iteration"] = self.current_iteration
        self.data["metadata"]["use_fixed_categories"] = self.use_fixed_categories
        return json.dumps(self.data, indent=4)

    def _import_legacy_state(self, state: Dict[str, Any]):
        for section in self.sections:
            for raw_item in state.get(section, []) or []:
                item = copy.deepcopy(raw_item)
                item.setdefault("id", self._generate_id())
                while item["id"] in self.data["items"]:
                    item["id"] = self._generate_id()
                item["legacy_section"] = section
                self._normalize_item(item)
                self.data["items"][item["id"]] = item
                self._place_item(item, preserve_existing_leaf=False)

    def _safe_get_embedding(self, text: str, is_query: bool = False):
        if not text:
            return []
        try:
            return self._get_query_embedding(text) if is_query else self._get_embedding(text)
        except Exception:
            return []

    def _keyword_score(self, text: str, keywords: List[str]) -> int:
        lowered = text.lower()
        score = 0
        for keyword in keywords:
            score += lowered.count(keyword.lower())
        return score

    def _infer_category(self, content: str, section_hint: str = "") -> str:
        if not content:
            content = ""
        scores = {category: self._keyword_score(content, keywords) for category, keywords in self.CATEGORY_KEYWORDS.items()}

        if section_hint == "failed_attempts":
            scores["Debugging Rule"] += 2
        elif section_hint == "meta_reasoning":
            scores["Correctness Rule"] += 1
        elif section_hint == "solutions_and_patterns":
            scores["Kernel Pattern"] += 1
            scores["Performance Rule"] += 1

        best_category = max(scores, key=scores.get)
        if scores[best_category] > 0:
            return best_category

        item_embedding = self._safe_get_embedding(content)
        if item_embedding:
            best_score = -1.0
            for category, description in self.CATEGORY_DESCRIPTIONS.items():
                category_embedding = self._category_embedding_cache.get(category)
                if category_embedding is None:
                    category_embedding = self._safe_get_embedding(description)
                    self._category_embedding_cache[category] = category_embedding
                similarity = self._cosine_similarity(item_embedding, category_embedding)
                if similarity > best_score:
                    best_category = category
                    best_score = similarity
            return best_category

        return "Kernel Pattern"

    def _infer_internal_name(self, content: str, category: str, subcategory_hint: str = "") -> str:
        if subcategory_hint:
            return self._clean_label(subcategory_hint, self.DEFAULT_INTERNAL_NAMES[category])

        topics = self.TOPIC_KEYWORDS.get(category, {})
        best_name = self.DEFAULT_INTERNAL_NAMES[category]
        best_score = 0
        for topic_name, keywords in topics.items():
            score = self._keyword_score(content, keywords)
            if score > best_score:
                best_name = topic_name
                best_score = score
        return best_name

    def _clean_label(self, label: str, fallback: str) -> str:
        cleaned = re.sub(r"\s+", " ", (label or "").strip(" -:")).strip()
        return cleaned[:80] if cleaned else fallback

    def _derive_leaf_name(self, content: str, fallback: str) -> str:
        compact = re.sub(r"\s+", " ", content or "").strip()
        if not compact:
            return fallback
        compact = re.sub(r"^[A-Za-z]+(?:\s+[A-Za-z]+){0,2}\s+(?:to|for|with)\s+", "", compact, count=1)
        compact = re.split(r"[.;\n]", compact, maxsplit=1)[0]
        words = re.findall(r"[A-Za-z0-9+/.-]+", compact)
        if not words:
            return fallback
        leaf_name = " ".join(words[:5]).strip()
        leaf_name = leaf_name.title()
        return leaf_name[:80] if leaf_name else fallback

    def _find_child_by_name(self, parent_id: str, name: str, node_type: Optional[str] = None) -> Optional[str]:
        parent = self.data["nodes"].get(parent_id)
        if not parent:
            return None
        for child_id in parent.get("child_ids", []):
            child = self.data["nodes"].get(child_id)
            if not child:
                continue
            if child.get("name") == name and (node_type is None or child.get("node_type") == node_type):
                return child_id
        return None

    def _create_node(self, parent_id: str, name: str, node_type: str) -> str:
        node_id = self._generate_node_id()
        parent = self.data["nodes"][parent_id]
        parent_path = parent.get("path", ["Root"])
        self.data["nodes"][node_id] = {
            "id": node_id,
            "name": name,
            "node_type": node_type,
            "parent_id": parent_id,
            "child_ids": [],
            "item_ids": [],
            "path": list(parent_path) + [name],
            "stats": {"access_count": 0},
        }
        parent["child_ids"].append(node_id)
        return node_id

    def _ensure_category_node(self, category: str) -> str:
        if self.use_fixed_categories:
            return self.CATEGORY_NODE_IDS[category]

        existing_child = self._find_child_by_name(self.ROOT_NODE_ID, category, node_type="category")
        if existing_child:
            return existing_child
        return self._create_node(self.ROOT_NODE_ID, category, "category")

    def _ensure_internal_node(self, category: str, internal_name: str) -> str:
        category_node_id = self._ensure_category_node(category)
        existing_child = self._find_child_by_name(category_node_id, internal_name, node_type="internal")
        if existing_child:
            return existing_child
        return self._create_node(category_node_id, internal_name, "internal")

    def _ensure_leaf_node(self, parent_id: str, leaf_name: str) -> str:
        parent = self.data["nodes"][parent_id]
        for child_id in parent.get("child_ids", []):
            child = self.data["nodes"][child_id]
            if child["node_type"] == "leaf" and child["name"] == leaf_name and len(child["item_ids"]) < self.leaf_capacity:
                return child_id

        existing_names = {self.data["nodes"][child_id]["name"] for child_id in parent.get("child_ids", [])}
        final_name = leaf_name
        suffix = 2
        while final_name in existing_names:
            final_name = f"{leaf_name} ({suffix})"
            suffix += 1
        return self._create_node(parent_id, final_name, "leaf")

    def _remove_item_from_leaf(self, item: Dict[str, Any]):
        leaf_node_id = item.get("leaf_node_id")
        if not leaf_node_id:
            return
        leaf_node = self.data["nodes"].get(leaf_node_id)
        if not leaf_node:
            item["leaf_node_id"] = None
            return
        if item["id"] in leaf_node.get("item_ids", []):
            leaf_node["item_ids"].remove(item["id"])
        item["leaf_node_id"] = None

    def _place_item(
        self,
        item: Dict[str, Any],
        category_hint: str = "",
        subcategory_hint: str = "",
        leaf_hint: str = "",
        preserve_existing_leaf: bool = False,
    ) -> str:
        self._normalize_item(item)
        section_hint = item.get("legacy_section", "")

        if self.use_fixed_categories:
            category = category_hint or item.get("category", "")
            if category not in self.FIXED_CATEGORIES:
                category = self._infer_category(item.get("content", ""), section_hint=section_hint)

            internal_name = self._infer_internal_name(
                item.get("content", ""),
                category,
                subcategory_hint or item.get("subcategory", ""),
            )
            leaf_name = self._clean_label(
                leaf_hint or item.get("leaf_name", ""),
                fallback="",
            )
            if not leaf_name:
                default_leaf_fallback = internal_name if internal_name != self.DEFAULT_INTERNAL_NAMES[category] else "General Rule"
                leaf_name = self._derive_leaf_name(item.get("content", ""), default_leaf_fallback)
        else:
            category = self._clean_label(category_hint or item.get("category", ""), fallback="Uncategorized")
            internal_name = self._clean_label(subcategory_hint or item.get("subcategory", ""), fallback="General")
            leaf_name = self._clean_label(
                leaf_hint or item.get("leaf_name", ""),
                fallback="",
            )
            if not leaf_name:
                leaf_name = self._derive_leaf_name(item.get("content", ""), "General Rule")

        if not preserve_existing_leaf:
            self._remove_item_from_leaf(item)

        internal_node_id = self._ensure_internal_node(category, internal_name)
        leaf_node_id = self._ensure_leaf_node(internal_node_id, leaf_name)
        leaf_node = self.data["nodes"][leaf_node_id]
        if item["id"] not in leaf_node["item_ids"]:
            leaf_node["item_ids"].append(item["id"])

        item["leaf_node_id"] = leaf_node_id
        item["category"] = category
        item["subcategory"] = internal_name
        item["leaf_name"] = leaf_node["name"]
        return leaf_node_id

    def _refresh_paths(self):
        def visit(node_id: str, parent_path: List[str]):
            node = self.data["nodes"][node_id]
            node["path"] = list(parent_path) + [node["name"]]
            for child_id in node.get("child_ids", []):
                if child_id in self.data["nodes"]:
                    visit(child_id, node["path"])

        visit(self.ROOT_NODE_ID, [])

    def _delete_node(self, node_id: str):
        node = self.data["nodes"].get(node_id)
        if not node:
            return
        parent_id = node.get("parent_id")
        if parent_id and parent_id in self.data["nodes"]:
            parent = self.data["nodes"][parent_id]
            if node_id in parent.get("child_ids", []):
                parent["child_ids"].remove(node_id)
        del self.data["nodes"][node_id]

    def _cleanup_redundant_nodes(self):
        preserved_node_ids = {self.ROOT_NODE_ID}
        if self.use_fixed_categories:
            preserved_node_ids.update(self.CATEGORY_NODE_IDS.values())

        changed = True
        while changed:
            changed = False
            for node_id, node in list(self.data["nodes"].items()):
                if node_id in preserved_node_ids:
                    continue
                if node["node_type"] == "leaf" and not node.get("item_ids"):
                    self._delete_node(node_id)
                    changed = True
                    break
                if node["node_type"] in {"category", "internal"}:
                    if not node.get("child_ids"):
                        self._delete_node(node_id)
                        changed = True
                        break
                    if node["node_type"] == "category" or not self.use_fixed_categories:
                        continue
                    if len(node["child_ids"]) == 1:
                        only_child_id = node["child_ids"][0]
                        only_child = self.data["nodes"].get(only_child_id)
                        parent = self.data["nodes"].get(node.get("parent_id"))
                        if not only_child or not parent:
                            continue
                        default_name = self.DEFAULT_INTERNAL_NAMES.get(parent["name"], "")
                        if node["name"] == default_name or node["name"] == only_child["name"]:
                            parent["child_ids"] = [
                                only_child_id if child_id == node_id else child_id
                                for child_id in parent["child_ids"]
                            ]
                            only_child["parent_id"] = parent["id"]
                            self._delete_node(node_id)
                            changed = True
                            break
        self._refresh_paths()

    def _iter_leaf_ids(self) -> List[str]:
        return [
            node_id
            for node_id, node in self.data["nodes"].items()
            if node.get("node_type") == "leaf"
        ]

    def _node_path_text(self, node_id: str) -> str:
        node = self.data["nodes"].get(node_id)
        if not node:
            return ""
        return " > ".join(node.get("path", []))

    def _render_item_lines(self, item: Dict[str, Any], include_stats: bool = False) -> List[str]:
        lines = [f"[ID: {item['id']}] {item.get('content', '')}"]
        if include_stats:
            lines.append(
                "  - Usage Count: {usage}, Last Used Iteration: {last}, Created Iteration: {created}".format(
                    usage=item.get("usage_count", 0),
                    last=item.get("last_used_iter", -1),
                    created=item.get("created_iter", 0),
                )
            )
        if item.get("code_snippet"):
            lines.append(f"  - Code Snippet: {item['code_snippet']}")
        for variation in item.get("variations", []):
            lines.append(f"  - Variation ({variation.get('name', 'variant')}): {variation.get('content', '')}")
        for edge_case in item.get("edge_cases", []):
            lines.append(f"  - Note: {edge_case.get('content', '')}")
        for relation in item.get("relations", []):
            justification = relation.get("justification", "").strip()
            relation_line = f"  - Relation ({relation.get('type', 'UNKNOWN')} -> {relation.get('target_id', 'UNKNOWN')})"
            if justification:
                relation_line += f": {justification}"
            lines.append(relation_line)
        return lines

    def _render_full_tree(self) -> str:
        output = ["=== TREE CHEATSHEET ==="]

        def render(node_id: str, depth: int):
            node = self.data["nodes"][node_id]
            if node["node_type"] != "root":
                indent = "  " * depth
                suffix = f" ({len(node.get('item_ids', []))} items)" if node["node_type"] == "leaf" else ""
                output.append(f"{indent}- {node['name']}{suffix}")
            for child_id in node.get("child_ids", []):
                render(child_id, depth + 1)
            if node["node_type"] == "leaf":
                indent = "  " * (depth + 1)
                for item_id in node.get("item_ids", []):
                    item = self.data["items"].get(item_id)
                    if not item:
                        continue
                    item_lines = self._render_item_lines(item, include_stats=True)
                    output.append(f"{indent}{item_lines[0]}")
                    for line in item_lines[1:]:
                        output.append(f"{indent}{line}")

        render(self.ROOT_NODE_ID, 0)
        return "\n".join(output)

    def _retrieve_items(self, top_k_hot: int, query: Optional[str]) -> Dict[str, Any]:
        query_embedding = self._safe_get_embedding(query, is_query=True) if query else None
        leaf_scores: List[Tuple[str, float]] = []
        for leaf_id in self._iter_leaf_ids():
            leaf = self.data["nodes"][leaf_id]
            if not leaf.get("item_ids"):
                continue
            scored_items = [
                self.calculate_combined_score(self.data["items"][item_id], query=query, query_embedding=query_embedding)
                for item_id in leaf["item_ids"]
                if item_id in self.data["items"]
            ]
            if not scored_items:
                continue
            leaf_scores.append((leaf_id, sum(scored_items) / len(scored_items)))

        leaf_scores.sort(key=lambda pair: pair[1], reverse=True)

        candidate_ids: List[str] = []
        candidate_set = set()
        target_candidates = max(top_k_hot * 2, top_k_hot)
        for leaf_id, _ in leaf_scores:
            for item_id in self.data["nodes"][leaf_id].get("item_ids", []):
                if item_id not in candidate_set and item_id in self.data["items"]:
                    candidate_set.add(item_id)
                    candidate_ids.append(item_id)
            if len(candidate_ids) >= target_candidates:
                break

        ranked_items = sorted(
            [self.data["items"][item_id] for item_id in candidate_ids],
            key=lambda item: self.calculate_combined_score(item, query=query, query_embedding=query_embedding),
            reverse=True,
        )
        selected_items = ranked_items[:top_k_hot]
        selected_leaf_ids = []
        seen_leaf_ids = set()
        for item in selected_items:
            leaf_id = item.get("leaf_node_id")
            if leaf_id and leaf_id not in seen_leaf_ids:
                seen_leaf_ids.add(leaf_id)
                selected_leaf_ids.append(leaf_id)

        context = {
            "query": query,
            "leaf_node_ids": selected_leaf_ids,
            "item_ids": [item["id"] for item in selected_items],
            "leaf_scores": {leaf_id: score for leaf_id, score in leaf_scores},
        }
        self.data["metadata"]["last_retrieval_context"] = context
        return {
            "items": selected_items,
            "leaf_scores": leaf_scores,
            "context": context,
        }

    def to_string_for_prompt(self, top_k_hot: int = -1, query: Optional[str] = None) -> str:
        if top_k_hot == -1:
            return self._render_full_tree()

        retrieval = self._retrieve_items(top_k_hot=top_k_hot, query=query)
        output = ["=== RETRIEVED TREE PATHS ==="]
        if not retrieval["context"]["leaf_node_ids"]:
            output.append("(Empty)")
        else:
            for leaf_id in retrieval["context"]["leaf_node_ids"]:
                score = retrieval["context"]["leaf_scores"].get(leaf_id, 0.0)
                output.append(f"- {self._node_path_text(leaf_id)} | aggregated_score={score:.3f}")

        output.append("")
        output.append("=== TOP ITEMS ===")
        if not retrieval["items"]:
            output.append("(Empty)")
        for item in retrieval["items"]:
            output.append(f"- Path: {self._node_path_text(item.get('leaf_node_id'))}")
            output.extend(self._render_item_lines(item, include_stats=False))
            output.append("")
        return "\n".join(output).rstrip()

    def get_stats(self) -> str:
        total_items = len(self.data.get("items", {}))
        total_nodes = len(self.data.get("nodes", {}))
        total_leaves = len(self._iter_leaf_ids())
        total_length = len(self.to_string_for_prompt())
        return (
            f"Total Items: {total_items} | Total Nodes: {total_nodes} | "
            f"Leaf Nodes: {total_leaves} | Total Length: {total_length} characters"
        )

    def _tree_prompt_header(self) -> str:
        if not self.use_fixed_categories:
            return (
                "The cheatsheet is a hierarchical tree.\n"
                "Choose concise category, subcategory, and leaf_name labels based on the insight itself. "
                "Do not use a fixed taxonomy; create labels that best organize the reusable knowledge.\n"
                "When adding or refining items, preserve reusable natural-language guidance. "
                "Code snippets are optional and should only be included when they add concrete value."
            )

        return (
            "The cheatsheet is a hierarchical tree.\n"
            "The first layer is fixed to: Kernel Pattern, Correctness Rule, Performance Rule, Debugging Rule.\n"
            "When adding or refining items, preserve reusable natural-language guidance. "
            "Code snippets are optional and should only be included when they add concrete value.\n"
            "You may optionally provide category, subcategory, and leaf_name hints for routing, but they are not required."
        )

    def _tree_add_operation_description(self) -> str:
        if not self.use_fixed_categories:
            return (
                "1. ADD\n"
                "   - content: high-level reusable insight\n"
                "   - code_snippet: optional short code snippet\n"
                "   - category: optional LLM-chosen top-level routing label\n"
                "   - subcategory: optional LLM-chosen second-level routing label\n"
                "   - leaf_name: optional specific leaf label"
            )

        return (
            "1. ADD\n"
            "   - section: optional legacy compatibility hint from [meta_reasoning, solutions_and_patterns, failed_attempts]\n"
            "   - content: high-level reusable insight\n"
            "   - code_snippet: optional short code snippet\n"
            "   - category: optional one of [Kernel Pattern, Correctness Rule, Performance Rule, Debugging Rule]\n"
            "   - subcategory: optional internal routing label\n"
            "   - leaf_name: optional specific leaf label"
        )

    def _tree_update_operation_description(self) -> str:
        if not self.use_fixed_categories:
            return (
                "2. UPDATE\n"
                "   - target_id\n"
                "   - content\n"
                "   - code_snippet: optional\n"
                "   - category: optional LLM-chosen top-level routing label\n"
                "   - subcategory: optional LLM-chosen second-level routing label\n"
                "   - leaf_name: optional specific leaf label"
            )

        return (
            "2. UPDATE\n"
            "   - target_id\n"
            "   - content\n"
            "   - code_snippet: optional\n"
            "   - category / subcategory / leaf_name: optional routing overrides"
        )

    def build_prompt_no_qa(self, raw_prompt) -> str:
        template = """
You are a master curator of long-term technical knowledge. Your task is to update a tree-structured cheatsheet from the latest context.

{tree_header}

**CRITICAL: You MUST respond with valid JSON only.**

Current Cheatsheet Stats:
{cheatsheet_stats}

**Previous Cheatsheet Tree:**
{previous_cheatsheet}

**Current Context:**
{raw_prompt}

Output ONLY a valid JSON object with:
- reasoning
- operations

Available Operations:
{add_operation}
{update_operation}
3. VARIATION
   - target_id
   - name
   - content
4. EXPAND
   - target_id
   - content

If no update is needed, return an empty operations list.
"""
        return template.format(
            tree_header=self._tree_prompt_header(),
            cheatsheet_stats=self.get_stats(),
            previous_cheatsheet=self.to_string_for_prompt(),
            raw_prompt=raw_prompt,
            add_operation=self._tree_add_operation_description(),
            update_operation=self._tree_update_operation_description(),
        )

    def build_prompt_qa(self, question: str, model_answer: str) -> str:
        return self.build_prompt(question=question, model_answer=model_answer, model_reflection="")

    def build_prompt_reflect(self, question: str, model_reflection: str) -> str:
        template = """
You are a master curator of long-term technical knowledge. Your task is to update a tree-structured cheatsheet using the model reflection.

{tree_header}

Current Cheatsheet Stats:
{cheatsheet_stats}

**Previous Cheatsheet Tree:**
{previous_cheatsheet}

**Current Question:**
{question}

**Model Reflection:**
{model_reflection}

Output ONLY a valid JSON object with:
- reasoning
- operations

Available Operations:
{add_operation}
{update_operation}
3. VARIATION
   - target_id
   - name
   - content
4. EXPAND
   - target_id
   - content
"""
        return template.format(
            tree_header=self._tree_prompt_header(),
            cheatsheet_stats=self.get_stats(),
            previous_cheatsheet=self.to_string_for_prompt(),
            question=question,
            model_reflection=model_reflection,
            add_operation=self._tree_add_operation_description(),
            update_operation=self._tree_update_operation_description(),
        )

    def build_prompt(self, question: str, model_answer: str, model_reflection: str) -> str:
        template = """
You are a master curator of long-term technical knowledge. Your task is to update a tree-structured cheatsheet from the latest answer and reflection.

{tree_header}

Current Cheatsheet Stats:
{cheatsheet_stats}

**Previous Cheatsheet Tree:**
{previous_cheatsheet}

**Current Question:**
{question}

**Model Answer:**
{model_answer}

**Model Reflection:**
{model_reflection}

Output ONLY a valid JSON object with:
- reasoning
- operations

Available Operations:
{add_operation}
{update_operation}
3. VARIATION
   - target_id
   - name
   - content
4. EXPAND
   - target_id
   - content
5. REMOVE
   - target_id
6. ADD_RELATION
   - source_id
   - target_id
   - relation: one of [SIMILAR, REFINES, PREREQUISITE]
   - justification
7. UPDATE_RELATION
   - source_id
   - target_id
   - relation: one of [SIMILAR, REFINES, PREREQUISITE]
   - justification
"""
        return template.format(
            tree_header=self._tree_prompt_header(),
            cheatsheet_stats=self.get_stats(),
            previous_cheatsheet=self.to_string_for_prompt(),
            question=question,
            model_answer=model_answer,
            model_reflection=model_reflection,
            add_operation=self._tree_add_operation_description(),
            update_operation=self._tree_update_operation_description(),
        )

    def build_prompt_delta(self, question: str, model_answer: str, model_reflection: str) -> str:
        template = """
You are a curator of high-value technical deltas for a tree-structured cheatsheet.

{tree_header}

Extract only the minimal causal insight that explains:
- why a previous attempt failed
- why the current attempt succeeded
- what new transferable capability should be retained

Current Cheatsheet Stats:
{cheatsheet_stats}

**Previous Cheatsheet Tree:**
{previous_cheatsheet}

**Current Question:**
{question}

**Model Answer:**
{model_answer}

**Model Reflection:**
{model_reflection}

Output ONLY valid JSON with:
- reasoning
- operations

Available Operations:
{add_operation}
{update_operation}
3. VARIATION
   - target_id
   - name
   - content
4. EXPAND
   - target_id
   - content
"""
        return template.format(
            tree_header=self._tree_prompt_header(),
            cheatsheet_stats=self.get_stats(),
            previous_cheatsheet=self.to_string_for_prompt(),
            question=question,
            model_answer=model_answer,
            model_reflection=model_reflection,
            add_operation=self._tree_add_operation_description(),
            update_operation=self._tree_update_operation_description(),
        )

    def build_prompt_delta_no_qa(self, raw_prompt) -> str:
        template = """
You are a curator of high-value technical deltas for a tree-structured cheatsheet.

{tree_header}

Current Cheatsheet Stats:
{cheatsheet_stats}

**Previous Cheatsheet Tree:**
{previous_cheatsheet}

**Current Context:**
{raw_prompt}

Output ONLY valid JSON with:
- reasoning
- operations

Available Operations:
{add_operation}
{update_operation}
3. VARIATION
   - target_id
   - name
   - content
4. EXPAND
   - target_id
   - content
"""
        return template.format(
            tree_header=self._tree_prompt_header(),
            cheatsheet_stats=self.get_stats(),
            previous_cheatsheet=self.to_string_for_prompt(),
            raw_prompt=raw_prompt,
            add_operation=self._tree_add_operation_description(),
            update_operation=self._tree_update_operation_description(),
        )

    def build_prompt_relation(self, question: str, model_answer: str, model_reflection: str) -> str:
        return self.build_prompt(question=question, model_answer=model_answer, model_reflection=model_reflection)

    def build_prompt_relation_no_qa(self, raw_prompt) -> str:
        return self.build_prompt_no_qa(raw_prompt)

    def prune_length(self, max_length: int = 1000000, max_items: int = 100):
        while len(self.data["items"]) > max_items:
            candidate = min(
                self.data["items"].values(),
                key=lambda item: (self.calculate_combined_score(item), item.get("created_iter", 0)),
            )
            self._remove_item_by_id(candidate["id"])

        while len(self.to_string_for_prompt()) > max_length and self.data["items"]:
            candidate = min(
                self.data["items"].values(),
                key=lambda item: (self.calculate_combined_score(item), item.get("created_iter", 0)),
            )
            self._remove_item_by_id(candidate["id"])

    def prune_by_utility(self, min_usage_ratio: float = 0.5, age_threshold: int = 2, query: Optional[str] = None):
        query_embedding = self._safe_get_embedding(query, is_query=True) if query else None
        to_remove: List[str] = []
        for item_id, item in self.data["items"].items():
            age = self.current_iteration - item.get("created_iter", 0)
            if age < age_threshold:
                continue
            score_parts = self._score_item(item, query=query, query_embedding=query_embedding)
            if score_parts["combined"] < min_usage_ratio:
                to_remove.append(item_id)

        for item_id in to_remove:
            self._remove_item_by_id(item_id)

    def build_prompt_for_pruning(self, target_length: int = 1000000) -> str:
        template = """
You are a master curator of long-term technical knowledge. The current tree cheatsheet exceeds the desired {target_length} character limit.

{tree_header}

Current Cheatsheet Stats:
{cheatsheet_stats}

**Current Cheatsheet Tree:**
{cheatsheet}

Output ONLY valid JSON with:
- reasoning
- operations

Available Operations:
1. REMOVE
   - target_id
{update_operation}
"""
        return template.format(
            target_length=target_length,
            tree_header=self._tree_prompt_header(),
            cheatsheet_stats=self.get_stats(),
            cheatsheet=self.to_string_for_prompt(),
            update_operation=self._tree_update_operation_description(),
        )

    def _find_item_by_id(self, target_id: str):
        item = self.data["items"].get(target_id)
        if not item:
            return None, None
        leaf = self.data["nodes"].get(item.get("leaf_node_id"))
        parent_list = leaf.get("item_ids") if leaf else None
        return item, parent_list

    def _bump_node_access(self, node_id: Optional[str]):
        while node_id and node_id in self.data["nodes"]:
            node = self.data["nodes"][node_id]
            node.setdefault("stats", {})
            node["stats"]["access_count"] = node["stats"].get("access_count", 0) + 1
            node_id = node.get("parent_id")

    def record_usage(self, model_thought: str, current_iter: int, pass_call: bool = False, pass_exe: bool = False):
        self.current_iteration = current_iter
        self.data["metadata"]["current_iteration"] = current_iter
        unique_ids_in_this_run = self._extract_referenced_ids(model_thought)
        if unique_ids_in_this_run is None:
            return
        observed_gain = self._observed_performance_gain(pass_call=pass_call, pass_exe=pass_exe)

        for target_id in unique_ids_in_this_run:
            item = self.data["items"].get(target_id)
            if not item:
                continue
            item["usage_count"] += 1
            item["last_used_iter"] = self.current_iteration
            if observed_gain is not None:
                item["performance_gain"] = max(
                    self.calculate_performance_gain(item),
                    observed_gain,
                )
            self._bump_node_access(item.get("leaf_node_id"))

    def apply_operations(self, llm_response: str):
        try:
            clean_response = llm_response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:-3]
            elif clean_response.startswith("```"):
                clean_response = clean_response[3:-3]

            parsed = json.loads(clean_response)
            ops = parsed.get("operations", [])
            temp_id_map = {}

            for op in ops:
                op_type = op.get("type", "").upper()
                if op_type == "ADD":
                    self._op_add(op, temp_id_map)
                elif op_type == "UPDATE":
                    self._op_update(op)
                elif op_type == "VARIATION":
                    self._op_variation(op)
                elif op_type == "EXPAND":
                    self._op_expand(op)
                elif op_type == "REMOVE":
                    self._op_remove(op)
                elif op_type == "ADD_RELATION":
                    self._op_add_relation(op, temp_id_map)
                elif op_type == "UPDATE_RELATION":
                    self._op_update_relation(op, temp_id_map)
                elif op_type in {"META_REASONING", "SOLUTIONS_AND_PATTERNS", "FAILED_ATTEMPTS"}:
                    inferred = dict(op)
                    inferred["type"] = "ADD"
                    inferred["section"] = op_type.lower()
                    self._op_add(inferred, temp_id_map)
        except json.JSONDecodeError:
            print("Error: Failed to parse LLM response as JSON.")
        except Exception as exc:
            print(f"Error applying operations: {exc}")

    def _resolve_item_reference(self, item_id: str, temp_id_map: Optional[Dict[str, str]] = None) -> str:
        if temp_id_map and item_id in temp_id_map:
            return temp_id_map[item_id]
        return item_id

    def _op_add(self, op, temp_id_map: Optional[Dict[str, str]] = None):
        content = op.get("content", "")
        ref_id = op.get("ref_id")
        item_id = self._generate_id()
        while item_id in self.data["items"]:
            item_id = self._generate_id()

        new_item = {
            "id": item_id,
            "content": content,
            "code_snippet": op.get("code_snippet", ""),
            "usage_count": 0,
            "last_used_iter": -1,
            "created_iter": self.current_iteration,
            "variations": [],
            "edge_cases": [],
            "relations": [],
            "embedding": op.get("embedding", []),
            "performance_gain": op.get("performance_gain", 0.0),
            "conflict_count": op.get("conflict_count", 0),
            "legacy_section": (op.get("section") or "").lower(),
            "category": op.get("category", ""),
            "subcategory": op.get("subcategory", ""),
            "leaf_name": op.get("leaf_name", ""),
        }
        self._normalize_item(new_item)
        self.data["items"][item_id] = new_item
        self._place_item(
            new_item,
            category_hint=op.get("category", ""),
            subcategory_hint=op.get("subcategory", ""),
            leaf_hint=op.get("leaf_name", ""),
            preserve_existing_leaf=False,
        )
        self._cleanup_redundant_nodes()
        if temp_id_map is not None and ref_id:
            temp_id_map[ref_id] = item_id

    def _op_update(self, op):
        target_id = op.get("target_id")
        item = self.data["items"].get(target_id)
        if not item:
            print(f" ! FAILED UPDATE: ID {target_id} not found.")
            return

        item["content"] = op.get("content", item.get("content", ""))
        if "code_snippet" in op:
            item["code_snippet"] = op.get("code_snippet", "")
        if "embedding" in op:
            item["embedding"] = op.get("embedding", [])
        if "performance_gain" in op:
            item["performance_gain"] = op.get("performance_gain", item.get("performance_gain", 0.0))
        if "conflict_count" in op:
            item["conflict_count"] = op.get("conflict_count", item.get("conflict_count", 0))
        if "section" in op:
            item["legacy_section"] = (op.get("section") or "").lower()
        if "category" in op:
            item["category"] = op.get("category", "")
        if "subcategory" in op:
            item["subcategory"] = op.get("subcategory", "")
        if "leaf_name" in op:
            item["leaf_name"] = op.get("leaf_name", "")

        self._normalize_item(item)
        self._place_item(
            item,
            category_hint=op.get("category", ""),
            subcategory_hint=op.get("subcategory", ""),
            leaf_hint=op.get("leaf_name", ""),
            preserve_existing_leaf=False,
        )
        self._cleanup_redundant_nodes()

    def _op_variation(self, op):
        target_id = op.get("target_id")
        item = self.data["items"].get(target_id)
        if not item:
            print(f" ! FAILED VARIATION: ID {target_id} not found.")
            return
        item.setdefault("variations", [])
        item["variations"].append({"name": op.get("name"), "content": op.get("content")})

    def _op_expand(self, op):
        target_id = op.get("target_id")
        item = self.data["items"].get(target_id)
        if not item:
            print(f" ! FAILED EXPAND: ID {target_id} not found.")
            return
        item.setdefault("edge_cases", [])
        item["edge_cases"].append({"content": op.get("content")})

    def _remove_item_by_id(self, target_id: str):
        item = self.data["items"].get(target_id)
        if not item:
            return
        self._remove_item_from_leaf(item)
        del self.data["items"][target_id]
        for other_item in self.data["items"].values():
            other_item["relations"] = [
                relation for relation in other_item.get("relations", [])
                if relation.get("target_id") != target_id
            ]
        self._cleanup_redundant_nodes()

    def _op_remove(self, op):
        target_id = op.get("target_id")
        if target_id not in self.data["items"]:
            print(f" ! FAILED REMOVE: ID {target_id} not found.")
            return
        self._remove_item_by_id(target_id)

    def _op_add_relation(self, op, temp_id_map: Optional[Dict[str, str]] = None):
        source_id = self._resolve_item_reference(op.get("source_id"), temp_id_map)
        target_id = self._resolve_item_reference(op.get("target_id"), temp_id_map)
        relation = op.get("relation")
        justification = op.get("justification", "")
        allowed_relations = {"SIMILAR", "REFINES", "PREREQUISITE"}

        if not source_id or not target_id or source_id == target_id or not isinstance(relation, str):
            return
        relation = relation.upper()
        if relation not in allowed_relations:
            return

        source_item = self.data["items"].get(source_id)
        target_item = self.data["items"].get(target_id)
        if not source_item or not target_item:
            return

        source_item.setdefault("relations", [])
        if any(
            existing.get("type") == relation and existing.get("target_id") == target_id
            for existing in source_item["relations"]
        ):
            return
        if len(source_item["relations"]) >= 2:
            return

        source_item["relations"].append(
            {
                "type": relation,
                "target_id": target_id,
                "justification": justification,
            }
        )

    def _op_update_relation(self, op, temp_id_map: Optional[Dict[str, str]] = None):
        source_id = self._resolve_item_reference(op.get("source_id"), temp_id_map)
        target_id = self._resolve_item_reference(op.get("target_id"), temp_id_map)
        relation = op.get("relation")
        justification = op.get("justification", "")
        allowed_relations = {"SIMILAR", "REFINES", "PREREQUISITE"}

        if not source_id or not target_id or source_id == target_id or not isinstance(relation, str):
            return
        relation = relation.upper()
        if relation not in allowed_relations:
            return

        source_item = self.data["items"].get(source_id)
        target_item = self.data["items"].get(target_id)
        if not source_item or not target_item:
            return

        for existing in source_item.get("relations", []):
            if existing.get("target_id") == target_id:
                existing["type"] = relation
                existing["justification"] = justification
                return


CheatsheetManager = TreeCheatsheetManager
