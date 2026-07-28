"""Compatibility launcher for the LangChain TileLang/flat condition."""

from experiments.code_utils import (
    classify_legacy_tilelang_result as classify_result,
    extract_response_code,
    extract_run_test_tool_code,
    extract_test_shape_hints,
    fix_tilelang_prim_func_indent,
)
from run_experiment import main


if __name__ == "__main__":
    raise SystemExit(
        main(default_filters={"dsl": "tilelang", "workflow": "langchain", "memory": "flat"})
    )
