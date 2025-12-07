# SPDX-License-Identifier: MIT
"""Tagalog/Filipino language plugin implementation."""

from __future__ import annotations

import logging
import random

from ..dictionaries import (
    CompositeDictionary,
    StaticWordSetDictionary,
    WordfreqDictionary,
)
from ..dictionary_base import DictionaryBackend
from ..language_base import LanguagePlugin
from ..phonotactics import build_candidate_from_profile
from ..strictness import Strictness

logger = logging.getLogger(__name__)

TAGALOG_ONSETS = [
    "",
    "b",
    "bl",
    "br",
    "d",
    "dr",
    "f",
    "g",
    "gl",
    "gr",
    "h",
    "k",
    "kl",
    "kr",
    "l",
    "m",
    "n",
    "p",
    "pl",
    "pr",
    "r",
    "s",
    "t",
    "tr",
    "w",
    "y",
    "ng",
]

TAGALOG_NUCLEI = [
    "a",
    "e",
    "i",
    "o",
    "u",
    "ai",
    "au",
    "ei",
    "ia",
    "io",
    "oa",
    "oi",
    "ua",
    "uo",
]

TAGALOG_CODAS = [
    "",
    "k",
    "l",
    "m",
    "n",
    "ng",
    "r",
    "s",
    "t",
]

COMMON_TAGALOG_WORDS = [
    "kamusta",
    "salamat",
    "pakiusap",
    "bahay",
    "aso",
    "pusa",
    "babae",
    "lalaki",
    "tubig",
    "apoy",
    "hangin",
    "lupa",
    "kaibigan",
    "pamilya",
    "oras",
    "trabaho",
    "mundo",
    "pagibig",
    "buhay",
    "ina",
    "ama",
    "kapatid",
    "ate",
    "kuya",
    "marami",
    "kaunti",
    "oo",
    "hindi",
    "isa",
    "dalawa",
    "tatlo",
]


class TagalogLanguagePlugin(LanguagePlugin):
    """Language plugin providing a Tagalog/Filipino-flavored generator."""

    name = "tagalog"

    def build_candidate(
        self,
        rng: random.Random,
        min_syllables: int,
        max_syllables: int,
        max_length: int,
    ) -> str:
        return build_candidate_from_profile(
            rng,
            min_syllables,
            max_syllables,
            max_length,
            TAGALOG_ONSETS,
            TAGALOG_NUCLEI,
            TAGALOG_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [
            StaticWordSetDictionary(COMMON_TAGALOG_WORDS)
        ]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(
                real_word_min_zipf=threshold, language="fil"
            )
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Tagalog; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["TagalogLanguagePlugin"]
