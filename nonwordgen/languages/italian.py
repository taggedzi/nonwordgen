"""Italian language plugin implementation."""
from __future__ import annotations

import logging
import random

from ..dictionary_base import DictionaryBackend
from ..dictionaries import CompositeDictionary, StaticWordSetDictionary, WordfreqDictionary
from ..language_base import LanguagePlugin
from ..phonotactics import build_candidate_from_profile
from ..strictness import Strictness

logger = logging.getLogger(__name__)

ITALIAN_ONSETS = [
    "",
    "b",
    "c",
    "ch",
    "ci",
    "cl",
    "cr",
    "d",
    "f",
    "fl",
    "fr",
    "g",
    "gh",
    "gl",
    "gr",
    "l",
    "m",
    "n",
    "p",
    "pl",
    "pr",
    "qu",
    "r",
    "s",
    "sc",
    "sp",
    "st",
    "str",
    "t",
    "tr",
    "v",
    "z",
]

ITALIAN_NUCLEI = [
    "a",
    "e",
    "i",
    "o",
    "u",
    "à",
    "è",
    "é",
    "ì",
    "ò",
    "ù",
    "ai",
    "ei",
    "ia",
    "io",
    "oa",
    "oi",
    "ua",
    "ue",
]

ITALIAN_CODAS = [
    "",
    "l",
    "n",
    "r",
    "s",
    "t",
    "re",
    "le",
    "ri",
    "li",
    "lo",
    "no",
    "la",
    "ra",
]

COMMON_ITALIAN_WORDS = [
    "ciao",
    "grazie",
    "per favore",
    "casa",
    "cane",
    "gatto",
    "donna",
    "uomo",
    "acqua",
    "fuoco",
    "aria",
    "terra",
    "amico",
    "amica",
    "notte",
    "giorno",
    "tempo",
    "lavoro",
    "mondo",
    "famiglia",
    "amore",
    "vita",
    "madre",
    "padre",
    "fratello",
    "sorella",
    "molto",
    "poco",
    "sì",
    "no",
    "uno",
    "due",
    "tre",
]


class ItalianLanguagePlugin(LanguagePlugin):
    """Language plugin providing an Italian-flavored generator."""

    name = "italian"

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
            ITALIAN_ONSETS,
            ITALIAN_NUCLEI,
            ITALIAN_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [StaticWordSetDictionary(COMMON_ITALIAN_WORDS)]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(real_word_min_zipf=threshold, language="it")
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Italian; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["ItalianLanguagePlugin"]
