import pathlib
import re
import sys

PYPROJECT = pathlib.Path("pyproject.toml")


def get_version_from_pyproject() -> str:
    text = PYPROJECT.read_text(encoding="utf-8")
    # Match: version = "0.4.0" under [project]
    m = re.search(r'(?m)^\s*version\s*=\s*"([^"]+)"', text)
    if not m:
        print("Could not find [project].version in pyproject.toml", file=sys.stderr)
        sys.exit(1)
    return m.group(1)


def main() -> None:
    # e.g. "refs/tags/v0.4.0"
    if len(sys.argv) < 2:
        print("Usage: check_version_matches_tag.py <GITHUB_REF>", file=sys.stderr)
        sys.exit(1)

    ref = sys.argv[1]
    m = re.match(r"refs/tags/v?(\d+\.\d+\.\d+)$", ref)
    if not m:
        print(f"Ref {ref!r} is not a semantic version tag like v1.2.3", file=sys.stderr)
        sys.exit(1)

    tag_version = m.group(1)
    project_version = get_version_from_pyproject()

    if tag_version != project_version:
        print(
            "Version mismatch:\n"
            f"  pyproject.toml: {project_version}\n"
            f"  git tag:        {tag_version}",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"OK: tag {tag_version} matches pyproject.toml")


if __name__ == "__main__":
    main()
