import ast
import os
import subprocess
from random import randint
from tqdm import tqdm
from shutil import copyfile
import datetime
import json
import numpy as np
import re

## Implementation from https://arxiv.org/pdf/2107.03374
def passk(n, c, k):
    if n -c < k: return 1.0
    return 1 - np.prod(
        1 - k/ np.arange(
            n-c+1, n+1
        )
    )

def get_time():
    # Get the current time in the format YYYY-MM-DD_HH-MM-SS
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def get_temp_file(prefix='temp_code'):
    # Generate a unique temporary file name
    temp_file_name = f'{prefix}_{randint(999, 999999)}.py'
    while os.path.exists(temp_file_name):
        temp_file_name.replace('.py', f'_{randint(999, 999999)}.py')
    return temp_file_name

def code_call_exec_success_stdout(code, fname, temp_root="tmp2", tolerance=2, verbose=False):
    # Save the code to a temporary file
    tmp_triton_folder = os.path.join(temp_root, "triton") #f"{temp_root}_triton"
    tmp_gen_folder = os.path.join(temp_root, "gen") #f"{temp_root}_gen"
    os.makedirs(tmp_triton_folder, exist_ok=True)
    os.makedirs(tmp_gen_folder, exist_ok=True)
    

    triton_root = "dataloaders/TB_eval/TritonBench/data/TritonBench_G_v1"
    RAND_FILE = os.path.join(triton_root, "rand_utils.py")

    copyfile(RAND_FILE, os.path.join(tmp_triton_folder, "rand_utils.py"))
    copyfile(RAND_FILE, os.path.join(tmp_gen_folder, "rand_utils.py"))

    gen_file = get_temp_file(prefix=f'{fname}_gen_triton_code')
    triton_file = os.path.join(triton_root, fname)
    temp_triton_file = get_temp_file(prefix=f'{fname}_temp_triton')

    gen_file = os.path.join(tmp_gen_folder, gen_file)
    temp_triton_file = os.path.join(tmp_triton_folder, temp_triton_file)

    IMPORT_STATEMENT = f"""
from rand_utils import torch_rand, torch_randint, torch_randn
import torch
torch.set_printoptions(precision={tolerance},profile='full',sci_mode=False)
"""

    hash_line = "#"*146
    ## from triton_file copy everything after the hash_line into gen_file
    with open(triton_file, 'r') as f:
        lines = f.readlines()
        # lines.append(
        #     '\nprint(result_gold)'
        # )
        for iL, line in enumerate(lines):
            if line.strip() == hash_line:
                break
        test_code_lines = lines[iL+1:]
        test_code_lines = IMPORT_STATEMENT.split('\n') + test_code_lines
        test_code_lines_procs = []
        for line in test_code_lines:
            if "torch.rand" in line:
                line = line.replace("torch.rand", "torch_rand")
            test_code_lines_procs.append(line)

    with open(temp_triton_file, 'w') as f:
        triton_lines = lines[:iL] +  [hash_line] + test_code_lines_procs
        for line in triton_lines:
            f.write(line + "\n")

    code =  code + '\n\n' + hash_line + '\n' + '\n' + '\n'.join(test_code_lines_procs)
    with open(gen_file, 'w') as f:
        f.write(code)

    ## Execute two codes gen_file and triton_file using subprocess. 
    ## 1. If gen_file return error then return status as False, and stdout and stderr from gen file
    ## 2. If triton_file return error then return status as True and stdout and stderr as None
    ## 3. If gen_file and triton_file both return success then compare stdout from gen_file and triton_file. If stdout matches then return status as True, and stdout and stderr as None else return status as False and stdout and stderr as test cases mismatched.

    try:
        # Execute the generated code
        result_gen = subprocess.run(['python3', gen_file], capture_output=True, text=True, timeout=2*60)
        stdout_gen = result_gen.stdout
        stderr_gen = result_gen.stderr

        # Check if the generated code executed successfully
        if result_gen.returncode != 0:
            if verbose:
                print(f"Error in generated code: {stderr_gen}")
            return False, False, stdout_gen, stderr_gen

        # Execute the Triton code
        result_triton = subprocess.run(['python3', temp_triton_file], capture_output=True, text=True, timeout=2*60)
        stdout_triton = result_triton.stdout
        stderr_triton = result_triton.stderr

        # Check if the Triton code executed successfully
        if result_triton.returncode != 0:
            if verbose:
                print(f"Error in Triton code: {stderr_triton}")
            return None, None, None, None

        with open(gen_file+".out", 'w') as f:
            f.write(stdout_gen)
        with open(temp_triton_file+".out", 'w') as f:
            f.write(stdout_triton)

        with open(gen_file+".err", 'w') as f:
            f.write(stderr_gen)
        with open(temp_triton_file+".err", 'w') as f:
            f.write(stderr_triton)

        # Compare the outputs
        if stdout_gen == stdout_triton:
            return True, True, None, None
        else:
            return True, False, stdout_gen, "Error: not all test cases passed. The generated code and ground truth code produced different outputs."
    except Exception as e:
        if verbose:
            print(f"File: {fname}, Execution error: {e}")
        return False, False, None, str(e)
    # Clean up the temporary file
    except subprocess.TimeoutExpired:
        if verbose:
            print(f"File: {fname} timed out!")
        return None, None, None, "Time out"
    finally:
        pass
        # print(f"temp file for File: {fname} removed!")
        # if os.path.exists(gen_file):
        #     os.remove(gen_file)
    return False, False, None, None

