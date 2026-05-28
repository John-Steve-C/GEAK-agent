import argparse
import html
import json
import re
import webbrowser
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


TREE_KEYS = {"root_node_id", "nodes", "items"}


def is_tree_state(value: Any) -> bool:
    return isinstance(value, dict) and TREE_KEYS.issubset(value.keys())


def find_tree_state(value: Any) -> Optional[Dict[str, Any]]:
    if is_tree_state(value):
        return value
    if isinstance(value, dict):
        for child in value.values():
            found = find_tree_state(child)
            if found:
                return found
    if isinstance(value, list):
        for child in value:
            found = find_tree_state(child)
            if found:
                return found
    return None


def companion_paths(path: Path) -> Iterable[Path]:
    stem = path.stem

    if "_mem_" in stem:
        yield path.with_name(stem.replace("_mem_", "_cheatsheet_") + ".json")

    match = re.match(r"^(?P<prefix>.+)_(?P<iter>\d+)$", stem)
    if match:
        yield path.with_name(f"{match.group('prefix')}_cheatsheet_{match.group('iter')}.json")

    yield path.with_suffix(".json")


def load_json_or_jsonl(path: Path) -> Tuple[Dict[str, Any], Path]:
    if not path.exists():
        raise FileNotFoundError(path)

    if path.suffix == ".jsonl":
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                found = find_tree_state(json.loads(line))
                if found:
                    return found, path
    else:
        with path.open("r", encoding="utf-8") as f:
            found = find_tree_state(json.load(f))
            if found:
                return found, path

    for candidate in companion_paths(path):
        if candidate == path or not candidate.exists():
            continue
        with candidate.open("r", encoding="utf-8") as f:
            found = find_tree_state(json.load(f))
            if found:
                return found, candidate

    raise ValueError(
        f"No tree cheatsheet state found in {path}. Expected keys: root_node_id, nodes, items."
    )


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def truncate(text: Any, max_chars: int) -> str:
    text = "" if text is None else str(text)
    if max_chars > 0 and len(text) > max_chars:
        return text[:max_chars].rstrip() + "..."
    return text


def valid_child_ids(nodes: Dict[str, Dict[str, Any]], child_ids: List[str]) -> List[str]:
    return [node_id for node_id in child_ids if node_id in nodes]


def item_search_text(item: Dict[str, Any]) -> str:
    parts = [
        item.get("id", ""),
        item.get("content", ""),
        item.get("code_snippet", ""),
        item.get("category", ""),
        item.get("subcategory", ""),
        item.get("leaf_name", ""),
    ]
    for variation in item.get("variations", []) or []:
        parts.append(variation.get("content", ""))
    for edge_case in item.get("edge_cases", []) or []:
        parts.append(edge_case.get("content", ""))
    return " ".join(str(part) for part in parts if part)


def render_item(item: Dict[str, Any], max_item_chars: int) -> str:
    item_id = item.get("id", "")
    content = truncate(item.get("content", ""), max_item_chars)
    code = truncate(item.get("code_snippet", ""), max_item_chars)
    variations = item.get("variations", []) or []
    edge_cases = item.get("edge_cases", []) or []
    relations = item.get("relations", []) or []

    stats = [
        ("usage", item.get("usage_count", 0)),
        ("last", item.get("last_used_iter", -1)),
        ("created", item.get("created_iter", 0)),
        ("gain", item.get("performance_gain", 0.0)),
        ("conflicts", item.get("conflict_count", 0)),
    ]
    stats_html = "".join(f"<span>{esc(name)}: {esc(value)}</span>" for name, value in stats)

    extra_parts = []
    if code:
        extra_parts.append(f"<div class=\"item-section\">Code</div><pre>{esc(code)}</pre>")
    if variations:
        body = "".join(
            f"<li><b>{esc(variation.get('name', 'variant'))}</b>: "
            f"{esc(truncate(variation.get('content', ''), max_item_chars))}</li>"
            for variation in variations
        )
        extra_parts.append(f"<div class=\"item-section\">Variations</div><ul>{body}</ul>")
    if edge_cases:
        body = "".join(
            f"<li>{esc(truncate(edge_case.get('content', ''), max_item_chars))}</li>"
            for edge_case in edge_cases
        )
        extra_parts.append(f"<div class=\"item-section\">Notes</div><ul>{body}</ul>")
    if relations:
        body = "".join(
            "<li>"
            f"{esc(relation.get('type', 'UNKNOWN'))} -> {esc(relation.get('target_id', 'UNKNOWN'))}"
            f"{': ' + esc(relation.get('justification', '')) if relation.get('justification') else ''}"
            "</li>"
            for relation in relations
        )
        extra_parts.append(f"<div class=\"item-section\">Relations</div><ul>{body}</ul>")

    return f"""
<div class="item" data-search="{esc(item_search_text(item)).lower()}">
  <div class="item-title"><span class="item-id">ID: {esc(item_id)}</span></div>
  <div class="item-content">{esc(content)}</div>
  <div class="item-stats">{stats_html}</div>
  {''.join(extra_parts)}
</div>
"""


