#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
add_spdx_headers.py

Add SPDX-License-Identifier headers to source/text files in the repository.

- Inserts a hash-style SPDX header (e.g. "# SPDX-License-Identifier: MIT")
- Respects shebang and coding cookie ordering for Python files
- Skips common build/virtualenv/cache directories
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from typing import Iterable

# 🔧 Adjust these for other projects if needed
LICENSE_ID = "MIT"
SPDX_TEXT = f"SPDX-License-Identifier: {LICENSE_ID}"

# Directories we will NOT descend into
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

# File extensions that should get a hash-style SPDX header
HASH_COMMENT_EXTS = {
    ".py",
    ".sh",
    ".bash",
    ".zsh",
    ".ps1",
    ".psm1",
    ".psd1",
    ".cfg",
    ".ini",
    ".toml",
    ".yml",
    ".yaml",
    ".md",
    ".txt",
    ".rst",
}

CODING_RE = re.compile(r"coding[:=]\s*([-\w.]+)")


def has_spdx_header(lines: list[str]) -> bool:
    """Return True if any of the first few lines already contains the SPDX marker."""
    for line in lines[:5]:
        if SPDX_TEXT in line:
            return True
    return False


def detect_hash_comment_prefix(path: pathlib.Path) -> str | None:
    """
    For files in HASH_COMMENT_EXTS, return the hash comment prefix.
    For more complex comment styles, extend this function.
    """
    if path.suffix.lower() in HASH_COMMENT_EXTS:
        return "# "
    return None


def insert_spdx_hash_header(lines: list[str]) -> list[str]:
    """
    Insert a hash-style SPDX header into the given list of lines.

    - Keeps shebang on the first line if present.
    - Keeps coding cookie in first or second line.
    """
    if not lines:
        # Empty file: just add the SPDX header
        return [f"# {SPDX_TEXT}\n"]

    # Determine insertion index
    idx = 0
    shebang_first = lines[0].startswith("#!")
    has_coding_line_0 = bool(CODING_RE.search(lines[0])) if lines else False
    has_coding_line_1 = bool(CODING_RE.search(lines[1])) if len(lines) > 1 else False

    if shebang_first:
        idx = 1
        # If second line is coding cookie, insert after it
        if has_coding_line_1:
            idx = 2
    else:
        # No shebang; if first line is coding cookie, insert after it
        if has_coding_line_0:
            idx = 1

    spdx_line = f"# {SPDX_TEXT}\n"
    return lines[:idx] + [spdx_line] + lines[idx:]


def should_process_file(path: pathlib.Path) -> bool:
    """Decide whether this file should be considered for SPDX insertion."""
    if not path.is_file():
        return False
    if path.suffix.lower() in HASH_COMMENT_EXTS:
        return True
    return False


def iter_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    """Yield all candidate files under root, skipping SKIP_DIRS."""
    for dirpath, dirnames, filenames in os_walk(root):
        # dirpath is a Path, dirnames and filenames lists of names (no paths)
        # Filter dirnames in-place to prevent descending
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            yield dirpath / name


def os_walk(root: pathlib.Path):
    """
    Wrapper around os.walk that yields Path objects instead of strings.
    """
    import os

    for dirpath, dirnames, filenames in os.walk(root):
        yield pathlib.Path(dirpath), dirnames, filenames


def process_file(
    path: pathlib.Path,
    dry_run: bool = False,
) -> bool:
    """
    Process a single file.

    Returns True if the file WOULD be modified (or WAS modified if not dry_run).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # Likely a binary file; skip
        return False

    lines = text.splitlines(keepends=True)

    if has_spdx_header(lines):
        return False

    comment_prefix = detect_hash_comment_prefix(path)
    if comment_prefix is None:
        return False

    # For now, we only support hash comments. If we ever need to support
    # other styles, we can branch here based on extension / prefix.
    updated_lines = insert_spdx_hash_header(lines)

    if updated_lines == lines:
        return False

    if not dry_run:
        path.write_text("".join(updated_lines), encoding="utf-8")

    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Add SPDX-License-Identifier headers to source/text files."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Root directory to process (default: current directory).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not modify files; just print what would be changed.",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress per-file output; only show summary.",
    )

    args = parser.parse_args(argv)
    root = pathlib.Path(args.root).resolve()

    if not root.exists():
        print(f"Error: root path does not exist: {root}", file=sys.stderr)
        return 1

    modified = 0
    checked = 0

    for path in iter_files(root):
        if not should_process_file(path):
            continue
        checked += 1
        changed = process_file(path, dry_run=args.dry_run)
        if changed:
            modified += 1
            if not args.quiet:
                action = "WOULD add" if args.dry_run else "Added"
                print(f"{action} SPDX header: {path}")

    if not args.quiet:
        mode = "Dry run" if args.dry_run else "Updated"
        print(f"{mode}: {modified} file(s) out of {checked} candidate(s).")

    # Exit 0 even if nothing changed; we’re not a linter by default.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
