"""Language plugin registry and helpers."""
from __future__ import annotations

from typing import Dict

from ..language_base import LanguagePlugin
from .english import EnglishLanguagePlugin
from .french import FrenchLanguagePlugin
from .spanish import SpanishLanguagePlugin

_REGISTERED_PLUGINS: Dict[str, LanguagePlugin] = {}


def register_language(plugin: LanguagePlugin) -> None:
    """Register a language plugin by its lowercase name."""
    _REGISTERED_PLUGINS[plugin.name.lower()] = plugin


register_language(EnglishLanguagePlugin())
register_language(FrenchLanguagePlugin())
register_language(SpanishLanguagePlugin())


def available_languages() -> list[str]:
    """Return the list of registered language identifiers."""
    return sorted(_REGISTERED_PLUGINS)


def get_language_plugin(name: str | None = None) -> LanguagePlugin:
    """Retrieve a language plugin by name, defaulting to English."""
    key = (name or "english").lower()
    if key not in _REGISTERED_PLUGINS:
        raise ValueError(
            f"Unknown language '{name}'. Available languages: {', '.join(available_languages())}."
        )
    return _REGISTERED_PLUGINS[key]


__all__ = ["available_languages", "get_language_plugin", "register_language"]
