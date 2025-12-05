"""Dictionary backend implementations."""
from __future__ import annotations

import logging
from typing import Any, Iterable, Sequence

from .dictionary_base import DictionaryBackend

logger = logging.getLogger(__name__)

try:  # pragma: no cover - optional dependency
    from wordfreq import zipf_frequency  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    zipf_frequency = None  # type: ignore[assignment]


class BuiltinCommonWordsDictionary(DictionaryBackend):
    """Very small fallback dictionary containing ultra-common English words."""

    _COMMON_WORDS = {
        "about",
        "after",
        "again",
        "always",
        "because",
        "before",
        "could",
        "first",
        "from",
        "have",
        "house",
        "never",
        "other",
        "people",
        "should",
        "small",
        "their",
        "there",
        "these",
        "thing",
        "think",
        "those",
        "time",
        "under",
        "water",
        "where",
        "which",
        "with",
        "world",
        "would",
        "your",
        "the",
        "and",
        "that",
        "this",
        "what",
    }

    def is_real_word(self, word: str) -> bool:
        return word.lower() in self._COMMON_WORDS


class WordfreqDictionary(DictionaryBackend):
    """Dictionary backend powered by the optional wordfreq package."""

    def __init__(
        self,
        real_word_min_zipf: float = 2.7,
        language: str = "en",
        require_library: bool = False,
    ) -> None:
        self.real_word_min_zipf = real_word_min_zipf
        self.language = language
        self._available = zipf_frequency is not None
        if not self._available:
            message = (
                "wordfreq is not installed; WordfreqDictionary will not flag words."
            )
            if require_library:
                raise RuntimeError(message)
            logger.info(message)

    @property
    def available(self) -> bool:
        """Return True when the optional dependency is present."""
        return self._available

    def is_real_word(self, word: str) -> bool:
        if not self._available or zipf_frequency is None:
            return False
        score = zipf_frequency(word, self.language)
        return score >= self.real_word_min_zipf


class CompositeDictionary(DictionaryBackend):
    """Combine multiple dictionary backends with logical OR semantics."""

    def __init__(self, backends: Iterable[DictionaryBackend]) -> None:
        self.backends = list(backends)
        if not self.backends:
            raise ValueError("CompositeDictionary requires at least one backend.")

    def is_real_word(self, word: str) -> bool:
        return any(backend.is_real_word(word) for backend in self.backends)


class StaticWordSetDictionary(DictionaryBackend):
    """Simple dictionary that uses a provided set of words."""

    def __init__(self, words: Sequence[str]) -> None:
        if not words:
            raise ValueError("StaticWordSetDictionary requires at least one word.")
        self._words = {word.lower() for word in words}

    def is_real_word(self, word: str) -> bool:
        return word.lower() in self._words


__all__ = [
    "BuiltinCommonWordsDictionary",
    "WordfreqDictionary",
    "CompositeDictionary",
    "StaticWordSetDictionary",
]
