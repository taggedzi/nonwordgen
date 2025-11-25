"""Configuration helpers bridging user-facing APIs and language plugins."""
from __future__ import annotations

from .dictionary_base import DictionaryBackend
from .language_base import LanguagePlugin
from .languages import get_language_plugin
from .strictness import Strictness

__all__ = ["Strictness", "build_dictionary_for_strictness"]


def build_dictionary_for_strictness(
    strictness: Strictness,
    real_word_min_zipf: float = 2.7,
    *,
    language: str = "english",
    language_plugin: LanguagePlugin | None = None,
) -> DictionaryBackend:
    """Build a dictionary backend using the chosen language plugin."""
    plugin = language_plugin or get_language_plugin(language)
    return plugin.build_dictionary(strictness, real_word_min_zipf)
