# SPDX-License-Identifier: MIT
"""Thai plugin using RTGS romanization for phonotactics."""

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

THAI_ONSETS = [
    "",
    "b",
    "ch",
    "d",
    "f",
    "h",
    "k",
    "kh",
    "kr",
    "kl",
    "l",
    "m",
    "n",
    "ng",
    "p",
    "ph",
    "pr",
    "pl",
    "r",
    "s",
    "t",
    "th",
    "tr",
    "w",
    "y",
]

THAI_NUCLEI = [
    "a",
    "aa",
    "ae",
    "ai",
    "ao",
    "e",
    "ea",
    "ia",
    "i",
    "o",
    "oi",
    "oo",
    "ua",
    "u",
    "ue",
]

THAI_CODAS = [
    "",
    "k",
    "p",
    "t",
    "m",
    "n",
    "ng",
    "w",
    "y",
    "lp",
    "lt",
    "rk",
    "rt",
]

COMMON_THAI_WORDS = [
    "sawasdee",
    "khopkhun",
    "khobkhun",
    "krab",
    "kha",
    "baan",
    "ma",
    "maeo",
    "phuuying",
    "phuuchaai",
    "nam",
    "fai",
    "lom",
    "din",
    "phuan",
    "khropkhrua",
    "wela",
    "ngaan",
    "lok",
    "khwaamrak",
    "chiwit",
    "mae",
    "phoo",
    "phiichaai",
    "phiisao",
    "maak",
    "noi",
    "chai",
    "mai",
    "neung",
    "song",
    "sam",
]


class ThaiLanguagePlugin(LanguagePlugin):
    """Language plugin providing a Thai-flavored generator using RTGS forms."""

    name = "thai"

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
            THAI_ONSETS,
            THAI_NUCLEI,
            THAI_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [StaticWordSetDictionary(COMMON_THAI_WORDS)]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(
                real_word_min_zipf=threshold, language="th"
            )
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Thai; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["ThaiLanguagePlugin"]