def extract_code_from_llm_output(response):
    # Extract code blocks from the LLM response
    code = None
    if "```" not in response:
        return response
    from parse_llm_code import extract_code_blocks
    code_blocks = extract_code_blocks(response)
    for _code in code_blocks.code_dict_list:
        code += _code['context'] + "\n"
    return code

def get_fname_difficulty_from_label(label):
    triton_root = "dataloaders/TB_eval/TritonBench/data/TritonBench_G_comp_alpac_v1_fixed_with_difficulty.json"
    with open(triton_root, 'r') as f:
        data = json.load(f)
        for item in data:
            if item['output'] == label:
                return item['file'], item['difficulty']
    return None, None

def process_code(code: str):
    if "```python" in code:
        code = code.split("```python")[-1].replace("<|im_end|>", "").replace("<|EOT|>", "")
    
    try:
        tree = ast.parse(code)
        imports = []
        function_definitions = []

        # Traverse the AST to find import statements and function definitions
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                # Collect the import statements
                imports.append(ast.unparse(node))  # Convert the AST node back to code
            elif isinstance(node, ast.FunctionDef):
                # Collect function definitions
                function_code = ast.unparse(node)  # Get the Python code for the function
                function_definitions.append(function_code)

        return "\n".join(imports) + "\n\n" + "\n".join(function_definitions)

    except:
        return code


def code_call_exec_success_allclose(code, fname, py_folder, temp_root="tmp2", atol=1e-3, rtol=1e-1, timeout=2*60, verbose=False):
    tmp_gen_folder = os.path.join(temp_root, "gen")
    os.makedirs(tmp_gen_folder, exist_ok=True)
    
    triton_root = py_folder
    triton_file = os.path.join(triton_root, fname)

    gen_file = get_temp_file(prefix=f'{fname}_gen_triton_code')
    gen_file = os.path.join(tmp_gen_folder, gen_file)

    hash_line = "#"*146

    with open(triton_file, 'r') as f:
        lines = f.readlines()
        for iL, line in enumerate(lines):
            if line.strip() == hash_line:
                break
        test_code_lines = lines[iL+1:]
        test_code_lines_procs = test_code_lines

    # code = process_code(code)

    code =  code + '\n\n' + hash_line + '\n' + '\n' + '\n'.join(test_code_lines_procs)

    with open(gen_file, 'w') as f:
        f.write(code)

    try:
        ## Just to a simple call to the generated code
        result_call = subprocess.run([f'python3 {gen_file}'], capture_output=True, text=True, timeout=timeout, shell=True)
        call_status = result_call.returncode == 0

        # Check for correctness
        result_corr = subprocess.run([f'python3 /home/wentao/GEAK-agent/src/dataloaders/TB_eval/correctness.py --gen_file {gen_file} --ref_file {triton_file} --atol {atol} --rtol {rtol}'], capture_output=True, text=True, timeout=timeout, shell=True)
        stdout_corr = result_corr.stdout
        stderr_corr = result_corr.stderr

    except Exception as e:
        if verbose:
            print(f"File: {fname}, Execution error: {e}")
        return None, None, None, str(e), None, None
    
    # Clean up the temporary file
    except subprocess.TimeoutExpired:
        if verbose:
            print(f"File: {fname} timed out!")
        return None, None, None, "Time out", None, None
    finally:
        pass

    with open(gen_file+".stdout", 'w') as f:
        f.write(stdout_corr)

    with open(gen_file+".stderr", 'w') as f:
        f.write(stderr_corr)

    # Check if the generated code executed successfully
    if result_corr.returncode != 0:
        if verbose:
            print(f"Error in generated code: {stderr_corr}")
        return call_status, None, result_call.stdout, result_call.stderr, stdout_corr, stderr_corr
    else:
        if verbose:
            print(f"Success in generated code: {stdout_corr}")
        _, exec_status, gen_stdout, gen_stderr = stdout_corr.split("*#*#")
        return call_status, exec_status, result_call.stdout, result_call.stderr, gen_stdout, gen_stderr

