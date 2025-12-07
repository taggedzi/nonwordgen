# SPDX-License-Identifier: MIT
"""Swahili language plugin implementation."""

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

SWAHILI_ONSETS = [
    "",
    "b",
    "bw",
    "ch",
    "d",
    "dh",
    "f",
    "g",
    "h",
    "j",
    "k",
    "kw",
    "l",
    "m",
    "mw",
    "n",
    "ny",
    "p",
    "r",
    "s",
    "sh",
    "t",
    "tw",
    "v",
    "w",
    "y",
    "z",
]

SWAHILI_NUCLEI = [
    "a",
    "e",
    "i",
    "o",
    "u",
    "aa",
    "ai",
    "au",
    "ia",
    "ie",
    "io",
    "oa",
    "oi",
    "ua",
    "ue",
    "ui",
]

SWAHILI_CODAS = [
    "",
    "ka",
    "la",
    "ma",
    "na",
    "ra",
    "wa",
    "za",
    "li",
    "mi",
    "ni",
    "si",
]

COMMON_SWAHILI_WORDS = [
    "habari",
    "asante",
    "karibu",
    "ndio",
    "hapana",
    "rafiki",
    "nyumba",
    "mtoto",
    "mama",
    "baba",
    "kaka",
    "dada",
    "chakula",
    "maji",
    "moto",
    "ardhi",
    "anga",
    "familia",
    "wakati",
    "upendo",
    "maisha",
    "kazi",
    "mji",
    "kijiji",
    "siku",
    "usiku",
    "moja",
    "mbili",
    "tatu",
]


class SwahiliLanguagePlugin(LanguagePlugin):
    """Language plugin providing a Swahili-flavored generator."""

    name = "swahili"

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
            SWAHILI_ONSETS,
            SWAHILI_NUCLEI,
            SWAHILI_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [
            StaticWordSetDictionary(COMMON_SWAHILI_WORDS)
        ]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(
                real_word_min_zipf=threshold, language="sw"
            )
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Swahili; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["SwahiliLanguagePlugin"]
