# SPDX-License-Identifier: MIT
from __future__ import annotations

from pathlib import Path
import hashlib
import sys
from typing import List


CHUNK_SIZE = 1024 * 1024  # 1 MiB


def _compute_sha256(path: Path) -> str:
    """Compute the SHA-256 hex digest of a file in a streaming fashion."""
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def main(argv: List[str]) -> int:
    """CLI entry point: generate a .sha256 file for the given artifact."""
    if len(argv) != 2:
        print(
            "Usage: python tools/generate_sha256.py PATH_TO_FILE",
            file=sys.stderr,
        )
        return 1

    input_path = Path(argv[1])
    if not input_path.is_file():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        return 1

    digest = _compute_sha256(input_path)
    output_path = input_path.with_suffix(input_path.suffix + ".sha256")

    try:
        with output_path.open("w", encoding="utf-8") as fh:
            fh.write(f"{digest}  {input_path.name}\n")
    except OSError as exc:
        print(f"Error: failed to write checksum file: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

