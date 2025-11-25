"""Dictionary backend implementations."""
from __future__ import annotations

import logging
from typing import Any, Iterable

from .dictionary_base import DictionaryBackend

logger = logging.getLogger(__name__)

try:  # pragma: no cover - optional dependency
    from wordfreq import zipf_frequency  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    zipf_frequency = None  # type: ignore[assignment]

try:  # pragma: no cover - optional dependency
    import wordset as _wordset_module  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    _wordset_module = None


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
        require_library: bool = False,
    ) -> None:
        self.real_word_min_zipf = real_word_min_zipf
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
        score = zipf_frequency(word, "en")
        return score >= self.real_word_min_zipf


class WordsetDictionary(DictionaryBackend):
    """Dictionary backend backed by the optional wordset package."""

    def __init__(self, require_library: bool = False) -> None:
        self._words: set[str] = set()
        self._available = False
        module = _wordset_module
        if module is None:
            message = (
                "wordset is not installed; WordsetDictionary will not flag words."
            )
            if require_library:
                raise RuntimeError(message)
            logger.info(message)
            return

        words = self._load_words(module)
        if not words:
            logger.warning(
                "wordset is installed but returned no English entries; disabling backend."
            )
            return

        self._words = words
        self._available = True

    @staticmethod
    def _load_words(module: Any) -> set[str]:
        loaders = [
            getattr(module, "load", None),
            getattr(module, "words", None),
            getattr(module, "get_words", None),
        ]
        for loader in loaders:
            if not callable(loader):
                continue
            try:
                words_iter = loader("en")
            except TypeError:
                try:
                    words_iter = loader()
                except Exception:
                    continue
            except Exception:
                continue
            try:
                return {str(word).lower() for word in words_iter}
            except Exception:  # pragma: no cover - defensive
                logger.debug("Failed to coerce wordset words iterable.", exc_info=True)
                return set()
        return set()

    @property
    def available(self) -> bool:
        """Return True when an English word list was successfully loaded."""
        return self._available

    def is_real_word(self, word: str) -> bool:
        if not self._available:
            return False
        return word.lower() in self._words


class CompositeDictionary(DictionaryBackend):
    """Combine multiple dictionary backends with logical OR semantics."""

    def __init__(self, backends: Iterable[DictionaryBackend]) -> None:
        self.backends = list(backends)
        if not self.backends:
            raise ValueError("CompositeDictionary requires at least one backend.")

    def is_real_word(self, word: str) -> bool:
        return any(backend.is_real_word(word) for backend in self.backends)


__all__ = [
    "BuiltinCommonWordsDictionary",
    "WordfreqDictionary",
    "WordsetDictionary",
    "CompositeDictionary",
]
