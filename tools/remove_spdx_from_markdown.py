#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Remove SPDX-License-Identifier comment headers from Markdown files in the tree.

This is a one-off cleanup script to strip SPDX headers that were
accidentally added to *.md and *.markdown files.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from typing import Iterable


MARKDOWN_EXTS = {".md", ".markdown"}

SPDX_PATTERN = re.compile(
    r"""
    ^\s*
    (?P<prefix>\#|//|/\*|<!--)
    \s*SPDX-License-Identifier:\s*[A-Za-z0-9.\-+]+
    (?:\s*\*/\s*|\s*-->\s*)?
    \s*$
    """,
    re.VERBOSE,
)

# Directories we will NOT descend into (exact matches)
SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".mypy_cache",
    ".pytest_cache",
    ".venv",
    "venv",
    "env",
    ".env",
    "build",
    "dist",
    "__pycache__",
    ".tox",
    ".nox",
    ".idea",
    ".vscode",
    ".github",
}


def is_markdown_file(path: pathlib.Path) -> bool:
    """Return True if the path points to a Markdown file we should inspect."""
    return path.suffix.lower() in MARKDOWN_EXTS


def os_walk(root: pathlib.Path):
    """Wrapper around os.walk that yields Path objects instead of strings."""
    import os

    for dirpath, dirnames, filenames in os.walk(root):
        yield pathlib.Path(dirpath), dirnames, filenames


def iter_markdown_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    """Yield Markdown files under root, skipping SKIP_DIRS and *.egg-info."""
    for dirpath, dirnames, filenames in os_walk(root):
        dirnames[:] = [
            d
            for d in dirnames
            if d not in SKIP_DIRS and not d.endswith(".egg-info")
        ]
        for name in filenames:
            path = dirpath / name
            if is_markdown_file(path):
                yield path


def is_spdx_header_line(line: str) -> bool:
    """Return True if the given line is one of the supported SPDX header forms."""
    return SPDX_PATTERN.match(line) is not None


def remove_spdx_from_markdown_file(path: pathlib.Path) -> bool:
    """
    Remove a leading SPDX header from the Markdown file, if present.

    Returns True if the file was modified.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"Warning: could not read {path}: {exc}", file=sys.stderr)
        return False

    if not text:
        return False

    lines = text.splitlines(keepends=True)

    # Find index of first non-empty (non-whitespace) line
    first_nonempty_idx = None
    for idx, line in enumerate(lines):
        if line.strip():
            first_nonempty_idx = idx
            break

    if first_nonempty_idx is None:
        # File is all whitespace
        return False

    header_idx = first_nonempty_idx
    if not is_spdx_header_line(lines[header_idx]):
        # First non-empty line is not an SPDX header; leave file unchanged
        return False

    # Remove the SPDX header line
    del lines[header_idx]

    # Also remove a single immediately following blank line, if present
    if header_idx < len(lines) and not lines[header_idx].strip():
        del lines[header_idx]

    new_text = "".join(lines)
    if new_text == text:
        return False

    try:
        path.write_text(new_text, encoding="utf-8")
    except OSError as exc:
        print(f"Warning: could not write {path}: {exc}", file=sys.stderr)
        return False

    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Remove SPDX-License-Identifier headers from Markdown files "
            "that were accidentally modified."
        )
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Root directory to process (default: current directory).",
    )

    args = parser.parse_args(argv)
    root = pathlib.Path(args.root).resolve()

    if not root.exists():
        print(f"Error: root path does not exist: {root}", file=sys.stderr)
        return 1

    total_files = 0
    modified_files = 0

    for path in iter_markdown_files(root):
        total_files += 1
        if remove_spdx_from_markdown_file(path):
            modified_files += 1

    print(
        f"Scanned {total_files} Markdown file(s); "
        f"modified {modified_files} file(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

