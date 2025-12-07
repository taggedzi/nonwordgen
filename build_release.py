# SPDX-License-Identifier: MIT
"""Build helper for nonwordgen GUI releases.

This script automates:

- (Optionally) running the test suite, if pytest is installed
- Building the standalone GUI binary via PyInstaller using nonwords-gen.spec
- Creating a zip archive of the built dist/nonwords-gen folder

Usage:
    python build_release.py
"""
from __future__ import annotations

import pathlib
import shutil
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parent
DIST_DIR = ROOT / "dist"
EXE_DIR = DIST_DIR / "nonwords-gen"


def run(cmd: list[str]) -> None:
    print(">>", " ".join(cmd))
    subprocess.check_call(cmd)


def maybe_run_tests() -> None:
    try:
        import pytest  # type: ignore[unused-import]  # noqa: F401
    except Exception:
        print("pytest not installed; skipping tests.")
        return
    print("Running test suite...")
    run([sys.executable, "-m", "pytest"])


def build_binary() -> None:
    print("Building nonwords-gen.exe with PyInstaller...")
    run([sys.executable, "-m", "PyInstaller", "nonwords-gen.spec"])


def make_zip() -> pathlib.Path:
    from nonwordgen import __version__  # import here so editable installs work

    exe_dir = EXE_DIR
    exe_file = DIST_DIR / "nonwords-gen.exe"

    if exe_dir.is_dir():
        archive_root = exe_dir
        base_dir = exe_dir
        base_name = None
    elif exe_file.is_file():
        # PyInstaller one-file mode: only a single EXE in dist/.
        # Zip just that executable so the release artifact remains a single download.
        archive_root = DIST_DIR
        base_dir = DIST_DIR
        base_name = exe_file.name
    else:
        raise SystemExit(
            f"Expected build output directory or EXE not found: {exe_dir} or {exe_file}"
        )

    DIST_DIR.mkdir(exist_ok=True)
    archive_stem = DIST_DIR / f"nonwords-gen-{__version__}-windows"
    archive_path = archive_stem.with_suffix(".zip")

    if archive_path.exists():
        archive_path.unlink()

    print(f"Creating release archive {archive_path} ...")
    if base_name is None:
        shutil.make_archive(str(archive_stem), "zip", base_dir)
    else:
        shutil.make_archive(str(archive_stem), "zip", base_dir, base_name)
    return archive_path


def main() -> int:
    maybe_run_tests()
    build_binary()
    archive_path = make_zip()
    print(f"Release build complete: {archive_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

