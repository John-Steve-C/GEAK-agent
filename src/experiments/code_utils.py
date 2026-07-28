from __future__ import annotations

import ast
import json
from typing import Any, Optional, Tuple

from utils.utils import clear_code, clear_json


def parse_model_response(response: Any, dsl: str) -> Tuple[str, str]:
    text = str(response or "").strip()
    thought = ""
    code = ""
    try:
        parsed = clear_json(text)
        if isinstance(parsed, dict):
            thought = str(parsed.get("thought", ""))
            code = clear_code(str(parsed.get("code", "")))
    except Exception:
        decoder = json.JSONDecoder()
        for index, char in enumerate(text):
            if char != "{":
                continue
            try:
                parsed, _ = decoder.raw_decode(text[index:])
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                thought = str(parsed.get("thought", ""))
                code = clear_code(str(parsed.get("code", "")))
                break
        if not code:
            code = clear_code(text)
    if dsl == "tilelang":
        code = fix_tilelang_prim_func_indent(code)
    return thought, code


def fix_tilelang_prim_func_indent(code: str) -> str:
    def line_indent(line: str) -> int:
        return len(line) - len(line.lstrip())

    output = list(code.splitlines())
    index = 0
    while index < len(output):
        line = output[index]
        if line.lstrip().startswith("@T.prim_func"):
            indent = line[: len(line) - len(line.lstrip())]
            definition = index + 1
            while definition < len(output) and output[definition].strip() == "":
                definition += 1
            if definition < len(output) and output[definition].lstrip().startswith("def "):
                output[definition] = indent + output[definition].lstrip()
                paren_balance = output[definition].count("(") - output[definition].count(")")
                signature_end = definition
                while signature_end + 1 < len(output):
                    if paren_balance <= 0 and output[signature_end].rstrip().endswith(":"):
                        break
                    signature_end += 1
                    paren_balance += output[signature_end].count("(") - output[signature_end].count(")")

                for line_index in range(definition + 1, signature_end):
                    if output[line_index].strip():
                        output[line_index] = indent + "    " + output[line_index].lstrip()
                if signature_end > definition and output[signature_end].strip():
                    output[signature_end] = indent + output[signature_end].lstrip()

                body_start = signature_end + 1
                while body_start < len(output) and output[body_start].strip() == "":
                    body_start += 1
                if body_start < len(output) and line_indent(output[body_start]) <= len(indent):
                    body_end = body_start
                    while body_end < len(output):
                        stripped = output[body_end].strip()
                        if (
                            stripped
                            and line_indent(output[body_end]) <= len(indent)
                            and (
                                stripped == "return main"
                                or stripped.startswith(("@tl.jit", "@T.prim_func", "def ", "class "))
                            )
                        ):
                            break
                        body_end += 1
                    body_indents = [
                        line_indent(item) for item in output[body_start:body_end] if item.strip()
                    ]
                    min_body_indent = min(body_indents) if body_indents else 0
                    for line_index in range(body_start, body_end):
                        if output[line_index].strip():
                            relative_indent = max(
                                0, line_indent(output[line_index]) - min_body_indent
                            )
                            output[line_index] = (
                                indent
                                + "    "
                                + (" " * relative_indent)
                                + output[line_index].lstrip()
                            )
                    if body_end < len(output) and output[body_end].strip() == "return main":
                        output[body_end] = indent + output[body_end].lstrip()
                    index = body_end
                else:
                    index = signature_end
        index += 1
    return "\n".join(output)


def _strip_fenced_block(text: str, preferred_languages=()) -> Optional[str]:
    blocks = []
    start = 0
    while True:
        fence_start = text.find("```", start)
        if fence_start == -1:
            break
        language_start = fence_start + 3
        language_end = text.find("\n", language_start)
        if language_end == -1:
            break
        fence_end = text.find("```", language_end + 1)
        if fence_end == -1:
            break
        blocks.append(
            (text[language_start:language_end].strip().lower(), text[language_end + 1:fence_end])
        )
        start = fence_end + 3
    for language, body in blocks:
        if language in preferred_languages:
            return body
    return blocks[0][1] if blocks else None


