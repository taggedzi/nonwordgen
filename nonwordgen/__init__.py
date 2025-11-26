"""Public API for the nonwordgen package."""
from __future__ import annotations

from .config import Strictness, build_dictionary_for_strictness
from .dictionary_base import DictionaryBackend
from .generator import WordGenerator
from .language_base import LanguagePlugin
from .languages import available_languages, get_language_plugin
from .textgen import (
    generate_sentence,
    generate_sentences,
    generate_paragraph,
    generate_paragraphs,
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

__version__ = "1.0.1"
