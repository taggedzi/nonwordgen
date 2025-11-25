"""Public API for the nonwordgen package."""
from __future__ import annotations

from .config import Strictness, build_dictionary_for_strictness
from .dictionary_base import DictionaryBackend
from .generator import WordGenerator

__all__ = [
    "DictionaryBackend",
    "Strictness",
    "WordGenerator",
    "build_dictionary_for_strictness",
]

__version__ = "0.1.0"
