import numpy as np
import re
import ast
import json

from openai import OpenAI
from typing import List
from tenacity import retry, stop_after_attempt, wait_random_exponential
import os

# embedder = pipeline("feature-extraction", model="/shared/models/hf/jina-embeddings-v3", trust_remote_code=True)

# client = OpenAI(
#     base_url="http://localhost:8000/v1",
#     api_key="token-abc123",
#     timeout=None,
# )
_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is required for embedding-based retrieval")
        _client = OpenAI(api_key=api_key)
    return _client


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(5))
def get_embedding(text: str) -> List[float]:
    response = _get_client().embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    if not response or not hasattr(response, 'data') or len(response.data) == 0:
        raise ValueError("No embedding data returned from the API.")
    
    # convert to np array
    return np.array(response.data[0].embedding)

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(5))
def get_response(prompt: str, temperature=1) -> str:
    response = _get_client().chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert programming assistant.",
            },
            {
                "role": "user", 
                "content": prompt,
            },
        ],
        temperature=temperature,
        max_tokens=512,
    )
    if not response or not hasattr(response, 'choices') or len(response.choices) == 0:
        raise ValueError("No response choices returned from the API.")
    return response.choices[0].message.content

def cosine_sim(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Calculate the cosine similarity between two vectors."""
    assert len(vec_a) == len(vec_b), "Vectors must be the same length"
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

def _regex_split_triton_blocks(code: str):
    """
    当 ast.parse 失败时，用正则匹配 @triton.xxx 装饰的函数，
    尽可能提取 core 与 auxiliary。保持可逆性。
    """
    lines = code.splitlines()
    n = len(lines)
    # 模式匹配 @triton.xxx 以及紧接的 def
    # 捕获从装饰器开始直到下一个 def 或文件结束
    pattern = re.compile(
        r'(^\s*@triton\.[^\n]*\n\s*def\s+\w+\s*\([^)]*\)\s*:[\s\S]*?)(?=^\s*(?:@|def|class|\Z))',
        re.MULTILINE,
    )

    core_spans = []
    for match in pattern.finditer(code):
        start = code[: match.start()].count("\n")
        end = code[: match.end()].count("\n")
        # 向上扩展注释行
        i = start - 1
        while i >= 0 and (lines[i].strip().startswith("#") or lines[i].strip() == ""):
            i -= 1
        core_spans.append((i + 1, end))

    covered = set()
    for s, e in core_spans:
        covered.update(range(s, e))

    snippets = []
    for i, _ in enumerate(lines):
        if i not in covered:
            snippets.append((i, i + 1, "aux"))
    for s, e in core_spans:
        snippets.append((s, e, "core"))

    snippets.sort(key=lambda x: x[0])

    core_lines, aux_lines = [], []
    for s, e, cat in snippets:
        seg = "\n".join(lines[s:e])
        if cat == "core":
            core_lines.append(seg)
        else:
            aux_lines.append(seg)

    return {
        "core": "\n".join(core_lines) if core_lines else code,
        "auxiliary": "\n".join(aux_lines),
    }

def split_core_auxiliary(code: str):
    lines = code.splitlines()
    try:
        tree = ast.parse(code)
    except Exception:
        # 解析失败，直接把全部放 core 避免丢失
        # print("Warning: Error parsing code, returning full code as core.")
        # return {"core": code, "auxiliary": ""}
        # ret = _regex_split_triton_blocks(code)
        # print("Core: ", ret["core"])
        # print("Auxiliary: ", ret["auxiliary"])
        # print("Original: ", code)
        # print("==================================")
        return _regex_split_triton_blocks(code)
    
    def include_leading_comments(start_idx):
        """向上扩展，包含紧邻的注释行与空行"""
        i = start_idx - 1
        while i >= 0:
            line = lines[i].strip()
            if line.startswith("#") or line == "":
                i -= 1
            else:
                break
        return i + 1  # 返回第一个应包含的行号
    
    # 每个 snippet 记录：(start_line, end_line, category)
    snippets = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Try to locate decorator start
            if node.decorator_list:
                start = min(d.lineno for d in node.decorator_list) - 1
            else:
                start = node.lineno - 1
            end = getattr(node, "end_lineno", node.lineno)

            name_has_kernel = "kernel" in node.name.lower()

            # Detect @triton.xxx decorator
            has_triton_attr = any(
                (
                    isinstance(d, ast.Attribute)
                    and isinstance(d.value, ast.Name)
                    and d.value.id == "triton"
                )
                or (
                    isinstance(d, ast.Call)
                    and isinstance(d.func, ast.Attribute)
                    and isinstance(d.func.value, ast.Name)
                    and d.func.value.id == "triton"
                )
                for d in node.decorator_list
            )
            if has_triton_attr or name_has_kernel:
                start = include_leading_comments(start)
                snippets.append((start, end, "core"))
        
        elif isinstance(node, ast.ClassDef): 
            start = node.lineno - 1
            end = getattr(node, "end_lineno", node.lineno)
            name_has_kernel = "kernel" in node.name.lower()
            if name_has_kernel:
                start = include_leading_comments(start)
                snippets.append((start, end, "core"))

        # else:  #  ast.Import, ast.ImportFrom
        #     snippets.append((node.lineno - 1, node.end_lineno, "aux"))

    # 记录所有覆盖行
    covered = set()
    for s, e, _ in snippets:
        covered.update(range(s, e))

    # 把未覆盖的行也补到 auxiliary
    for i, _ in enumerate(lines):
        if i not in covered:
            snippets.append((i, i + 1, "aux"))

    # 按行号排序保持原顺序
    snippets.sort(key=lambda x: x[0])

    core_lines, aux_lines = [], []
    for s, e, cat in snippets:
        segment = "\n".join(lines[s:e])
        if cat == "core":
            core_lines.append(segment)
        else:
            aux_lines.append(segment)
    
    return {
        "core": "\n".join(core_lines) if core_lines else code,  # 避免 core 为空
        "auxiliary": "\n".join(aux_lines),
    }

# def split_core_auxiliary(code: str):
#     try:
#         tree = ast.parse(code)
#     except Exception as e:
#         # print("Error parsing code:", e)

#         # fallback: regex 提取
#         # pattern = re.compile(r"(@[^\n]+\n\s*)*(def|class)\s+\w+\(.*\):")
#         # core, auxiliary = [], []
#         # for match in pattern.finditer(code):
#         #     snippet = match.group(0)
#         #     if "@triton.jit" in snippet:
#         #         core.append(snippet)
#         #     else:
#         #         auxiliary.append(snippet)
#         # # 如果 regex 什么都没提取到，把代码全放 core，避免丢失
#         # if not core and not auxiliary:
#         #     core.append(code)
#         # return {"core": "\n".join(core), "auxiliary": "\n".join(auxiliary)}
#         return {"core": code, "auxiliary": ""}

#     core, auxiliary = [], []
#     lines = code.splitlines()

#     for node in tree.body:
#         if isinstance(node, ast.FunctionDef):
#             # decorator 起点
#             if node.decorator_list:
#                 start = min(d.lineno for d in node.decorator_list) - 1
#             else:
#                 start = node.lineno - 1
#             func_code = "\n".join(lines[start: node.end_lineno])
            
#             # 判断是否有 @triton.xxx
#             has_triton_attr = any(
#                 isinstance(d, ast.Attribute) and isinstance(d.value, ast.Name) and d.value.id == "triton" # and d.attr == "jit"
#                 for d in node.decorator_list
#             )
#             if has_triton_attr:
#                 core.append(func_code)
#             else:
#                 auxiliary.append(func_code)

#         elif isinstance(node, ast.ClassDef):
#             class_code = "\n".join(lines[node.lineno-1: node.end_lineno])
#             auxiliary.append(class_code)

#         elif isinstance(node, (ast.Import, ast.ImportFrom)):
#             imp_code = "\n".join(lines[node.lineno-1: node.end_lineno])
#             auxiliary.append(imp_code)

#     return {"core": "\n".join(core), "auxiliary": "\n".join(auxiliary)}


# def split_core_auxiliary(code: str):
#     """
#     Split input python code into core and auxiliary parts.
    
#     Args:
#         code (str): full python code as a string
    
#     Returns:
#         dict: {"core": str, "auxiliary": str}
#     """
#     lines = code.splitlines()
#     core_lines = []
#     aux_lines = []

#     in_core = False
#     prev_line = ""

#     for line in lines:
#         # 检测到 @triton.jit 装饰器
#         if re.search(r'@triton\.jit', line.strip()) or re.search(r'class', line.strip()):
#             in_core = True
#             core_lines.append(line)
#         # 检测到 def 开始
#         elif in_core and re.match(r'\s*def\s+\w+', line) and prev_line.strip().startswith("@triton.jit"):
#             core_lines.append(line)
#         elif in_core:
#             # 如果还在 core 函数体内
#             if line.strip().startswith("def ") and not prev_line.strip().startswith("@triton.jit"):
#                 # 新的非kernel函数，退出 core 区域
#                 in_core = False
#                 aux_lines.append(line)
#             else:
#                 core_lines.append(line)
#         else:
#             aux_lines.append(line)

#         prev_line = line
        
#     return {
#         "core": "\n".join(core_lines).strip(),
#         "auxiliary": "\n".join(aux_lines).strip()
#     }

def split_core_auxiliary_llm(code: str):
    """
    Use LLM to split input python code into core and auxiliary parts.
    
    Args:
        code (str): full python code as a string
    """

    prompt = f"""\
You are a helpful assistant that extracts the core logic snippet from Python triton code.
Given the following Python code, extract the core logic that is directly related to triton kernels and their execution.
Return the core logic and auxiliary code separately in JSON format with keys "core" and "auxiliary".
Here is the code:
```
{code}
```
Respond in the following JSON format:
{{
"core": core logic snippet here,
"auxiliary": auxiliary code here"
}}
Make sure the JSON is properly formatted.
"""

    response = get_response(prompt, temperature=0)
    print(response)
    # filter the ```json ... ```
    pattern = r"```json\s*(.*?)\s*```"
    match = re.search(pattern, response, re.DOTALL)
    if match:
        text = match.group(1).strip()
    print(text)
    ret = json.loads(text)
    return ret


from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def parse_corpus(content_input_path: str):
    with open(content_input_path, "r", encoding="utf-8") as f:
        content = json.load(f)
    print('Original total number: ', len(content))
    corpus = []
    chunks = []

    def process_item(c):
        """处理单条内容，返回 description 和 code 的 embedding"""
        desc_emb = get_embedding(c["description_1"])
        code_emb = get_embedding(c["code"])
        return desc_emb, code_emb
    
    results = [None] * len(content)
    with ThreadPoolExecutor(max_workers=32) as executor:
        # 提交所有任务
        # futures = [executor.submit(process_item, c) for c in content]
        # # tqdm 显示进度，但是乱序保存
        # for f in tqdm(as_completed(futures), total=len(futures)):
        #     desc_emb, code_emb = f.result()
        #     corpus.append(desc_emb)
        #     chunks.append(code_emb)

        def wrapper(i, c):
            desc_emb, code_emb = process_item(c)  # 保持 process_item 不变
            return i, desc_emb, code_emb
        # 额外传入 index 以便后续排序
        futures = [executor.submit(wrapper, i, c) for i, c in enumerate(content)]

        for f in tqdm(as_completed(futures), total=len(futures), desc="Embedding corpus and codes"):
            i, desc_emb, code_emb = f.result()
            results[i] = (desc_emb, code_emb)       # 按顺序保存
    
    # 最后恢复顺序
    corpus = [r[0] for r in results]
    chunks = [r[1] for r in results]

    with open("parsed_corpus_embeddings_ordered.json", "w", encoding="utf-8") as f:
        json.dump({"corpus_text": [c.tolist() for c in corpus], "chunks_code": [c.tolist() for c in chunks]}, f, indent=4)

# remove duplicate items in core_code and aux_code
def parse_split_code(content_input_path: str):
    with open(content_input_path, "r", encoding="utf-8") as f:
        content = json.load(f)
    print('Original total number: ', len(content))
    core_code = []
    aux_code = []
    for c in content:
        split_res = split_core_auxiliary(c["code"])
        # 去重
        if split_res["core"] not in core_code and split_res["core"].strip():
            core_code.append(split_res["core"])
        if split_res["auxiliary"] not in aux_code and split_res["auxiliary"].strip():
            aux_code.append(split_res["auxiliary"])
    
    print('After split total number: ', len(core_code), len(aux_code))

    def embed_core(core):
        return get_embedding(core)

    def embed_aux(aux):
        return get_embedding(aux)

    core_results = [None] * len(core_code)
    with ThreadPoolExecutor(max_workers=32) as executor:
        futures = {executor.submit(embed_core, c): i for i, c in enumerate(core_code)}
        for f in tqdm(as_completed(futures), total=len(futures), desc="Embedding core"):
            i = futures[f]
            core_results[i] = f.result()

    aux_results = [None] * len(aux_code)
    with ThreadPoolExecutor(max_workers=32) as executor:
        futures = {executor.submit(embed_aux, c): i for i, c in enumerate(aux_code)}
        for f in tqdm(as_completed(futures), total=len(futures), desc="Embedding aux"):
            i = futures[f]
            aux_results[i] = f.result() if aux_code[i].strip() else np.zeros_like(core_results[0])
    
    print(len(core_results), len(aux_results))

    with open("parsed_corpus_embeddings_split_ordered.json", "w", encoding="utf-8") as f:
        json.dump({"core_embed": [c.tolist() for c in core_results], "aux_embed": [c.tolist() for c in aux_results],
                   "core_code": core_code, "aux_code": aux_code}, f, indent=4)

# keep all items in core_code and aux_code, and also maintain the original order
def parse_ordered_split_code(content_input_path: str):
    with open(content_input_path, "r", encoding="utf-8") as f:
        content = json.load(f)
    print('Original total number: ', len(content))
    corpus = []
    chunks = []

    def process_item(c):
        ret = split_core_auxiliary(c["code"])
        core_emb = get_embedding(ret["core"])
        aux_emb = get_embedding(ret["auxiliary"])
        return core_emb, aux_emb, ret["core"], ret["auxiliary"]
    
    results = [None] * len(content)
    with ThreadPoolExecutor(max_workers=32) as executor:
        # 提交所有任务
        # futures = [executor.submit(process_item, c) for c in content]
        # # tqdm 显示进度，但是乱序保存
        # for f in tqdm(as_completed(futures), total=len(futures)):
        #     desc_emb, code_emb = f.result()
        #     corpus.append(desc_emb)
        #     chunks.append(code_emb)

        def wrapper(i, c):
            core_emb, aux_emb, core_code, aux_code = process_item(c)  # 保持 process_item 不变
            return i, core_emb, aux_emb, core_code, aux_code
        # 额外传入 index 以便后续排序
        futures = [executor.submit(wrapper, i, c) for i, c in enumerate(content)]

        for f in tqdm(as_completed(futures), total=len(futures), desc="Embedding corpus and codes"):
            i, core_emb, aux_emb, core_code, aux_code = f.result()
            results[i] = (core_emb, aux_emb, core_code, aux_code)       # 按顺序保存
    
    # 最后恢复顺序
    cores = [r[0] for r in results]
    auxs = [r[1] for r in results]
    core_codes = [r[2] for r in results]
    aux_codes = [r[3] for r in results]

    with open("parsed_corpus_embeddings_split_ordered_whole.json", "w", encoding="utf-8") as f:
        json.dump({"core_embed": [c.tolist() for c in cores], "aux_embed": [c.tolist() for c in auxs],
                   "core_code": core_codes, "aux_code": aux_codes}, f, indent=4)


if __name__ == "__main__":
    code = "import triton\nimport triton.language as tl\n\n# triton kernel\n@triton.jit\ndef kernel(X, stride_xm,\n           Z, stride_zn,\n           BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr):\n    off_m = tl.arange(0, BLOCK_M)\n    off_n = tl.arange(0, BLOCK_N)\n    Xs = X + off_m[:, None] * stride_xm + off_n[None, :] * 1\n    Zs = Z + off_m[:, None] * 1 + off_n[None, :] * stride_zn\n    tl.store(Zs, tl.load(Xs))\n\n\nret = triton.compile(kernel, signature=\"*fp32,i32,*fp32,i32\", constants={\"BLOCK_M\": 64, \"BLOCK_N\": 64}, output=\"ttgir\")\n\nprint(ret)\n"
    # embed = get_embedding(code)
    # print(embed)

    # parse_corpus("/home/wentao/GEAK-agent/src/dataloaders/TB_eval/train_crawl.json")
    # parse_split_code("/home/wentao/GEAK-agent/src/dataloaders/TB_eval/train_crawl.json")
    # parse_ordered_split_code("/home/wentao/GEAK-agent/src/dataloaders/TB_eval/train_crawl.json")

    ret = split_core_auxiliary_llm(code)
    print("Core: ", ret["core"])
    print("Auxiliary: ", ret["auxiliary"])

    # with open("parsed_corpus_embeddings.json", "r", encoding="utf-8") as f:
    #     parsed_embedding = json.load(f)
    # print(parsed_embedding.keys())

    # with open("/home/wentao/GEAK-agent/src/dataloaders/TB_eval/train_crawl.json", "r", encoding="utf-8") as f:
    #     data = json.load(f)
    # for i in range(4024):
    #     core, aux = split_core_auxiliary(data[i]["code"]).values()
    #     if core == "" or aux == "":
    #         print(f"Empty at index {i}:")
    #         print("Core:\n", core)
    #         print("Auxiliary:\n", aux)
    #         print("Original:\n", data[i]["code"])
    #         print("==================")
            # input("Press Enter to continue...")
    #     print("==================")
    #     print("Core:\n", core)
    #     print("Auxiliary:\n", aux)
    #     print("Original:\n", data[i]["code"])
    #     print("==================")
    #     input("Press Enter to continue...")

    # clear empty items

    # with open("parsed_corpus_embeddings_split_ordered.json", "r", encoding="utf-8") as f:
    #     data = json.load(f)

    # core_code = data["core_code"]
    # core_embed = data["core_embed"]
    # print(len(core_code), len(core_embed))

    # # 保留 core_code 非空的条目
    # filtered_core_code = []
    # filtered_core_embed = []

    # for code, emb in zip(core_code, core_embed):
    #     if code.strip():  # 过滤掉空字符串
    #         filtered_core_code.append(code)
    #         filtered_core_embed.append(emb)

    # # 更新数据
    # data["core_code"] = filtered_core_code
    # data["core_embed"] = filtered_core_embed

    # print(len(filtered_core_code), len(filtered_core_embed))

    # with open("parsed_corpus_embeddings_split_ordered.json", "w", encoding="utf-8") as f:
    #     json.dump(data, f, indent=4, ensure_ascii=False)
