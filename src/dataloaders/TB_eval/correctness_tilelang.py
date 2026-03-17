import json
import argparse
import os
import importlib.util
import random
import numpy as np
import torch
from collections import namedtuple

torch.set_printoptions(profile="full")


def set_seed(seed: int = 42) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    os.environ['PYTHONHASHSEED'] = str(seed)


def import_variable_from_file(file_path, variable_name):
    set_seed()

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No file found at {file_path}")

    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"Could not load specification for module {module_name}")

    module = importlib.util.module_from_spec(spec)
    if module is None:
        raise ImportError(f"Could not create module {module_name} from spec")

    try:
        spec.loader.exec_module(module)
    except Exception as e:
        raise ImportError(f"Could not execute module {module_name} due to {e}")

    return getattr(module, variable_name, None)


def _compare(ref, gen, fname, atol=1e-3, rtol=1e-3, verbose=False):
    if type(gen) == np.ndarray:
        if np.allclose(ref, gen, atol=atol, rtol=rtol):
            if verbose:
                print(f"Reference and generated outputs matched for file: {fname}")
            return True
        if verbose:
            diff = np.amax(np.abs(ref - gen))
            print(f"Test failed for file: {fname} with abs max diff: {diff}")
        return False
    if type(gen) == torch.Tensor:
        if torch.allclose(ref, gen, atol=atol, rtol=rtol):
            if verbose:
                print(f"Reference and generated outputs matched for file: {fname}")
            return True
        if verbose:
            diff = (ref - gen).abs().max()
            print(f"Test failed for file: {fname} with abs max diff: {diff}")
        return False
    if type(gen) == namedtuple:
        if ref._fields != gen._fields:
            return False
        for field in ref._fields:
            if not torch.equal(getattr(ref, field), getattr(gen, field)):
                return False
        return True
    return ref == gen


def compare(ref, gen, fname, atol=1e-3, rtol=1e-3, verbose=False):
    ret_val = True
    if (type(gen) == list) or (type(gen) == tuple):
        for ref_item, gen_item in zip(ref, gen):
            ret_val &= compare(ref_item, gen_item, fname, atol=atol, rtol=rtol, verbose=verbose)
    elif type(gen) == dict:
        return compare(list(ref.values()), list(gen.values()), fname, atol=atol, rtol=rtol, verbose=verbose)
    else:
        ret_val &= _compare(ref, gen, fname, atol=atol, rtol=rtol, verbose=verbose)
    return ret_val


def test_correctness(ref_file, gen_file, var_name, atol=1e-3, rtol=1e-3, verbose=False):
    fname = os.path.basename(gen_file)
    gen_call_acc = False
    gen_stderr = None
    try:
        gen_result_golden = import_variable_from_file(gen_file, var_name)
        if verbose:
            with open(gen_file + ".out", "w") as f:
                f.write(f"file: {fname}\n")
                json.dump(str(gen_result_golden), f)
                f.write("\n\n\n")
                f.write("#" * 146)
        gen_call_acc = True
    except Exception as e:
        gen_stderr = e
        return gen_call_acc, None, None, gen_stderr

    try:
        ref_result_golden = import_variable_from_file(ref_file, var_name)
        if verbose:
            with open(gen_file + ".out_ref", "w") as f:
                f.write(f"file: {fname}\n")
                json.dump(str(ref_result_golden), f)
                f.write("\n\n\n")
                f.write("#" * 146)
    except Exception as e:
        return gen_call_acc, None, None, e

    if gen_result_golden is None:
        return gen_call_acc, False, None, "Generated output is None"
    if ref_result_golden is None:
        return gen_call_acc, False, None, "Reference output is None"
    if type(gen_result_golden) != type(ref_result_golden):
        return gen_call_acc, False, None, (
            "Reference and Generated output results should be of the same type "
            f"but generated is: {type(gen_result_golden)}, and reference is: {type(ref_result_golden)}"
        )

    exec_acc = compare(ref_result_golden, gen_result_golden, fname, atol=atol, rtol=rtol, verbose=verbose)
    if not exec_acc:
        gen_stderr = f"Generated output does not match reference output for file: {fname}"
    return gen_call_acc, exec_acc, None, gen_stderr


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gen_file", "-pf", type=str, required=True)
    parser.add_argument("--ref_file", "-tf", type=str, required=True)
    parser.add_argument("--var_name", type=str, default="result_gold")
    parser.add_argument("--atol", type=float, default=1e-3)
    parser.add_argument("--rtol", type=float, default=1e-1)
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    gen_call_acc, exec_acc, stdout, gen_stderr = test_correctness(
        args.ref_file,
        args.gen_file,
        args.var_name,
        atol=args.atol,
        rtol=args.rtol,
        verbose=args.verbose,
    )
    print(f"{gen_call_acc}*#*#{exec_acc}*#*#{stdout}*#*#{gen_stderr}")