def _is_missing_tilelang_error(stderr: str) -> bool:
    if not stderr:
        return False
    stderr_lower = stderr.lower()
    return "modulenotfounderror" in stderr_lower and "tilelang" in stderr_lower


_TILELANG_FORBIDDEN_APIS = {
    "T.if_scope": "use a normal `if` statement inside `@T.prim_func`, or `T.if_then_else` for expression selection",
    "T.Assume": "use `T.assume`",
    "T.get_block_id": "use the variable bound by `with T.Kernel(...) as bid`, or `T.get_block_binding(0)`",
    "T.cdiv": "use `T.ceildiv`",
    "T.constant": "use a Python literal such as `0`, or `T.cast(0, dtype)`",
    "T.any": "use concrete dimensions captured by `@tl.jit`",
    "T.unary": "use the explicit TileLang math primitive, such as `T.sqrt`, `T.exp`, or `T.log`",
    "T.Cast": "use `T.cast(value, dtype)` or `value.astype(dtype)`",
}

def _is_decorated_with(node, value_name, attr_name):
    return any(
        isinstance(decorator, ast.Attribute)
        and decorator.attr == attr_name
        and isinstance(decorator.value, ast.Name)
        and decorator.value.id == value_name
        for decorator in node.decorator_list
    )

def _is_t_call(node, attr_name):
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == attr_name
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "T"
    )

def _contains_name(node, name):
    return any(isinstance(child, ast.Name) and child.id == name for child in ast.walk(node))

def _buffer_rank_from_annotation(annotation):
    if not _is_t_call(annotation, "Buffer") or not annotation.args:
        return None
    shape = annotation.args[0]
    if isinstance(shape, ast.Tuple):
        return len(shape.elts)
    return None

def _subscript_rank(slice_node):
    if isinstance(slice_node, ast.Tuple):
        return len(slice_node.elts)
    return 1

