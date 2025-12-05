"""Nox sessions for testing, linting, type checking, and building."""

from __future__ import annotations

from pathlib import Path
import shutil
import sys

import nox
from nox.command import CommandFailed

ROOT = Path(__file__).resolve().parent
PYTHON_VERSIONS = ["3.11"]


def _detect_package_name() -> str:
    """Detect the main package directory (contains __init__.py in repo root)."""
    candidates: list[str] = []
    for path in ROOT.iterdir():
        if path.is_dir() and (path / "__init__.py").exists():
            candidates.append(path.name)
    if "nonwordgen" in candidates:
        return "nonwordgen"
    if candidates:
        return sorted(candidates)[0]
    raise RuntimeError("Could not detect a package directory in the repository root.")


PACKAGE = _detect_package_name()
CODE_LOCATIONS = (PACKAGE, "tests")

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
@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    _install_project_editable(session)
    session.install("pytest")
    session.run("pytest", *session.posargs)


# Run tests with coverage and generate coverage.xml.
@nox.session(python=PYTHON_VERSIONS)
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
@nox.session(name="lint_fix")
def lint_fix(session: nox.Session) -> None:
    session.install("ruff", "black")
    session.run("ruff", "check", "--fix", *CODE_LOCATIONS)
    session.run("black", *CODE_LOCATIONS)


# Format code using Black.
@nox.session
def format(session: nox.Session) -> None:
    session.install("black")
    session.run("black", *CODE_LOCATIONS)


# Run static type checking with mypy.
@nox.session(python=PYTHON_VERSIONS)
def typecheck(session: nox.Session) -> None:
    _install_project_editable(session)
    session.install("mypy")
    session.run("mypy", PACKAGE, *session.posargs)


# Run the existing build script in the repo root.
@nox.session
def build(session: nox.Session) -> None:
    _install_project_editable(session)
    # PyInstaller is required by build_release.py for the GUI binary.
    session.install("pyinstaller")
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


# Build a standalone Windows executable using PyInstaller.
@nox.session
def build_exe(session: nox.Session) -> None:
    # On non-Windows platforms, just log and exit successfully without running PyInstaller.
    if sys.platform != "win32":
        session.log("Skipping build_exe: Windows-only build.")
        return

    _install_project_editable(session)
    session.install("pyinstaller")

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
