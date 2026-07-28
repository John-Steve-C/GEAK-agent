"""Compatibility launcher for the LangChain Triton/tree condition."""

from run_experiment import main


if __name__ == "__main__":
    raise SystemExit(
        main(default_filters={"dsl": "triton", "workflow": "langchain", "memory": "tree"})
    )