def lint_tilelang_code_for_eval(code):
    errors = []

    def add_error(error):
        if error not in errors:
            errors.append(error)

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [f"SyntaxError before execution: {e}"]

    for api, replacement in _TILELANG_FORBIDDEN_APIS.items():
        if api in code:
            add_error(f"Unsupported TileLang API `{api}`; {replacement}.")

    if re.search(r"\bT\.if_then\s*\(", code):
        add_error("Unsupported TileLang API `T.if_then`; use `T.if_then_else`.")

    if ".dtype.name" in code:
        add_error("Do not use `torch.dtype.name`; pass TileLang dtype strings such as `str(x.dtype).replace('torch.', '')` outside `@tl.jit`.")

    if re.search(r"str\s*\([^)]*\.dtype\s*\)\s*\.lower\s*\(", code):
        add_error("Do not use `str(tensor.dtype).lower()` for TileLang dtypes; remove the `torch.` prefix with `.replace('torch.', '')` or `.split('.')[-1]`.")

    if re.search(r"str\s*\([^)]*\.dtype\s*\)(?!\s*\.(replace|split))", code):
        add_error("Do not pass raw `str(tensor.dtype)` to TileLang; use dtype strings such as `str(x.dtype).replace('torch.', '')`.")

    if re.search(r"T\.Buffer\s*\([^)]*None", code, re.S):
        add_error("Do not use `None` in `T.Buffer` shapes; capture concrete runtime dimensions in the private `@tl.jit` factory.")

    if re.search(r"T\.Buffer\s*\(\s*\(\s*-1", code):
        add_error("Do not use `-1` in `T.Buffer` shapes; capture concrete runtime dimensions in the private `@tl.jit` factory.")

    if "T.Any" in code:
        add_error("Do not use `T.Any` in generated `T.Buffer` shapes; use concrete dimensions captured by `@tl.jit`.")

    if re.search(r"T\.Buffer\s*\(.*?T\.int(?:32|64)\s*(?:\(\s*\))?", code, re.S):
        add_error("Do not use `T.int32` or `T.int64` as generated `T.Buffer` dimensions; use concrete dimensions captured by `@tl.jit`.")

    if re.search(r"T\.Buffer\s*\([^)]*(typing\.Optional|Optional\s*\[)", code, re.S):
        add_error("Do not use Python typing objects such as `Optional[...]` inside TileLang buffer/dtype declarations.")

    if re.search(r"[-+]?3\.40282[0-9]*e\+?38", code):
        add_error("Do not use boundary float32 literals such as `3.402823e+38`; use `T.infinity('float32')` or a smaller finite sentinel.")

    prim_func_names = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and _is_decorated_with(node, "T", "prim_func")
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in prim_func_names:
            add_error(f"Do not call `@T.prim_func` function `{node.func.id}` directly; return it from a private `@tl.jit` factory and call the compiled factory result.")

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        is_tl_jit = _is_decorated_with(node, "tl", "jit")
        is_prim_func = _is_decorated_with(node, "T", "prim_func")
        args = list(node.args.posonlyargs) + list(node.args.args) + list(node.args.kwonlyargs)

        if is_tl_jit:
            arg_names = {arg.arg for arg in args}
            for arg in args:
                if arg.annotation is None:
                    continue
                annotation = ast.unparse(arg.annotation)
                if "torch.Tensor" in annotation:
                    add_error(
                        f"`@tl.jit` function `{node.name}` has tensor parameter `{arg.arg}`; public tensor wrappers must be plain Python functions and private `@tl.jit` factories should take only compile-time values."
                    )
                    break
            for child in ast.walk(node):
                if (
                    isinstance(child, ast.Attribute)
                    and child.attr in {"shape", "dtype", "device", "stride", "ndim", "dim"}
                    and isinstance(child.value, ast.Name)
                    and child.value.id in arg_names
                ):
                    add_error(
                        f"`@tl.jit` function `{node.name}` reads `{child.value.id}.{child.attr}`; derive tensor metadata in the public Python wrapper and pass only compile-time values to the TileLang factory."
                    )
                    break
            for child in ast.walk(node):
                if child is not node and isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and _is_decorated_with(child, "tl", "jit"):
                    add_error(f"Do not nest `@tl.jit` function `{child.name}` inside `@tl.jit` function `{node.name}`.")
                    break

        if is_prim_func:
            buffer_ranks = {
                arg.arg: _buffer_rank_from_annotation(arg.annotation)
                for arg in args
                if arg.annotation is not None and _buffer_rank_from_annotation(arg.annotation) is not None
            }

            class PrimFuncVisitor(ast.NodeVisitor):
                def __init__(self):
                    self.kernel_depth = 0
                    self.serial_depth = 0

                def visit_With(self, with_node):
                    is_kernel = any(_is_t_call(item.context_expr, "Kernel") for item in with_node.items)
                    if is_kernel and self.kernel_depth:
                        add_error("Do not nest `with T.Kernel(...)` blocks; use a single `T.Kernel` with multiple grid dimensions or flatten the grid.")
                    if is_kernel:
                        self.kernel_depth += 1
                    self.generic_visit(with_node)
                    if is_kernel:
                        self.kernel_depth -= 1

                def visit_For(self, for_node):
                    is_serial = _is_t_call(for_node.iter, "serial")
                    if is_serial:
                        self.serial_depth += 1
                    self.generic_visit(for_node)
                    if is_serial:
                        self.serial_depth -= 1

                def visit_Return(self, return_node):
                    add_error("Do not use `return` inside `@T.prim_func`; guard computation with `if` statements instead.")

                def visit_Continue(self, continue_node):
                    add_error("Do not use `continue` inside `@T.prim_func`; guard computation with `if` statements instead.")

                def visit_Break(self, break_node):
                    add_error("Do not use `break` inside `@T.prim_func`; guard computation with `if` statements instead.")

                def visit_Attribute(self, attr_node):
                    if attr_node.attr == "dtype":
                        add_error("Do not read buffer `.dtype` inside `@T.prim_func`; pass TileLang dtype strings from the `@tl.jit` factory.")
                    self.generic_visit(attr_node)

                def visit_AugAssign(self, assign_node):
                    if self.serial_depth and isinstance(assign_node.target, ast.Name):
                        add_error("Do not mutate Python scalar variables with `+=` inside `T.serial`; use `T.alloc_local((1,), dtype)` or a local buffer accumulator.")
                    self.generic_visit(assign_node)

                def visit_Assign(self, assign_node):
                    if self.serial_depth:
                        for target in assign_node.targets:
                            if isinstance(target, ast.Name) and _contains_name(assign_node.value, target.id):
                                add_error("Do not reassign Python scalar accumulators inside `T.serial`; use `T.alloc_local((1,), dtype)` or a local buffer accumulator.")
                                break
                    self.generic_visit(assign_node)

                def visit_Subscript(self, subscript_node):
                    if isinstance(subscript_node.value, ast.Name) and subscript_node.value.id in buffer_ranks:
                        expected_rank = buffer_ranks[subscript_node.value.id]
                        actual_rank = _subscript_rank(subscript_node.slice)
                        if expected_rank != actual_rank:
                            add_error(
                                f"`T.Buffer` `{subscript_node.value.id}` is declared rank {expected_rank} but indexed with {actual_rank} dimension(s)."
                            )
                    self.generic_visit(subscript_node)

            PrimFuncVisitor().visit(node)

    return errors


