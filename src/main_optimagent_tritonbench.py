"""Compatibility launcher for the fixed Triton/tree condition."""

from run_experiment import main


if __name__ == "__main__":
    raise SystemExit(
        main(default_filters={"dsl": "triton", "workflow": "fixed", "memory": "tree"})
    )