def count_descendant_items(nodes: Dict[str, Dict[str, Any]], node_id: str) -> int:
    node = nodes[node_id]
    count = len(node.get("item_ids", []) or [])
    for child_id in node.get("child_ids", []) or []:
        if child_id in nodes:
            count += count_descendant_items(nodes, child_id)
    return count


def render_node(
    state: Dict[str, Any],
    node_id: str,
    depth: int,
    max_item_chars: int,
    open_depth: int,
) -> str:
    nodes = state["nodes"]
    items = state["items"]
    node = nodes[node_id]
    child_ids = valid_child_ids(nodes, node.get("child_ids", []) or [])
    item_ids = [item_id for item_id in node.get("item_ids", []) or [] if item_id in items]
    descendant_items = count_descendant_items(nodes, node_id)
    node_type = node.get("node_type", "internal")
    access_count = node.get("stats", {}).get("access_count", 0)
    path = " > ".join(node.get("path", []) or [node.get("name", node_id)])
    open_attr = " open" if depth <= open_depth else ""
    search_text = " ".join([node.get("id", ""), node.get("name", ""), node_type, path]).lower()

    child_html = "".join(
        render_node(state, child_id, depth + 1, max_item_chars, open_depth)
        for child_id in child_ids
    )
    item_html = "".join(render_item(items[item_id], max_item_chars) for item_id in item_ids)

    return f"""
<details class="node node-{esc(node_type)}" data-search="{esc(search_text)}"{open_attr}>
  <summary>
    <span class="node-name">{esc(node.get('name', node_id))}</span>
    <span class="badge">{esc(node_type)}</span>
    <span class="muted">{descendant_items} items</span>
    <span class="muted">access {esc(access_count)}</span>
  </summary>
  <div class="node-meta">{esc(path)} | {esc(node.get('id', node_id))}</div>
  <div class="children">
    {child_html}
    {item_html}
  </div>
</details>
"""


def max_depth(nodes: Dict[str, Dict[str, Any]], node_id: str, depth: int = 0) -> int:
    child_depths = [
        max_depth(nodes, child_id, depth + 1)
        for child_id in nodes[node_id].get("child_ids", []) or []
        if child_id in nodes
    ]
    return max([depth] + child_depths)


def build_html(state: Dict[str, Any], source_path: Path, max_item_chars: int, open_depth: int) -> str:
    nodes = state.get("nodes", {})
    items = state.get("items", {})
    root_id = state.get("root_node_id", "root")
    if root_id not in nodes:
        raise ValueError(f"Root node {root_id!r} is missing from cheatsheet state.")

    node_type_counts: Dict[str, int] = {}
    for node in nodes.values():
        node_type = node.get("node_type", "internal")
        node_type_counts[node_type] = node_type_counts.get(node_type, 0) + 1

    metadata = state.get("metadata", {}) or {}
    summary_cards = [
        ("Items", len(items)),
        ("Nodes", len(nodes)),
        ("Leaves", node_type_counts.get("leaf", 0)),
        ("Depth", max_depth(nodes, root_id)),
        ("Iteration", metadata.get("current_iteration", "n/a")),
    ]
    cards_html = "".join(
        f"<div class=\"card\"><div class=\"card-value\">{esc(value)}</div><div class=\"card-label\">{esc(label)}</div></div>"
        for label, value in summary_cards
    )
    counts_html = ", ".join(f"{esc(key)}: {esc(value)}" for key, value in sorted(node_type_counts.items()))
    tree_html = render_node(state, root_id, 0, max_item_chars, open_depth)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tree Cheatsheet Visualization</title>
