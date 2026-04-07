import json
from collections import OrderedDict
from glob import glob


ERROR_TYPES = [
    "Compile / launch error",
    "Runtime error",
    "Wrong answer",
    "Boundary failure",
    "Performance fail",
]

BOUNDARY_KEYWORDS = [
    "mask",
    "boundary",
    "out of bounds",
    "out-of-bounds",
    "oob",
    "non-divisible",
    "non divisible",
    "not divisible",
    "divisible",
    "shape mismatch",
    "broadcast",
    "stride",
    "misaligned",
    "tl.load",
    "tl.store",
]

WRONG_ANSWER_KEYWORDS = [
    "generated output does not match reference output",
    "does not match reference",
    "allclose",
    "mismatch",
    "abs max diff",
    "reference and generated output results should be of the same type",
    "generated output is none",
]


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_iteration_files(root):
    pattern = f"{root}_*.json"
    files = []
    for path in glob(pattern):
        suffix = path[len(root) + 1 : -5]
        if suffix.isdigit():
            files.append((int(suffix), path))
    return sorted(files)


def normalize_text(*parts):
    merged = "\n".join(str(part) for part in parts if part not in (None, "", "None"))
    return merged.lower()


def classify_error(item):
    pass_call = bool(item.get("pass_call"))
    pass_exe = bool(item.get("pass_exe"))
    pass_perf = bool(item.get("pass_perf"))

    if pass_perf or (pass_exe and pass_perf):
        return None
    if pass_exe and not pass_perf:
        return "Performance fail"
    if pass_call and pass_exe:
        return None
    if not pass_call:
        return "Compile / launch error"

    error_text = normalize_text(item.get("call_err_msg"), item.get("exe_err_msg"))
    if any(keyword in error_text for keyword in BOUNDARY_KEYWORDS):
        return "Boundary failure"
    if any(keyword in error_text for keyword in WRONG_ANSWER_KEYWORDS):
        return "Wrong answer"
    return "Runtime error"


def initialize_distribution():
    return OrderedDict((error_type, 0) for error_type in ERROR_TYPES)


def summarize_iteration(data, flag_pass_call, flag_pass_exe, flag_pass_perf, solutions):
    distribution = initialize_distribution()

    for filename, item in data.items():
        if item.get("pass_call"):
            flag_pass_call[filename] = True
        if item.get("pass_exe"):
            flag_pass_exe[filename] = True
        if item.get("pass_perf"):
            flag_pass_perf[filename] = True

        if item.get("pass_perf") and item.get("perf_candidates"):
            solutions[filename] = item["perf_candidates"][-1][0]
        elif item.get("exe_candidate") is not None:
            solutions[filename] = item["exe_candidate"]
        elif item.get("call_candidate") is not None:
            solutions[filename] = item["call_candidate"]

        error_type = classify_error(item)
        if error_type is not None:
            distribution[error_type] += 1

    return distribution


def format_distribution(distribution, total):
    lines = []
    for error_type, count in distribution.items():
        rate = (count / total) if total else 0.0
        lines.append(f"  - {error_type}: {count} ({rate:.4f})")
    return "\n".join(lines)


if __name__ == "__main__":
    root = "../outputs/new/optimagent_gpt41_origin_mem"

    iter_files = find_iteration_files(root)
    if not iter_files:
        raise FileNotFoundError(f"No iteration files found for root: {root}")

    first_data = load_json(iter_files[0][1])
    filenames = list(first_data.keys())

    flag_pass_call = OrderedDict((filename, False) for filename in filenames)
    flag_pass_exe = OrderedDict((filename, False) for filename in filenames)
    flag_pass_perf = OrderedDict((filename, False) for filename in filenames)
    solutions = OrderedDict((filename, None) for filename in filenames)

    summaries = []
    last_data = first_data

    for iter_num, file_path in iter_files:
        data = load_json(file_path)
        last_data = data

        for filename in filenames:
            if filename not in data:
                raise KeyError(f"Missing filename {filename} in {file_path}")

        distribution = summarize_iteration(
            data=data,
            flag_pass_call=flag_pass_call,
            flag_pass_exe=flag_pass_exe,
            flag_pass_perf=flag_pass_perf,
            solutions=solutions,
        )

        total = len(filenames)
        accumulated_call_rate = sum(flag_pass_call.values()) / total
        accumulated_exe_rate = sum(flag_pass_exe.values()) / total
        accumulated_perf_rate = sum(flag_pass_perf.values()) / total

        summary = {
            "iter": iter_num,
            "accumulated_call_rate": accumulated_call_rate,
            "accumulated_exe_rate": accumulated_exe_rate,
            "accumulated_perf_rate": accumulated_perf_rate,
            "distribution": distribution,
        }
        summaries.append(summary)

        print(
            f"iter {iter_num}: "
            f"accumulated_call_rate={accumulated_call_rate:.4f}, "
            f"accumulated_exe_rate={accumulated_exe_rate:.4f}, "
            f"accumulated_perf_rate={accumulated_perf_rate:.4f}"
        )
        print(format_distribution(distribution, total))

    with open(f"{root}_final_solutions.jsonl", "w", encoding="utf-8") as f:
        for filename in filenames:
            item = last_data[filename]
            output = {
                "filename": filename,
                "pass_call": bool(flag_pass_call[filename]),
                "pass_exe": bool(flag_pass_exe[filename]),
                "pass_perf": bool(flag_pass_perf[filename]),
                "solution": solutions[filename],
                "error_type": classify_error(item),
            }
            f.write(json.dumps(output, ensure_ascii=False) + "\n")

    metrics_path = f"{root}_accumulated_acc_2.txt"
    with open(metrics_path, "w", encoding="utf-8") as f:
        for summary in summaries:
            f.write(
                f"Iter {summary['iter']}: "
                f"accumulated_call_rate={summary['accumulated_call_rate']:.4f}, "
                f"accumulated_exe_rate={summary['accumulated_exe_rate']:.4f}, "
                f"accumulated_perf_rate={summary['accumulated_perf_rate']:.4f}\n"
            )
            f.write("Error distribution:\n")
            f.write(format_distribution(summary["distribution"], len(filenames)))
            f.write("\n")
