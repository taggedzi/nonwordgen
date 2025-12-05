"""Malay language plugin implementation."""
from __future__ import annotations

import logging
import random

from ..dictionary_base import DictionaryBackend
from ..dictionaries import CompositeDictionary, StaticWordSetDictionary, WordfreqDictionary
from ..language_base import LanguagePlugin
from ..phonotactics import build_candidate_from_profile
from ..strictness import Strictness

logger = logging.getLogger(__name__)

MALAY_ONSETS = [
    "",
    "b",
    "c",
    "ch",
    "d",
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
    "ng",
    "ny",
]

MALAY_NUCLEI = [
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
    "ua",
    "ue",
    "uo",
]

MALAY_CODAS = [
    "",
    "h",
    "k",
    "l",
    "m",
    "n",
    "ng",
    "p",
    "r",
    "s",
    "t",
]

COMMON_MALAY_WORDS = [
    "hai",
    "terima",
    "kasih",
    "tolong",
    "rumah",
    "anjing",
    "kucing",
    "wanita",
    "lelaki",
    "air",
    "api",
    "udara",
    "tanah",
    "kawan",
    "keluarga",
    "masa",
    "kerja",
    "dunia",
    "cinta",
    "hidup",
    "ibu",
    "bapa",
    "abang",
    "kakak",
    "banyak",
    "sedikit",
    "ya",
    "tidak",
    "satu",
    "dua",
    "tiga",
]


class MalayLanguagePlugin(LanguagePlugin):
    """Language plugin providing a Malay-flavored generator."""

    name = "malay"

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
            MALAY_ONSETS,
            MALAY_NUCLEI,
            MALAY_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [StaticWordSetDictionary(COMMON_MALAY_WORDS)]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(real_word_min_zipf=threshold, language="ms")
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Malay; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["MalayLanguagePlugin"]
