#!/usr/bin/env python
# SPDX-License-Identifier: MIT
"""
make_release.py

Automates a release flow:

- Check that the working tree is clean
- Verify the requested version matches pyproject.toml's [project.version]
- Regenerate CHANGELOG.md
- Commit CHANGELOG.md if it changed
- Create a git tag for the version
- Push the current branch and the new tag to origin

Usage:

    python tools/make_release.py 1.2.1
    python tools/make_release.py v1.2.1
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
import sys
import textwrap
import tomllib
from typing import List

ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = ROOT / "pyproject.toml"
CHANGELOG = ROOT / "CHANGELOG.md"


def run_git(args: List[str], check: bool = True) -> str:
    """Run a git command in the repo root and return stdout."""
    result = subprocess.run(
        ["git"] + args,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        sys.stderr.write(f"git {' '.join(args)} failed:\n{result.stderr}\n")
        sys.exit(result.returncode)
    return result.stdout.strip()


def ensure_clean_working_tree() -> None:
    """Fail if there are uncommitted changes."""
    status = run_git(["status", "--porcelain"], check=True)
    if status:
        sys.stderr.write(
            "Refusing to make a release: working tree is not clean.\n"
            "Please commit or stash your changes first.\n"
        )
        sys.exit(1)


def load_pyproject_version() -> str:
    """Return [project.version] from pyproject.toml."""
    if not PYPROJECT.is_file():
        sys.stderr.write(f"pyproject.toml not found at {PYPROJECT}\n")
        sys.exit(1)
    data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    try:
        return str(data["project"]["version"])
    except KeyError as exc:
        sys.stderr.write(
            "Could not find [project.version] in pyproject.toml.\n"
        )
        raise SystemExit(1) from exc


def generate_changelog() -> None:
    """Run the changelog generator script."""
    script = ROOT / "tools" / "generate_changelog.py"
    if not script.is_file():
        sys.stderr.write(f"Changelog generator not found: {script}\n")
        sys.exit(1)

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
    )
    if result.returncode != 0:
        sys.stderr.write("Failed to generate changelog.\n")
        sys.exit(result.returncode)


def changelog_changed() -> bool:
    """Return True if CHANGELOG.md has uncommitted changes."""
    status = run_git(["status", "--porcelain", "--", str(CHANGELOG)], check=True)
    return bool(status.strip())


def commit_changelog(tag_name: str) -> None:
    """Stage and commit CHANGELOG.md if it has changed."""
    if not changelog_changed():
        print("No changes in CHANGELOG.md; skipping changelog commit.")
        return

    print("Committing updated CHANGELOG.md...")
    run_git(["add", str(CHANGELOG)], check=True)
    msg = f"Update changelog for {tag_name}"
    run_git(["commit", "-m", msg], check=True)


def tag_exists(tag_name: str) -> bool:
    """Return True if the given tag already exists."""
    output = run_git(["tag", "--list", tag_name], check=True)
    return bool(output.strip())


def create_tag(tag_name: str) -> None:
    """Create an annotated git tag."""
    if tag_exists(tag_name):
        sys.stderr.write(f"Tag {tag_name} already exists.\n")
        sys.exit(1)

    print(f"Creating tag {tag_name}...")
    run_git(["tag", "-a", tag_name, "-m", f"Release {tag_name}"], check=True)


def push_release(tag_name: str) -> None:
    """Push the current branch and the new tag to origin."""
    branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"], check=True)
    if branch == "HEAD":
        sys.stderr.write("Cannot determine current branch (detached HEAD).\n")
        sys.exit(1)

    print(f"Pushing branch {branch} to origin...")
    run_git(["push", "origin", branch], check=True)

    print(f"Pushing tag {tag_name} to origin...")
    run_git(["push", "origin", tag_name], check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a tagged release (generate changelog, commit, tag, push).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
            Examples:
              python tools/make_release.py 1.2.1
              python tools/make_release.py v1.2.1
            """
        ),
    )
    parser.add_argument(
        "version",
        help="Version to release (e.g. 1.2.1 or v1.2.1)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Normalize version/tag
    raw_version = args.version.strip()
    if not raw_version:
        sys.stderr.write("Version cannot be empty.\n")
        sys.exit(1)

    if raw_version.startswith("v"):
        normalized_version = raw_version[1:]
        tag_name = raw_version
    else:
        normalized_version = raw_version
        tag_name = f"v{raw_version}"

    print(f"Preparing release for version {normalized_version} (tag {tag_name})")

    # Ensure working tree is clean before we start
    ensure_clean_working_tree()

    # Check pyproject version matches
    project_version = load_pyproject_version()
    if project_version != normalized_version:
        sys.stderr.write(
            f"Version mismatch:\n"
            f"  requested: {normalized_version}\n"
            f"  pyproject: {project_version}\n\n"
            "Please update [project.version] in pyproject.toml and commit it first.\n"
        )
        sys.exit(1)

    # Generate and commit changelog (if changed)
    generate_changelog()
    commit_changelog(tag_name)

    # Now working tree should be clean again; create tag and push
    ensure_clean_working_tree()
    create_tag(tag_name)
    push_release(tag_name)

    print("Release completed.")
    print("GitHub Actions should now pick up the tag and build the release artifacts.")


if __name__ == "__main__":
    main()
