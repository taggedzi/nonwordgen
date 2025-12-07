#!/usr/bin/env python
# SPDX-License-Identifier: MIT
"""
Generate a CHANGELOG.md file from git tags and commit messages.

This script:
- Lists git tags in chronological order
- For each tag, collects commits since the previous tag
- Writes a simple markdown changelog with sections per version

It is intentionally simple and does not require extra dependencies.
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List, Tuple


ROOT = Path(__file__).resolve().parent.parent
CHANGELOG_PATH = ROOT / "CHANGELOG.md"


def run_git(args: List[str]) -> str:
    """Run a git command and return its stripped stdout as text."""
    result = subprocess.run(
        ["git"] + args,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def get_tags() -> List[str]:
    """
    Return a list of tags sorted by creation date (oldest first).

    If there are no tags, returns an empty list.
    """
    try:
        output = run_git(["tag", "--sort=creatordate"])
    except subprocess.CalledProcessError:
        return []
    tags = [line.strip() for line in output.splitlines() if line.strip()]
    return tags


def get_commits_range(ref_from: str | None, ref_to: str) -> List[str]:
    """
    Get commit messages in the range (ref_from, ref_to].

    If ref_from is None, includes all commits up to ref_to.
    """
    if ref_from:
        rev_range = f"{ref_from}..{ref_to}"
    else:
        rev_range = ref_to

    try:
        output = run_git(
            [
                "log",
                rev_range,
                "--pretty=format:- %s (%h)",
            ]
        )
    except subprocess.CalledProcessError:
        return []

    commits = [line for line in output.splitlines() if line.strip()]
    return commits


def get_unreleased_commits(last_tag: str | None) -> List[str]:
    """Get commits after the last tag, up to HEAD."""
    if last_tag is None:
        # If there are no tags, we'll treat everything as part of the initial release range
        return []
    try:
        output = run_git(
            [
                "log",
                f"{last_tag}..HEAD",
                "--pretty=format:- %s (%h)",
            ]
        )
    except subprocess.CalledProcessError:
        return []
    commits = [line for line in output.splitlines() if line.strip()]
    return commits


def build_changelog() -> str:
    """Construct the full changelog markdown as a string."""
    tags = get_tags()
    lines: List[str] = []

    # Header
    lines.append("# Changelog")
    lines.append("")
    lines.append(
        "All notable changes to this project will be documented in this file."
    )
    lines.append("")
    lines.append(
        "This changelog is **automatically generated** from git tags and commit "
        "messages using `tools/generate_changelog.py`."
    )
    lines.append("")

    # Unreleased section (commits after the latest tag)
    last_tag = tags[-1] if tags else None
    unreleased = get_unreleased_commits(last_tag)
    lines.append("## [Unreleased]")
    lines.append("")
    if unreleased:
        lines.extend(unreleased)
        lines.append("")
    else:
        lines.append("_No unreleased changes yet._")
        lines.append("")

    # Versioned sections (latest first)
    lines.append("---")
    lines.append("")

    # Build sections from newest tag to oldest
    prev_tag: str | None = None
    tag_pairs: List[Tuple[str | None, str]] = []

    # tags is oldest -> newest; we want newest -> oldest for output
    if tags:
        # First range: commits up to the first tag (if that’s meaningful)
        # We'll just show all commits up to the first tag as that version.
        prev_tag = None
        for tag in tags:
            tag_pairs.append((prev_tag, tag))
            prev_tag = tag

    # Now write sections newest first
    for ref_from, ref_to in reversed(tag_pairs):
        commits = get_commits_range(ref_from, ref_to)
        if not commits:
            # If there are no commits in this range, skip writing the section
            continue

        lines.append(f"## [{ref_to}]")
        lines.append("")
        lines.extend(commits)
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    changelog = build_changelog()
    CHANGELOG_PATH.write_text(changelog, encoding="utf-8")
    print(f"Changelog written to {CHANGELOG_PATH}")


if __name__ == "__main__":
    main()
