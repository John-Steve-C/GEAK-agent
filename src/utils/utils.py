import re
import json
import ast

def extract_function_signatures(code, mode='triton'):
    function_defs = []
    pattern = r'def\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)'
    matches = re.finditer(pattern, code)
    
    for match in matches:
        func_name = match.group(1)
        params = match.group(2)
        
        if mode == 'tilelang':
            # TileLang does not support tl.constexpr annotations in function signatures.
            params = re.sub(r":\s*tl\.constexpr\b", "", params)
            params = re.sub(r"\s+,", ",", params)
        
        function_defs.append(f"def {func_name}({params})")
    
    # print("Extracted function signatures:", function_defs)
    return function_defs

def clear_code(code):
    if  "```python" in code:
        code = code.split("```python")[-1].replace("<|im_end|>", "").replace("<|EOT|>", "")
    if "```" in code:
        code = code.split("```")[0]
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
