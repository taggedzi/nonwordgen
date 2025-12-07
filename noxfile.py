# SPDX-License-Identifier: MIT
"""Nox sessions for testing, linting, type checking, and building."""
from __future__ import annotations
from pathlib import Path
import shutil
import sys
import zipfile

try:  # Python 3.11+
    import tomllib
except ModuleNotFoundError:  # Python <3.11
    import tomli as tomllib  # type: ignore[no-redef]

import nox
from nox.command import CommandFailed

ROOT = Path(__file__).resolve().parent


def _run_pytest(session: nox.Session) -> None:
    _install_project_editable(session)
    session.install("pytest")
    session.run("pytest", *session.posargs)


def get_project_version() -> str:
    """Read and return the project version from pyproject.toml."""
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    return data["project"]["version"]


def _detect_package_name() -> str:
    """Detect the main package directory (contains __init__.py under src/)."""
    src_root = ROOT / "src"
    if not src_root.is_dir():
        raise RuntimeError("Expected a src/ directory for the package layout.")

    candidates: list[str] = []
    for path in src_root.iterdir():
        if path.is_dir() and (path / "__init__.py").exists():
            candidates.append(path.name)
    if "nonwordgen" in candidates:
        return "nonwordgen"
    if candidates:
        return sorted(candidates)[0]
    raise RuntimeError("Could not detect a package directory under src/.")


PACKAGE = _detect_package_name()
CODE_LOCATIONS = ("src", "tests")

# When running bare `nox`, run tests and lint by default.
nox.options.sessions = ("tests", "lint")


def _install_project_editable(session: nox.Session) -> None:
    """Install the project in editable mode, with dev extras if available."""
    try:
        session.install("-e", ".[dev]")
    except CommandFailed:
        session.install("-e", ".")


def _find_build_script() -> Path:
    """Find an existing build script in the repo root (e.g. build_release.py)."""
    candidates = sorted(ROOT.glob("build*.py"))
    if not candidates:
        raise RuntimeError("No build_*.py script found in the repository root.")
    for candidate in candidates:
        if candidate.name == "build_release.py":
            return candidate
    return candidates[0]


# Run the test suite with pytest.
@nox.session
def tests(session: nox.Session) -> None:
    """Run the test suite with the current interpreter."""
    _run_pytest(session)


# Run tests with coverage and generate coverage.xml.
@nox.session
def coverage(session: nox.Session) -> None:
    _install_project_editable(session)
    session.install("pytest", "coverage", "pytest-cov")
    session.run("coverage", "erase")
    # Use pytest-cov so configuration from .coveragerc is respected while keeping
    # the invocation simple and reproducible.
    session.run(
        "pytest",
        f"--cov={PACKAGE}",
        "--cov-report=term",
        "--cov-report=xml",
        *session.posargs,
    )
    # Optionally generate an HTML coverage report under htmlcov/.
    session.run("coverage", "html")


# Run Ruff in check-only mode (no changes).
@nox.session
def lint(session: nox.Session) -> None:
    session.install("ruff")
    session.run("ruff", "check", *CODE_LOCATIONS)


# Run Ruff with auto-fix, then Black formatting.
@nox.session
def format(session: nox.Session) -> None:
    session.install("ruff", "black")
    session.run("ruff", "check", "--fix", *CODE_LOCATIONS)
    session.run("black", *CODE_LOCATIONS)


# Run static type checking with mypy.
@nox.session
def typecheck(session: nox.Session) -> None:
    _install_project_editable(session)
    session.install("mypy")
    session.run("mypy", f"src/{PACKAGE}", *session.posargs)


# Run the existing build script in the repo root.
@nox.session
def build(session: nox.Session) -> None:
    _install_project_editable(session)
    # Ensure optional dictionary backend is available so wordfreq
    # support (and its data files) are included in GUI builds.
    session.install(".[dictionaries]")
    # PyInstaller (and PyQt6) are required by build_release.py for the GUI binary.
    session.install("pyinstaller", "PyQt6")
    script = _find_build_script()
    session.run("python", str(script))


