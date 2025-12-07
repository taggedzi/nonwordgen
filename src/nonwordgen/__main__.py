# SPDX-License-Identifier: MIT
"""Allow running `python -m nonwordgen` to invoke the CLI."""

from __future__ import annotations

from .cli import main

if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
