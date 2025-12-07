# SPDX-License-Identifier: MIT
"""Romanian language plugin implementation."""

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

ROMANIAN_ONSETS = [
    "",
    "b",
    "br",
    "c",
    "ch",
    "cl",
    "cr",
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
    "l",
    "m",
    "n",
    "p",
    "pl",
    "pr",
    "r",
    "s",
    "sc",
    "sl",
    "sm",
    "sn",
    "sp",
    "st",
    "str",
    "t",
    "tr",
    "v",
    "z",
]

ROMANIAN_NUCLEI = [
    "a",
    "e",
    "i",
    "o",
    "u",
    "ă",
    "â",
    "î",
    "ai",
    "ei",
    "ia",
    "ie",
    "io",
    "oa",
    "oi",
    "ua",
    "ui",
]

ROMANIAN_CODAS = [
    "",
    "l",
    "n",
    "r",
    "s",
    "t",
    "m",
    "p",
    "c",
    "ș",
    "ț",
    "nd",
    "nt",
    "st",
    "rs",
    "rt",
    "rm",
]

COMMON_ROMANIAN_WORDS = [
    "salut",
    "mulțumesc",
    "te rog",
    "casă",
    "câine",
    "pisică",
    "femeie",
    "bărbat",
    "apă",
    "foc",
    "aer",
    "pământ",
    "prieten",
    "prietena",
    "noapte",
    "zi",
    "timp",
    "muncă",
    "lume",
    "familie",
    "dragoste",
    "viață",
    "mamă",
    "tată",
    "frate",
    "soră",
    "mult",
    "puțin",
    "da",
    "nu",
    "unu",
    "doi",
    "trei",
]


class RomanianLanguagePlugin(LanguagePlugin):
    """Language plugin providing a Romanian-flavored generator."""

    name = "romanian"

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
            ROMANIAN_ONSETS,
            ROMANIAN_NUCLEI,
            ROMANIAN_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [
            StaticWordSetDictionary(COMMON_ROMANIAN_WORDS)
        ]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(
                real_word_min_zipf=threshold, language="ro"
            )
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Romanian; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["RomanianLanguagePlugin"]
