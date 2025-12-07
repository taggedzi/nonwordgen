# SPDX-License-Identifier: MIT
"""Danish language plugin implementation."""

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

DANISH_ONSETS = [
    "",
    "b",
    "bl",
    "br",
    "c",
    "ch",
    "d",
    "dr",
    "f",
    "fl",
    "fr",
    "g",
    "gl",
    "gr",
    "h",
    "j",
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
    "sk",
    "sl",
    "sm",
    "sn",
    "sp",
    "st",
    "str",
    "t",
    "tr",
    "v",
]

DANISH_NUCLEI = [
    "a",
    "e",
    "i",
    "o",
    "u",
    "y",
    "æ",
    "ø",
    "å",
    "ai",
    "ei",
    "ia",
    "ie",
    "io",
    "oa",
    "oi",
    "ua",
    "ue",
]

DANISH_CODAS = [
    "",
    "l",
    "n",
    "r",
    "s",
    "t",
    "m",
    "p",
    "k",
    "g",
    "d",
    "ng",
    "nd",
    "nt",
    "st",
    "rs",
    "rt",
    "rm",
]

COMMON_DANISH_WORDS = [
    "hej",
    "tak",
    "venligst",
    "hus",
    "hund",
    "kat",
    "kvinde",
    "mand",
    "vand",
    "ild",
    "luft",
    "jord",
    "ven",
    "veninde",
    "nat",
    "dag",
    "tid",
    "arbejde",
    "verden",
    "familie",
    "kærlighed",
    "liv",
    "mor",
    "far",
    "bror",
    "søster",
    "meget",
    "lidt",
    "ja",
    "nej",
    "en",
    "to",
    "tre",
]


class DanishLanguagePlugin(LanguagePlugin):
    """Language plugin providing a Danish-flavored generator."""

    name = "danish"

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
            DANISH_ONSETS,
            DANISH_NUCLEI,
            DANISH_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [
            StaticWordSetDictionary(COMMON_DANISH_WORDS)
        ]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(
                real_word_min_zipf=threshold, language="da"
            )
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Danish; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["DanishLanguagePlugin"]