def _parse_response_json(text: str):
    stripped = text.strip()
    fenced = _strip_fenced_block(stripped, preferred_languages=("json",))
    candidates = [stripped] if fenced is None else [fenced.strip(), stripped]
    decoder = json.JSONDecoder()
    for candidate in candidates:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass
        for index, character in enumerate(candidate):
            if character != "{":
                continue
            try:
                parsed, _ = decoder.raw_decode(candidate[index:])
                return parsed
            except json.JSONDecodeError:
                continue
    return None


def extract_response_code(response) -> str:
    if isinstance(response, dict):
        raw_code = response.get("code", "")
    else:
        text = str(response)
        parsed = _parse_response_json(text)
        if isinstance(parsed, dict) and "code" in parsed:
            raw_code = parsed["code"]
        else:
            raw_code = _strip_fenced_block(text, preferred_languages=("python", "py")) or text
    return fix_tilelang_prim_func_indent(clear_code(str(raw_code)))


def extract_run_test_tool_code(tool_call) -> str:
    name = tool_call.get("name") if isinstance(tool_call, dict) else getattr(tool_call, "name", None)
    if name != "run_test_and_get_perf":
        return ""
    args = tool_call.get("args", {}) if isinstance(tool_call, dict) else getattr(tool_call, "args", {})
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except json.JSONDecodeError:
            return ""
    return str(args.get("code") or "") if isinstance(args, dict) else ""


def _torch_call_name(node):
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "torch"
    ):
        return node.func.attr
    return None


def _torch_creation_call(node):
    current = node
    while isinstance(current, ast.Call):
        call_name = _torch_call_name(current)
        if call_name is not None:
            return current, call_name
        if isinstance(current.func, ast.Attribute) and isinstance(current.func.value, ast.Call):
            current = current.func.value
            continue
        break
    return None, None


def extract_test_shape_hints(test_code: str, max_items: int = 20) -> str:
    try:
        tree = ast.parse(test_code or "")
    except SyntaxError:
        return ""
    hints = []
    seen = set()
    simple_values = {}
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and not isinstance(node.value, ast.Call)
        ):
            simple_values[node.targets[0].id] = ast.unparse(node.value)
    creation_functions = {
        "empty", "zeros", "ones", "rand", "randn", "randint",
        "empty_like", "zeros_like", "ones_like", "full",
    }
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        targets = [target for target in node.targets if isinstance(target, ast.Name)]
        call_node, call_name = _torch_creation_call(node.value)
        if not targets or call_name not in creation_functions:
            continue
        if call_name == "randint":
            shape_node = call_node.args[2] if len(call_node.args) >= 3 else None
        else:
            shape_node = call_node.args[0] if call_node.args else None
        if shape_node is None:
            continue
        dtype = None
        for keyword in call_node.keywords:
            if keyword.arg == "dtype":
                dtype = ast.unparse(keyword.value)
                dtype = simple_values.get(dtype, dtype)
                break
        shape = f"{ast.unparse(shape_node)}.shape" if call_name.endswith("_like") else ast.unparse(shape_node)
        for target in targets:
            if target.id in seen:
                continue
            seen.add(target.id)
            hint = f"- {target.id}: shape={shape}"
            if dtype:
                hint += f", dtype={dtype}"
            hints.append(hint)
            if len(hints) >= max_items:
                return "\n".join(hints)
    return "\n".join(hints)


def classify_legacy_tilelang_result(result: dict) -> Optional[str]:
    pass_call = bool(result.get("pass_call"))
    pass_correctness = bool(result.get("pass_exe"))
    pass_performance = bool(result.get("pass_perf"))
    error_text = "\n".join(
        str(value)
        for value in (result.get("call_error"), result.get("exec_error"))
        if value not in (None, "", "None")
    ).lower()
    if pass_correctness and not pass_performance:
        return "Performance fail"
    if pass_performance or (pass_call and pass_correctness):
        return None
    if "empty model response" in error_text or "no code was returned" in error_text:
        return "Empty/parse failure"
    if (
        "object has no attribute '_inst'" in error_text
        and any(marker in error_text for marker in ("nestedloopcheckvisitor", "fragmentloopcheckvisitor"))
    ):
        return "TileLang environment error"
    if not pass_call:
        return "Compile / launch error"
    if any(marker in error_text for marker in ("mask", "boundary", "out of bounds", "stride")):
        return "Boundary failure"
    if any(marker in error_text for marker in ("does not match reference", "mismatch", "allclose")):
        return "Wrong answer"
    return "Runtime error"
