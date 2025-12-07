# SPDX-License-Identifier: MIT
"""Dictionary backend implementations."""

from __future__ import annotations

import logging
from typing import Iterable, Sequence

from .dictionary_base import DictionaryBackend

logger = logging.getLogger(__name__)

try:  # pragma: no cover - optional dependency
    from wordfreq import zipf_frequency
except Exception:  # pragma: no cover - optional dependency
    zipf_frequency = None


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
    """
    Dictionary backend that uses the `wordfreq` library to estimate whether
    a string is a 'real' word in a given language.

    If the language is not supported by wordfreq (e.g. Thai / 'th'), this
    backend automatically disables itself instead of raising.
    """

    def __init__(
        self,
        language: str = "en",
        min_zipf: float = 3.0,
        wordlist: str = "best",
        real_word_min_zipf: float | None = None,
    ) -> None:
        # Allow both the original ``min_zipf`` name and the newer
        # ``real_word_min_zipf`` keyword used by language plugins.
        effective_min_zipf = (
            real_word_min_zipf if real_word_min_zipf is not None else min_zipf
        )

        self.language = language
        self.min_zipf = effective_min_zipf
        self.wordlist = wordlist
        self._enabled = True
        # Expose an ``available`` flag so callers can cheaply test whether the
        # backend is usable, matching existing call sites that use getattr().
        self.available = False

        # If wordfreq is not installed, disable this backend immediately.
        if zipf_frequency is None:  # pragma: no cover - optional dependency
            logger.warning(
                "wordfreq is not installed; disabling WordfreqDictionary backend."
            )
            self._enabled = False
            return

        # Probe wordfreq once so unsupported languages are detected early.
        try:
            # This will trigger internal checks and cache setup. Prefer using
            # the ``wordlist`` keyword when supported, but fall back to a
            # simpler call for test doubles that do not accept it.
            try:
                zipf_frequency("probe", language, wordlist=wordlist)
            except TypeError:
                zipf_frequency("probe", language)
        except LookupError:
            logger.warning(
                "wordfreq lookup failed for language %r (no %r wordlist); "
                "disabling WordfreqDictionary.",
                language,
                wordlist,
            )
            self._enabled = False
        except Exception:
            # Any unexpected errors -> disable, but keep the app running.
            logger.exception(
                "Unexpected error while initializing WordfreqDictionary for %r; "
                "disabling WordfreqDictionary.",
                language,
            )
            self._enabled = False
        else:
            self.available = True

    def is_real_word(self, word: str) -> bool:
        """
        Return True if `word` is judged to be a real word by wordfreq.

        For unsupported languages or if wordfreq fails, returns False and
        permanently disables the backend.
        """
        if not self._enabled:
            # If we know this backend is unusable, don't even try.
            return False

        try:
            try:
                score = zipf_frequency(word, self.language, wordlist=self.wordlist)
            except TypeError:
                score = zipf_frequency(word, self.language)
        except LookupError:
            # This can happen if the language *seemed* okay during probing
            # but fails when actually loading the frequency list.
            logger.warning(
                "wordfreq raised LookupError for language %r during lookup; "
                "disabling WordfreqDictionary.",
                self.language,
            )
            self._enabled = False
            return False
        except Exception:
            # Any other runtime issue in wordfreq: log and degrade only this backend.
            logger.exception(
                "wordfreq errored for language %r and word %r; "
                "disabling WordfreqDictionary for this run.",
                self.language,
                word,
            )
            self._enabled = False
            return False

        return score >= self.min_zipf


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
