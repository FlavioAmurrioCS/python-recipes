from __future__ import annotations


def main(argv: list[str] | None = None) -> int:
    from python_recipes.cli import main as _main

    return _main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
