# SPDX-License-Identifier: MIT
"""Indonesian language plugin implementation."""

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

INDONESIAN_ONSETS = [
    "",
    "b",
    "c",
    "d",
    "f",
    "g",
    "h",
    "j",
    "k",
    "l",
    "m",
    "n",
    "p",
    "r",
    "s",
    "t",
    "w",
    "y",
    "bl",
    "br",
    "dr",
    "gr",
    "kl",
    "kr",
    "pl",
    "pr",
    "tr",
    "ny",
    "ng",
]

INDONESIAN_NUCLEI = [
    "a",
    "e",
    "i",
    "o",
    "u",
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

INDONESIAN_CODAS = [
    "",
    "h",
    "k",
    "l",
    "m",
    "n",
    "ng",
    "ny",
    "r",
    "s",
    "t",
]

COMMON_INDONESIAN_WORDS = [
    "halo",
    "terima",
    "kasih",
    "rumah",
    "anak",
    "orang",
    "air",
    "api",
    "tanah",
    "langit",
    "teman",
    "keluarga",
    "waktu",
    "cinta",
    "hidup",
    "ibu",
    "ayah",
    "kakak",
    "adik",
    "makan",
    "minum",
    "banyak",
    "sedikit",
    "ya",
    "tidak",
    "satu",
    "dua",
    "tiga",
]


class IndonesianLanguagePlugin(LanguagePlugin):
    """Language plugin providing an Indonesian-flavored generator."""

    name = "indonesian"

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
            INDONESIAN_ONSETS,
            INDONESIAN_NUCLEI,
            INDONESIAN_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [
            StaticWordSetDictionary(COMMON_INDONESIAN_WORDS)
        ]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(
                real_word_min_zipf=threshold, language="id"
            )
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Indonesian; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["IndonesianLanguagePlugin"]
