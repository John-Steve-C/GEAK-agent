import argparse
import concurrent.futures
import json
import os
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

from memories.TreeCheatsheetManager_v2 import TreeCheatsheetConfig, TreeCheatsheetManager
from models.OpenAI import OpenAIModel


DEFAULT_DOCS_DIR = "./triton_docs_markdown"
DEFAULT_TRAINSET_PATH = "./dataloaders/TB_eval/train_crawl.json"
DEFAULT_OUTPUT_PATH = "./triton_tree_cheatsheet.json"
DEFAULT_MODEL = "gpt-4.1-mini"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap a tree cheatsheet from crawled docs.")
    parser.add_argument("--docs-dir", default=DEFAULT_DOCS_DIR, help="Directory containing .md/.txt docs.")
    parser.add_argument("--prefix", default=None, help="Optional filename prefix filter.")
    parser.add_argument("--trainset", default=DEFAULT_TRAINSET_PATH, help="Optional trainset JSON to ingest.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_PATH, help="Output tree cheatsheet JSON path.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI model id for extraction.")
    parser.add_argument("--temperature", type=float, default=1.0, help="Extraction temperature.")
    parser.add_argument("--max-tokens", type=int, default=4000, help="Max tokens per extraction call.")
    parser.add_argument("--max-docs", type=int, default=None, help="Optional limit on loaded docs.")
    parser.add_argument("--leaf-capacity", type=int, default=10, help="Leaf capacity before split.")
    parser.add_argument("--leaf-cluster-size", type=int, default=3, help="Initial leaf grouping size.")
    parser.add_argument("--branching-factor", type=int, default=3, help="Target branch width.")
    parser.add_argument("--workers", type=int, default=8, help="Number of chunk extraction threads.")
    parser.add_argument(
        "--include-code-snippet",
        action="store_true",
        help="Allow bootstrap extraction to include code_snippet when needed.",
    )
    return parser.parse_args()


def read_documents(directory: str, prefix: Optional[str] = None, max_docs: Optional[int] = None) -> List[Dict[str, str]]:
    docs: List[Dict[str, str]] = []
    directory_path = Path(directory)
    for filepath in sorted(directory_path.rglob("*")):
        if not filepath.is_file():
            continue
        if filepath.suffix not in {".md", ".txt"}:
            continue
        if prefix and not filepath.name.startswith(prefix):
            continue
        docs.append(
            {
                "source_doc": str(filepath.relative_to(directory_path)),
                "text": filepath.read_text(encoding="utf-8"),
            }
        )
        if max_docs is not None and len(docs) >= max_docs:
            break
    return docs


def read_trainset_documents(path: str, max_docs: Optional[int] = None) -> List[Dict[str, str]]:
    trainset_path = Path(path)
    if not trainset_path.exists():
        return []
    data = json.loads(trainset_path.read_text(encoding="utf-8"))
    docs: List[Dict[str, str]] = []
    for index, entry in enumerate(data):
        description_parts = [
            (entry.get("description_1") or "").strip(),
            (entry.get("description_2") or "").strip(),
        ]
        text_parts = [part for part in description_parts if part]
        code = (entry.get("code") or "").strip()
        if code:
            text_parts.append(f"```python\n{code}\n```")
        if not text_parts:
            continue
        docs.append(
            {
                "source_doc": f"train_crawl.json::{index}",
                "text": "\n\n".join(text_parts),
            }
        )
        if max_docs is not None and len(docs) >= max_docs:
            break
    return docs


def parse_json_response(response_text: str) -> Dict[str, Any]:
    clean_response = response_text.strip()
    if clean_response.startswith("```json"):
        clean_response = clean_response[7:-3]
    elif clean_response.startswith("```"):
        clean_response = clean_response[3:-3]
    try:
        parsed = json.loads(clean_response)
    except json.JSONDecodeError:
        print("Warning: Failed to parse JSON response. Returning empty dict.")
        print("Raw response was:", response_text)
        return {"items": []}
    
    return parsed


def make_llm_extractor(
    model: OpenAIModel,
    manager: TreeCheatsheetManager,
    manager_lock: threading.RLock,
    temperature: float,
    max_tokens: int,
    include_code_snippet: bool,
):
    def extractor(chunk_text: str) -> Dict[str, Any]:
        with manager_lock:
            prompt = manager.build_bootstrap_extraction_prompt(
                chunk_text,
                include_code_snippet=include_code_snippet,
            )
        response = model.generate(
            [{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return parse_json_response(response)

    return extractor


def summarize_group(items: List[Dict[str, Any]]) -> Dict[str, str]:
    concepts = [item.get("key_concept", "").strip() for item in items if item.get("key_concept")]
    descriptions = [item.get("short_description", "").strip() for item in items if item.get("short_description")]
    if not concepts:
        concepts = ["Cheatsheet Group"]
    name = " / ".join(concepts[:2])
    description = " | ".join(descriptions[:2])[:240] if descriptions else "Grouped technical cheatsheet items."
    return {"name": name, "description": description}


def create_model_factory(api_key: str, model_id: str):
    thread_local = threading.local()

    def get_model() -> OpenAIModel:
        if not hasattr(thread_local, "model"):
            thread_local.model = OpenAIModel(api_key=api_key, model_id=model_id)
        return thread_local.model

    return get_model


def build_chunk_tasks(
    documents: List[Dict[str, str]],
    manager: TreeCheatsheetManager,
    manager_lock: threading.RLock,
) -> List[Dict[str, str]]:
    tasks: List[Dict[str, str]] = []
    for document in documents:
        with manager_lock:
            chunks = manager.chunk_document(document["text"], manager.config.to_dict())
        for chunk in chunks:
            tasks.append(
                {
                    "source_doc": document["source_doc"],
                    "chunk_id": chunk["chunk_id"],
                    "text": chunk["text"],
                }
            )
    return tasks


def extract_chunk_candidates(
    task: Dict[str, str],
    manager: TreeCheatsheetManager,
    manager_lock: threading.RLock,
    get_model,
    temperature: float,
    max_tokens: int,
    include_code_snippet: bool,
) -> Dict[str, Any]:
    model = get_model()
    extractor = make_llm_extractor(
        model=model,
        manager=manager,
        manager_lock=manager_lock,
        temperature=temperature,
        max_tokens=max_tokens,
        include_code_snippet=include_code_snippet,
    )

    extracted = extractor(task["text"])
    with manager_lock:
        candidates = manager._normalize_extractor_output(extracted, task["text"])

    normalized_candidates: List[Dict[str, Any]] = []
    for candidate in candidates:
        short_description = candidate.get("short_description", "").strip()
        if not short_description:
            continue
        normalized_candidates.append(
            {
                "category": candidate.get("category", "").strip(),
                "subcategory": candidate.get("subcategory", "").strip(),
                "leaf_name": candidate.get("leaf_name", "").strip(),
                "key_concept": candidate.get("key_concept", "").strip(),
                "short_description": short_description,
                "code_snippet": candidate.get("code_snippet", "").strip(),
                "source_doc": candidate.get("source_doc", task["source_doc"]),
                "source_chunk_id": candidate.get("source_chunk_id", task["chunk_id"]),
            }
        )
    return {
        "source_doc": task["source_doc"],
        "chunk_id": task["chunk_id"],
        "candidates": normalized_candidates,
    }

def main():
    args = parse_args()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required to run tree_cheatsheet_init.py")

    config = TreeCheatsheetConfig(
        leaf_capacity=args.leaf_capacity,
        leaf_cluster_size=args.leaf_cluster_size,
        branching_factor=args.branching_factor,
    )
    
    # with open("triton_tree_cheatsheet_v2.json", "r", encoding="utf-8") as f:
    #     init = json.load(f)
    manager = TreeCheatsheetManager(config=config)
    # print("Initial Cheatsheet Stats:", manager.get_stats())
    # exit(0)

    manager_lock = threading.RLock()
    get_model = create_model_factory(api_key=api_key, model_id=args.model)

    documents = read_documents(args.docs_dir, prefix=args.prefix, max_docs=args.max_docs)
    trainset_documents = read_trainset_documents(args.trainset, max_docs=args.max_docs)
    all_documents = documents + trainset_documents
    print(f"{len(documents)} docs loaded from {args.docs_dir}.")
    print(f"{len(trainset_documents)} trainset entries loaded from {args.trainset}.")
    if not all_documents:
        raise RuntimeError("No documentation or trainset entries were found for tree cheatsheet bootstrap.")

    chunk_tasks = build_chunk_tasks(all_documents, manager, manager_lock)
    print(f"{len(chunk_tasks)} semantic chunks queued for extraction.")

    all_candidates: List[Dict[str, Any]] = []
    worker_count = max(1, min(args.workers, len(chunk_tasks)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker_count) as executor:
        future_to_task = {
            executor.submit(
                extract_chunk_candidates,
                task,
                manager,
                manager_lock,
                get_model,
                args.temperature,
                args.max_tokens,
                args.include_code_snippet,
            ): task
            for task in chunk_tasks
        }
        completed = 0
        for future in concurrent.futures.as_completed(future_to_task):
            task = future_to_task[future]
            result = future.result()
            candidates = result["candidates"]
            all_candidates.extend(candidates)
            completed += 1
            print(
                f"[{completed}/{len(chunk_tasks)}] {result['source_doc']}:{result['chunk_id']} "
                f"-> {len(candidates)} items, cumulative {len(all_candidates)}"
            )

    manager.build_tree_from_items(
        items=all_candidates,
        embedder=None,
        clusterer=None,
        summarizer=summarize_group,
        config=config.to_dict(),
    )

    output_path = Path(args.output)
    output_path.write_text(manager.to_json(), encoding="utf-8")
    print(f"Saved tree cheatsheet to {output_path}")
    print("Final Cheatsheet Stats:", manager.get_stats())

def visualize_cheatsheet(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    manager = TreeCheatsheetManager(initial_state=data)
    print("status:", manager.get_stats())

if __name__ == "__main__":
    main()