# Build wheel and sdist packages for distribution (PyPI-ready artifacts).
@nox.session
def build_package(session: nox.Session) -> None:
    _install_project_editable(session)
    session.install("build")

    dist_dir = ROOT / "dist"
    build_dir = ROOT / "build"
    shutil.rmtree(dist_dir, ignore_errors=True)
    shutil.rmtree(build_dir, ignore_errors=True)

    session.run("python", "-m", "build", external=True)


@nox.session
def build_dist(session: nox.Session) -> None:
    """Build sdist and wheel artifacts on Linux only."""
    if sys.platform != "linux":
        session.log("Skipping build_dist: Linux-only build.")
        return

    _install_project_editable(session)
    session.install("build")

    dist_dir = ROOT / "dist"
    build_dir = ROOT / "build"
    shutil.rmtree(dist_dir, ignore_errors=True)
    shutil.rmtree(build_dir, ignore_errors=True)

    session.run("python", "-m", "build", external=True)


# Build a standalone Windows executable using PyInstaller.
@nox.session
def build_exe(session: nox.Session) -> None:
    # On non-Windows platforms, just log and exit successfully without running PyInstaller.
    if sys.platform != "win32":
        session.log("Skipping build_exe: Windows-only build.")
        return

    _install_project_editable(session)
    # Ensure optional dictionary backend is available for GUI builds
    # and PyInstaller/PyQt6 are present so dependencies freeze correctly.
    session.install(".[dictionaries]")
    session.install("pyinstaller", "PyQt6")

    dist_dir = ROOT / "dist"
    build_dir = ROOT / "build"
    shutil.rmtree(dist_dir, ignore_errors=True)
    shutil.rmtree(build_dir, ignore_errors=True)

    spec_files = sorted(ROOT.glob("*.spec"))
    if spec_files:
        spec_path = spec_files[0]
        session.run("pyinstaller", str(spec_path), external=True)
        return

    script = ROOT / "build_release.py"
    if script.exists():
        session.run("python", str(script), external=True)
        return

    raise RuntimeError("No .spec file or build_release.py found for EXE build.")


@nox.session
def changelog(session: nox.Session) -> None:
    """Regenerate CHANGELOG.md from git history."""
    session.install("gitpython")  # not strictly needed if you keep the script as-is
    session.run("python", "tools/generate_changelog.py", external=True)


@nox.session
def publish_release(session: nox.Session) -> None:
    """
    Create a tagged release and push it.

    Usage:
        nox -s make_release -- 1.2.1
        nox -s make_release -- v1.2.1
    """
    if not session.posargs:
        session.error("Usage: nox -s make_release -- <version>")

    version = session.posargs[0]
    session.run("python", "tools/make_release.py", version, external=True)



