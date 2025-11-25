"""Configuration helpers for dictionary strictness."""
from __future__ import annotations

import logging
from enum import Enum

from .dictionary_base import DictionaryBackend
from .dictionaries import (
    BuiltinCommonWordsDictionary,
    CompositeDictionary,
    WordfreqDictionary,
    WordsetDictionary,
)

logger = logging.getLogger(__name__)


class Strictness(str, Enum):
    """Controls how aggressively real-word dictionaries reject candidates."""

    LOOSE = "loose"
    MEDIUM = "medium"
    STRICT = "strict"
    VERY_STRICT = "very_strict"


def build_dictionary_for_strictness(
    strictness: Strictness,
    real_word_min_zipf: float = 2.7,
) -> DictionaryBackend:
    """
    Build a dictionary backend appropriate for the requested strictness.

    Strictness levels:
    - LOOSE: only the built-in word list.
    - MEDIUM: built-in list plus wordfreq if available.
    - STRICT: medium + wordset.
    - VERY_STRICT: strict, but with a lower wordfreq threshold to flag rarer words.
    """
    backends: list[DictionaryBackend] = [BuiltinCommonWordsDictionary()]

    if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
        threshold = real_word_min_zipf
        if strictness == Strictness.VERY_STRICT:
            threshold = min(real_word_min_zipf, 2.0)
        wordfreq_backend = WordfreqDictionary(real_word_min_zipf=threshold)
        if wordfreq_backend.available:
            backends.append(wordfreq_backend)
        else:
            logger.warning(
                "wordfreq backend unavailable; %s strictness is degraded.",
                strictness.value,
            )

    if strictness in {Strictness.STRICT, Strictness.VERY_STRICT}:
        wordset_backend = WordsetDictionary()
        if wordset_backend.available:
            backends.append(wordset_backend)
        else:
            logger.warning(
                "wordset backend unavailable; %s strictness is degraded.",
                strictness.value,
            )

    if len(backends) == 1:
        return backends[0]
    return CompositeDictionary(backends)
