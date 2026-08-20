from __future__ import annotations

import sys
from pathlib import Path

from Lexer import Lexer, LexerError


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("uso: python runner.py arquivo.microc", file=sys.stderr)
        return 2

    try:
        source = Path(args[0]).read_text(encoding="utf-8")
        tokens = Lexer(source).scan()
    except (OSError, UnicodeError) as error:
        print(f"erro ao ler {args[0]!r}: {error}", file=sys.stderr)
        return 2
    except LexerError as error:
        print(error, file=sys.stderr)
        return 1

    for token in tokens:
        print(token)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
