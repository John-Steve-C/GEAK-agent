"""Compatibility launcher for the fixed TileLang/tree condition."""

from run_experiment import main


if __name__ == "__main__":
    raise SystemExit(
        main(default_filters={"dsl": "tilelang", "workflow": "fixed", "memory": "tree"})
    )
