"""Public API for the nonwordgen package."""

from __future__ import annotations

from importlib import metadata
from pathlib import Path

from .config import Strictness, build_dictionary_for_strictness
from .dictionary_base import DictionaryBackend
from .generator import WordGenerator
from .language_base import LanguagePlugin
from .languages import available_languages, get_language_plugin
from .textgen import (
    generate_paragraph,
    generate_paragraphs,
    generate_sentence,
    generate_sentences,
)

__all__ = [
    "DictionaryBackend",
    "LanguagePlugin",
    "Strictness",
    "WordGenerator",
    "available_languages",
    "build_dictionary_for_strictness",
    "get_language_plugin",
    "generate_sentence",
    "generate_sentences",
    "generate_paragraph",
    "generate_paragraphs",
]


def _read_version_from_pyproject() -> str | None:
    """Read the project version from pyproject.toml when running from source.

    This keeps pyproject.toml as the single source of truth while still
    allowing the package to expose __version__ during development.
    """
    try:
        # Resolve the repository root from this file's location.
        package_root = Path(__file__).resolve().parent
        project_root = package_root.parent
        pyproject_path = project_root / "pyproject.toml"
        if not pyproject_path.is_file():
            return None

        # tomllib is available in the stdlib from Python 3.11+.
        import tomllib

        with pyproject_path.open("rb") as f:
            data = tomllib.load(f)
        project = data.get("project") or {}
        version = project.get("version")
        if isinstance(version, str):
            return version
    except Exception:
        return None
    return None


try:
    # Prefer the installed package metadata when available.
    __version__ = metadata.version("nonwordgen")
except metadata.PackageNotFoundError:
    # Fallback to reading directly from pyproject.toml in a source checkout.
    _version = _read_version_from_pyproject()
    __version__ = _version if _version is not None else "0.0.0"