def code_call_exec_success_allclose_tilelang(
    code,
    fname,
    py_folder,
    temp_root="tmp2",
    atol=1e-3,
    rtol=1e-1,
    timeout=2*60,
    verbose=False,
    py_interpreter="python3",
):
    tmp_gen_folder = os.path.join(temp_root, "gen")
    os.makedirs(tmp_gen_folder, exist_ok=True)

    lint_errors = lint_tilelang_code_for_eval(code)
    if lint_errors:
        err_msg = "Static TileLang preflight failed:\n" + "\n".join(f"- {error}" for error in lint_errors)
        if verbose:
            print(f"File: {fname}, {err_msg}")
        return False, None, "", err_msg, None, None

    ref_file = os.path.join(py_folder, fname)

    gen_file = get_temp_file(prefix=f'{fname}_gen_tilelang_code')
    gen_file = os.path.join(tmp_gen_folder, gen_file)

    # print('code: ', code)
    # print('gen_file: ', gen_file)
    # print('ref_file: ', ref_file)

    hash_line = "#" * 146

    with open(ref_file, 'r') as f:
        lines = f.readlines()
        for iL, line in enumerate(lines):
            if line.strip() == hash_line:
                break
        test_code_lines = lines[iL + 1:]

    code = code + '\n\n' + hash_line + '\n' + '\n' + '\n'.join(test_code_lines)

    with open(gen_file, 'w') as f:
        f.write(code)

    env = os.environ.copy()
    eval_gpu = os.environ.get("TILELANG_EVAL_GPU")
    if eval_gpu is not None:
        env["CUDA_VISIBLE_DEVICES"] = eval_gpu

    try:
        result_call = subprocess.run(
            [py_interpreter, gen_file],
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
        call_status = result_call.returncode == 0

        if (not call_status) and _is_missing_tilelang_error(result_call.stderr):
            err_msg = "TileLang runtime is unavailable in this environment; skipping TileLang execution."
            if verbose:
                print(f"File: {fname}, {err_msg}")
            return False, None, result_call.stdout, err_msg, None, None

        if not call_status:
            err_msg = f"Generated TileLang module import/call failure: {result_call.stderr}"
            if verbose:
                print(f"File: {fname}, {err_msg}")
            return False, None, result_call.stdout, err_msg, None, None

        result_corr = subprocess.run(
            [
                py_interpreter,
                "/home/wentao/GEAK-agent/src/dataloaders/TB_eval/correctness_tilelang.py",
                "--gen_file", gen_file,
                "--ref_file", ref_file,
                "--atol", str(atol),
                "--rtol", str(rtol),
            ],
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
        stdout_corr = result_corr.stdout
        stderr_corr = result_corr.stderr

    except Exception as e:
        if verbose:
            print(f"File: {fname}, Execution error: {e}")
        return None, None, None, str(e), None, None

    except subprocess.TimeoutExpired:
        if verbose:
            print(f"File: {fname} timed out!")
        return None, None, None, "Time out", None, None
    finally:
        pass

    with open(gen_file + ".stdout", 'w') as f:
        f.write(stdout_corr)

    with open(gen_file + ".stderr", 'w') as f:
        f.write(stderr_corr)

    if result_corr.returncode != 0:
        if verbose:
            print(f"Error in generated code: {stderr_corr}")
        return call_status, None, result_call.stdout, result_call.stderr, stdout_corr, stderr_corr

    if verbose:
        print(f"Success in generated code: {stdout_corr}")
    _, exec_status, gen_stdout, gen_stderr = stdout_corr.split("*#*#", 3)
    return call_status, exec_status, result_call.stdout, result_call.stderr, gen_stdout, gen_stderr


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def green_or_red(status):
    if status:
        return bcolors.OKGREEN
    else:
        return bcolors.FAIL

def color_end():
    return bcolors.ENDC

def bool_colorize(status):
    if status:
        return bcolors.OKGREEN + str(status) + bcolors.ENDC
    else:
        return bcolors.FAIL + str(status) + bcolors.ENDC
