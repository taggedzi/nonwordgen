# SPDX-License-Identifier: MIT
"""Hindi language plugin implementation."""

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

HINDI_ONSETS = [
    "",
    "क",
    "ख",
    "ग",
    "घ",
    "च",
    "छ",
    "ज",
    "झ",
    "ट",
    "ठ",
    "ड",
    "ढ",
    "त",
    "थ",
    "द",
    "ध",
    "न",
    "प",
    "फ",
    "ब",
    "भ",
    "म",
    "य",
    "र",
    "ल",
    "व",
    "श",
    "ष",
    "स",
    "ह",
    "त्र",
    "ज्ञ",
]

HINDI_NUCLEI = [
    "अ",
    "आ",
    "इ",
    "ई",
    "उ",
    "ऊ",
    "ऋ",
    "ए",
    "ऐ",
    "ओ",
    "औ",
    "ा",
    "ि",
    "ी",
    "ु",
    "ू",
    "े",
    "ै",
    "ो",
    "ौ",
]

HINDI_CODAS = [
    "",
    "क",
    "ख",
    "ग",
    "घ",
    "च",
    "ज",
    "ट",
    "ड",
    "त",
    "द",
    "न",
    "प",
    "फ",
    "ब",
    "भ",
    "म",
    "य",
    "र",
    "ल",
    "व",
    "स",
    "ह",
    "ँ",
    "ं",
    "ः",
]

COMMON_HINDI_WORDS = [
    "नमस्ते",
    "धन्यवाद",
    "कृपया",
    "घर",
    "कुत्ता",
    "बिल्ली",
    "महिला",
    "पुरुष",
    "पानी",
    "आग",
    "हवा",
    "धरती",
    "मित्र",
    "परिवार",
    "समय",
    "काम",
    "प्रेम",
    "जीवन",
    "मां",
    "पिता",
    "भाई",
    "बहन",
    "बहुत",
    "थोड़ा",
    "हाँ",
    "नहीं",
    "एक",
    "दो",
    "तीन",
    "शांति",
    "सपना",
]


class HindiLanguagePlugin(LanguagePlugin):
    """Language plugin providing a Hindi/Marathi-flavored generator."""

    name = "hindi"

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
            HINDI_ONSETS,
            HINDI_NUCLEI,
            HINDI_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [
            StaticWordSetDictionary(COMMON_HINDI_WORDS)
        ]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(
                real_word_min_zipf=threshold, language="hi"
            )
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Hindi; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["HindiLanguagePlugin"]
