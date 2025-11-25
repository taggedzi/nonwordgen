"""Public API for the nonwordgen package."""
from __future__ import annotations

from .config import Strictness, build_dictionary_for_strictness
from .dictionary_base import DictionaryBackend
from .generator import WordGenerator
from .language_base import LanguagePlugin
from .languages import available_languages, get_language_plugin

__all__ = [
    "DictionaryBackend",
    "LanguagePlugin",
    "Strictness",
    "WordGenerator",
    "available_languages",
    "build_dictionary_for_strictness",
    "get_language_plugin",
]

__version__ = "0.1.0"
