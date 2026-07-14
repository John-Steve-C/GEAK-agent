import re
import json
import ast
import codecs

def _split_params(params):
    parts = []
    current = []
    depth = 0
    for char in params:
        if char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        elif char == "," and depth == 0:
            part = "".join(current).strip()
            if part:
                parts.append(part)
            current = []
            continue
        current.append(char)
    part = "".join(current).strip()
    if part:
        parts.append(part)
    return parts

def _clean_tilelang_signature(signature):
    signature = re.sub(r":\s*['\"]?tl\.constexpr['\"]?", "", signature)
    signature = re.sub(r":\s*['\"]?triton\.language\.constexpr['\"]?", "", signature)
    signature = re.sub(r"\s+,", ",", signature)
    return signature

def _format_arg(name, default=None):
    if default is None:
        return name
    return f"{name}={default}"

def _format_function_signature(node, name_override=None, drop_first_param=False):
    args = node.args
    positional_args = list(args.posonlyargs) + list(args.args)
    positional_defaults = [None] * (len(positional_args) - len(args.defaults))
    positional_defaults += [ast.unparse(default) for default in args.defaults]

    params = [
        _format_arg(arg.arg, default)
        for arg, default in zip(positional_args, positional_defaults)
    ]

    if args.vararg is not None:
        params.append(f"*{args.vararg.arg}")
    elif args.kwonlyargs:
        params.append("*")

    for arg, default in zip(args.kwonlyargs, args.kw_defaults):
        params.append(_format_arg(arg.arg, ast.unparse(default) if default is not None else None))

    if args.kwarg is not None:
        params.append(f"**{args.kwarg.arg}")

    if drop_first_param and params:
        params = params[1:]

    name = name_override or node.name
    return f"def {name}({', '.join(params)})"

def _signature_from_node(code, node, name_override=None, drop_first_param=False):
    if node is None:
        return None
    return _format_function_signature(
        node,
        name_override=name_override,
        drop_first_param=drop_first_param,
    )

def _class_header_from_node(code, node):
    segment = ast.get_source_segment(code, node)
    if not segment:
        return None
    start = segment.find("class ")
    if start == -1:
        return None
    end = segment.find(":", start)
    if end == -1:
        return None
    return segment[start:end].strip()

def _called_public_apis(test_code):
    tree = ast.parse(test_code)
    calls = []
    class_apply_calls = []

    class Visitor(ast.NodeVisitor):
        def visit_Call(self, node):
            if isinstance(node.func, ast.Name):
                calls.append(node.func.id)
            elif (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "apply"
                and isinstance(node.func.value, ast.Name)
            ):
                class_apply_calls.append(node.func.value.id)
            self.generic_visit(node)

    Visitor().visit(tree)
    return calls, class_apply_calls

def _extract_tilelang_signatures(code, test_code=None):
    tree = ast.parse(code)
    top_functions = {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    classes = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    }
    apply_aliases = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not (
            isinstance(node.value, ast.Attribute)
            and node.value.attr == "apply"
            and isinstance(node.value.value, ast.Name)
        ):
            continue
        class_name = node.value.value.id
        for target in node.targets:
            if isinstance(target, ast.Name):
                apply_aliases[target.id] = class_name

    signatures = []
    seen = set()

    def add_signature(signature):
        if not signature:
            return
        signature = _clean_tilelang_signature(signature)
        if signature not in seen:
            signatures.append(signature)
            seen.add(signature)

    def add_autograd_class(class_name, alias_name=None):
        class_node = classes.get(class_name)
        if class_node is None:
            return
        methods = {
            item.name: item
            for item in class_node.body
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        forward = methods.get("forward")
        if alias_name is not None and forward is not None:
            add_signature(_signature_from_node(code, forward, name_override=alias_name, drop_first_param=True))
        add_signature(_class_header_from_node(code, class_node))
        for method_name in ("forward", "backward"):
            add_signature(_signature_from_node(code, methods.get(method_name)))

    if test_code:
        try:
            called_names, class_apply_calls = _called_public_apis(test_code)
        except SyntaxError:
            called_names, class_apply_calls = [], []

        for name in called_names:
            if name in top_functions:
                add_signature(_signature_from_node(code, top_functions[name]))
            elif name in apply_aliases:
                add_autograd_class(apply_aliases[name], alias_name=name)

        for class_name in class_apply_calls:
            add_autograd_class(class_name)

        if signatures:
            return signatures

    for node in top_functions.values():
        add_signature(_signature_from_node(code, node))
    for class_name in classes:
        add_autograd_class(class_name)
    return signatures

def extract_function_signatures(code, mode='triton', test_code=None):
    function_defs = []
    if mode == 'tilelang':
        try:
            return _extract_tilelang_signatures(code, test_code=test_code)
        except SyntaxError:
            pass

    pattern = r'def\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)'
    matches = re.finditer(pattern, code)
    
    for match in matches:
        func_name = match.group(1)
        params = match.group(2)
        
        if mode == 'tilelang':
            # TileLang does not support tl.constexpr annotations in function signatures.
            params = _clean_tilelang_signature(params)
        
        function_defs.append(f"def {func_name}({params})")
    
    # print("Extracted function signatures:", function_defs)
    return function_defs

def _strip_wrapped_code_string(code):
    stripped = code.strip()
    if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in ("'", '"'):
        try:
            parsed = ast.literal_eval(stripped)
            if isinstance(parsed, str):
                return parsed
        except (SyntaxError, ValueError):
            unwrapped = stripped[1:-1]
            try:
                return codecs.decode(unwrapped, "unicode_escape")
            except UnicodeDecodeError:
                return unwrapped.replace("\\n", "\n").replace("\\t", "\t")
    return code

def clear_code(code):
    # if code is None:
    #     return ""
    # if type(code) is not str:
    #     code = str(code)
    # code = _strip_wrapped_code_string(code.strip())
    if  "```python" in code:
        code = code.split("```python")[-1].replace("<|im_end|>", "").replace("<|EOT|>", "")
    if "```" in code:
        code = code.split("```")[0]
    # code = _strip_wrapped_code_string(code.strip())
    return code

def extract_function_calls(code):
    calls = []
    pattern = r'([a-zA-Z0-9_]+)\s*\(([^)]*)\)'
    matches = re.finditer(pattern, code)
    
    for match in matches:
        func_name = match.group(1)
        args = match.group(2)
        calls.append(f"{func_name}({args})")
    
    return calls

def clear_json(response):
    if type(response) is dict:
        return response
    elif type(response) is not str:
        response = str(response)
    try:
        response = response.replace("\n", " ")
        response = re.search('({.+})', response).group(0)
        response = re.sub(r"(\w)'(\w|\s)", r"\1\\'\2", response)
        result = ast.literal_eval(response)
    except (SyntaxError, NameError, AttributeError):
        return "ERR_SYNTAX"
    return result
