# SPDX-License-Identifier: MIT
"""Turkish language plugin implementation."""

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

TURKISH_ONSETS = [
    "",
    "b",
    "c",
    "ç",
    "d",
    "f",
    "g",
    "ğ",
    "h",
    "j",
    "k",
    "l",
    "m",
    "n",
    "p",
    "r",
    "s",
    "ş",
    "t",
    "v",
    "y",
    "z",
    "br",
    "dr",
    "gr",
    "kr",
    "pr",
    "tr",
]

TURKISH_NUCLEI = [
    "a",
    "e",
    "ı",
    "i",
    "o",
    "ö",
    "u",
    "ü",
    "ai",
    "au",
    "ei",
    "ia",
    "ie",
    "io",
    "oa",
    "oi",
    "ua",
    "ue",
]

TURKISH_CODAS = [
    "",
    "k",
    "l",
    "m",
    "n",
    "r",
    "s",
    "ş",
    "t",
    "ç",
    "rk",
    "rt",
    "rs",
    "rm",
    "nt",
]

COMMON_TURKISH_WORDS = [
    "merhaba",
    "teşekkür",
    "lütfen",
    "ev",
    "köpek",
    "kedi",
    "kadın",
    "adam",
    "su",
    "ateş",
    "hava",
    "toprak",
    "dost",
    "arkadaş",
    "gece",
    "gündüz",
    "zaman",
    "çalışma",
    "dünya",
    "aile",
    "aşk",
    "hayat",
    "anne",
    "baba",
    "kardeş",
    "abla",
    "çok",
    "az",
    "evet",
    "hayır",
    "bir",
    "iki",
    "üç",
]


class TurkishLanguagePlugin(LanguagePlugin):
    """Language plugin providing a Turkish-flavored generator."""

    name = "turkish"

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
            TURKISH_ONSETS,
            TURKISH_NUCLEI,
            TURKISH_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [
            StaticWordSetDictionary(COMMON_TURKISH_WORDS)
        ]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(
                real_word_min_zipf=threshold, language="tr"
            )
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Turkish; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["TurkishLanguagePlugin"]