<style>
:root {{
  color-scheme: light;
  --bg: #f7f7f5;
  --panel: #ffffff;
  --ink: #202124;
  --muted: #60646c;
  --line: #d8dadd;
  --accent: #1264a3;
  --accent-bg: #e8f2fb;
  --leaf-bg: #f3f9ef;
  --item-bg: #fff9ea;
  --code-bg: #f1f3f4;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.45;
}}
header {{
  position: sticky;
  top: 0;
  z-index: 2;
  background: rgba(247, 247, 245, 0.96);
  border-bottom: 1px solid var(--line);
  padding: 18px 24px;
}}
h1 {{
  margin: 0 0 6px;
  font-size: 24px;
  font-weight: 650;
  letter-spacing: 0;
}}
.source, .counts {{
  color: var(--muted);
  font-size: 13px;
  word-break: break-all;
}}
.toolbar {{
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 14px;
}}
input[type="search"] {{
  min-width: min(520px, 100%);
  flex: 1;
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 9px 10px;
  font: inherit;
  background: white;
}}
button {{
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 9px 12px;
  background: white;
  color: var(--ink);
  font: inherit;
  cursor: pointer;
}}
button:hover {{ border-color: var(--accent); color: var(--accent); }}
main {{
  padding: 20px 24px 40px;
  max-width: 1400px;
  margin: 0 auto;
}}
.cards {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 10px;
  margin-bottom: 16px;
}}
.card {{
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 12px;
}}
.card-value {{ font-size: 22px; font-weight: 700; }}
.card-label {{ color: var(--muted); font-size: 13px; }}
.tree {{
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 10px 12px;
}}
details {{
  margin: 6px 0 6px 18px;
  border-left: 2px solid var(--line);
  padding-left: 10px;
}}
details.node-root {{
  margin-left: 0;
  border-left: 0;
  padding-left: 0;
}}
details.node-leaf {{
  border-left-color: #78a65a;
  background: var(--leaf-bg);
  border-radius: 6px;
  padding-top: 2px;
  padding-bottom: 2px;
}}
summary {{
  cursor: pointer;
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  padding: 4px 0;
}}
summary::-webkit-details-marker {{ display: none; }}
summary::before {{
  content: "+";
  display: inline-grid;
  place-items: center;
  width: 18px;
  height: 18px;
  border: 1px solid var(--line);
  border-radius: 50%;
  color: var(--muted);
  font-size: 13px;
}}
details[open] > summary::before {{ content: "-"; }}
.node-name {{ font-weight: 650; }}
.badge {{
  border-radius: 999px;
  background: var(--accent-bg);
  color: var(--accent);
  padding: 2px 7px;
  font-size: 12px;
  font-weight: 600;
}}
.muted, .node-meta {{
  color: var(--muted);
  font-size: 12px;
}}
.node-meta {{
  margin: 0 0 4px 26px;
  word-break: break-word;
}}
.children {{ margin-left: 8px; }}
.item {{
  margin: 8px 0 8px 28px;
  padding: 10px 12px;
  border: 1px solid #ead7a2;
  border-radius: 8px;
  background: var(--item-bg);
}}
.item-title {{
  display: flex;
  gap: 8px;
  align-items: center;
  margin-bottom: 5px;
}}
.item-id {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 12px;
  color: var(--accent);
  font-weight: 700;
}}
.item-content {{
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}}
.item-stats {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  color: var(--muted);
  font-size: 12px;
  margin-top: 6px;
}}
.item-section {{
  margin-top: 8px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
}}
pre {{
  margin: 6px 0 0;
  padding: 10px;
  border-radius: 6px;
  background: var(--code-bg);
  overflow-x: auto;
  white-space: pre-wrap;
}}
ul {{ margin: 6px 0 0 18px; padding: 0; }}
.hidden {{ display: none !important; }}
mark {{ background: #ffe08a; padding: 0 2px; }}
@media (max-width: 700px) {{
  header, main {{ padding-left: 14px; padding-right: 14px; }}
  details {{ margin-left: 10px; padding-left: 8px; }}
  .item {{ margin-left: 12px; }}
}}
</style>
</head>
<body>
<header>
  <h1>Tree Cheatsheet Visualization</h1>
  <div class="source">Source: {esc(source_path)}</div>
  <div class="counts">Node types: {counts_html}</div>
  <div class="toolbar">
    <input id="search" type="search" placeholder="Search nodes and items">
    <button id="expand">Expand all</button>
    <button id="collapse">Collapse all</button>
  </div>
</header>
<main>
  <section class="cards">{cards_html}</section>
  <section class="tree" id="tree">{tree_html}</section>
</main>
<script>
const search = document.getElementById("search");
const tree = document.getElementById("tree");
const allDetails = () => Array.from(tree.querySelectorAll("details"));
const allSearchables = () => Array.from(tree.querySelectorAll("[data-search]"));

document.getElementById("expand").addEventListener("click", () => {{
  allDetails().forEach((el) => el.open = true);
}});
document.getElementById("collapse").addEventListener("click", () => {{
  allDetails().forEach((el) => el.open = false);
  const root = tree.querySelector("details.node-root");
  if (root) root.open = true;
}});

search.addEventListener("input", () => {{
  const q = search.value.trim().toLowerCase();
  allSearchables().forEach((el) => el.classList.remove("hidden"));
  if (!q) return;

  allSearchables().forEach((el) => {{
    const matched = el.dataset.search.includes(q);
    if (!matched) el.classList.add("hidden");
  }});

  allSearchables().forEach((el) => {{
    if (!el.classList.contains("hidden")) {{
      let parent = el.parentElement;
      while (parent && parent !== tree) {{
        if (parent.matches && parent.matches("details")) {{
          parent.classList.remove("hidden");
          parent.open = true;
        }}
        parent = parent.parentElement;
      }}
    }}
  }});

  allDetails().forEach((detail) => {{
    if (detail.querySelector("[data-search]:not(.hidden)")) {{
      detail.classList.remove("hidden");
      detail.open = true;
    }}
  }});
}});
</script>
</body>
</html>
"""


def default_output_path(source_path: Path) -> Path:
    return source_path.with_suffix(".html")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a TreeCheatsheetManager_v3 state as a self-contained HTML tree."
    )
    parser.add_argument(
        "input",
        help="Tree cheatsheet JSON, result JSONL, or related memory JSON path.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output HTML path. Defaults to the resolved cheatsheet JSON path with .html suffix.",
    )
    parser.add_argument(
        "--max-item-chars",
        type=int,
        default=1200,
        help="Maximum displayed characters per item field. Use 0 for no truncation.",
    )
    parser.add_argument(
        "--open-depth",
        type=int,
        default=2,
        help="Open tree nodes through this depth in the initial view.",
    )
    parser.add_argument(
        "--open-browser",
        action="store_true",
        help="Open the generated HTML in the default browser.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    state, source_path = load_json_or_jsonl(input_path)
    output_path = Path(args.output) if args.output else default_output_path(source_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        build_html(
            state,
            source_path=source_path,
            max_item_chars=args.max_item_chars,
            open_depth=args.open_depth,
        ),
        encoding="utf-8",
    )

    print(f"Loaded tree cheatsheet from {source_path}")
    print(f"Wrote visualization to {output_path}")
    print(f"Items: {len(state.get('items', {}))} | Nodes: {len(state.get('nodes', {}))}")

    if args.open_browser:
        webbrowser.open(output_path.resolve().as_uri())


if __name__ == "__main__":
    main()