@nox.session(name="bundle_release")
def bundle_release(session: nox.Session) -> None:
    """
    Bundle the built Windows executable and related artifacts into a versioned
    zip file and generate a SHA-256 checksum.
    """
    # NOTE: This session does NOT build the binary. Ensure that
    # dist/nonwords-gen.exe already exists (via another nox session, build
    # script, or CI step) before running this session; it only bundles
    # existing artifacts and generates checksums.
    version = get_project_version()
    release_name = f"nonwords-gen-v{version}-win64"

    dist_dir = ROOT / "dist"
    release_dir = dist_dir / release_name
    binary_path = dist_dir / "nonwords-gen.exe"

    if not binary_path.is_file():
        session.error(
            f"Binary not found: {binary_path} (build it before running the release session)"
        )

    if release_dir.exists():
        session.log(f"Removing existing release directory: {release_dir}")
        shutil.rmtree(release_dir)

    session.log(f"Creating release directory: {release_dir}")
    release_dir.mkdir(parents=True, exist_ok=True)

    # Copy core project files.
    root = ROOT
    files_to_copy = [
        ("LICENSE", release_dir / "LICENSE"),
        ("README.md", release_dir / "README.md"),
        ("THIRD_PARTY.md", release_dir / "THIRD_PARTY.md"),
    ]

    changelog_src = root / "CHANGELOG.md"
    if changelog_src.is_file():
        files_to_copy.append(("CHANGELOG.md", release_dir / "CHANGELOG.md"))

    for relative_name, destination in files_to_copy:
        src = root / relative_name
        if src.is_file():
            session.log(f"Copying {src} -> {destination}")
            shutil.copy2(src, destination)

    # Copy licenses directory.
    licenses_src = root / "licenses"
    licenses_dest = release_dir / "licenses"
    if licenses_src.is_dir():
        session.log(f"Copying licenses directory: {licenses_src} -> {licenses_dest}")
        shutil.copytree(licenses_src, licenses_dest)

    # Optionally copy the screenshot if present.
    screenshot_src = root / "docs" / "images" / "nonwords-gen_screenshot.png"
    if screenshot_src.is_file():
        screenshot_dest = release_dir / "docs" / "images" / "nonwords-gen_screenshot.png"
        session.log(f"Copying screenshot: {screenshot_src} -> {screenshot_dest}")
        screenshot_dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(screenshot_src, screenshot_dest)

    # Copy the built binary.
    binary_dest = release_dir / "nonwords-gen.exe"
    session.log(f"Copying binary: {binary_path} -> {binary_dest}")
    shutil.copy2(binary_path, binary_dest)

    # Create the zip archive containing the release directory.
    zip_path = dist_dir / f"{release_name}.zip"
    if zip_path.exists():
        session.log(f"Removing existing zip archive: {zip_path}")
        zip_path.unlink()

    session.log(f"Creating zip archive: {zip_path}")
    with zipfile.ZipFile(zip_path, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in release_dir.rglob("*"):
            if path.is_file():
                arcname = path.relative_to(dist_dir)
                zf.write(path, arcname=str(arcname))

    # Generate SHA-256 checksum for the zip archive.
    session.log("Generating SHA-256 checksum for the release zip")
    session.run("python", "tools/generate_sha256.py", str(zip_path), external=True)


@nox.session
def spdx(session):
    """
    Check (default) or add SPDX headers to the repository.
    Validates that all source files include an SPDX license header.
    This session is enforced in CI and required for releases.

    Usage:
        nox -s spdx            # check only, fails if headers are missing
        nox -s spdx -- add     # auto-add missing SPDX headers
    """
    script = "tools/add_spdx_headers.py"

    # Add mode: actually modify files.
    if session.posargs and session.posargs[0] == "add":
        session.log("Adding SPDX headers where missing...")
        session.run("python", script, external=True)
        return

    # Default: check mode (dry-run, fail if anything *would* change).
    session.log("Checking SPDX headers (dry run)...")
    output = session.run(
        "python",
        script,
        "--dry-run",
        external=True,
        silent=True,
        success_codes=[0],
    )

    if "WOULD add SPDX header" in output:
        session.error(
            "Some files are missing SPDX headers.\n"
            "Run `nox -s spdx -- add` to fix them."
        )
    else:
        session.log("All files already contain SPDX headers.")


@nox.session
def prepush(session: nox.Session) -> None:
    """
    Run all local checks before pushing to GitHub.

    This will:
      - auto-format the code
      - verify SPDX headers
      - run linting
      - run type-checking
      - run unit tests
      - run coverage
    """
    session.log("Running pre-push checks: format → spdx → lint → typecheck → tests → coverage")

    # These queue other sessions to be run in this Nox invocation.
    session.notify("format")
    session.notify("spdx")       # default is 'check' mode
    session.notify("lint")
    session.notify("typecheck")
    session.notify("tests")
    session.notify("coverage")
