"""Polish language plugin implementation."""
from __future__ import annotations

import logging
import random

from ..dictionary_base import DictionaryBackend
from ..dictionaries import CompositeDictionary, StaticWordSetDictionary, WordfreqDictionary
from ..language_base import LanguagePlugin
from ..phonotactics import build_candidate_from_profile
from ..strictness import Strictness

logger = logging.getLogger(__name__)

POLISH_ONSETS = [
    "",
    "b",
    "bl",
    "br",
    "c",
    "ch",
    "cz",
    "d",
    "dr",
    "dz",
    "dź",
    "dż",
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
    "sz",
    "sl",
    "sm",
    "sn",
    "sp",
    "st",
    "str",
    "t",
    "tr",
    "w",
    "z",
    "ź",
    "ż",
]

POLISH_NUCLEI = [
    "a",
    "e",
    "i",
    "o",
    "u",
    "y",
    "ą",
    "ę",
    "ai",
    "ei",
    "io",
    "ia",
    "ie",
    "io",
    "oi",
    "ua",
    "ue",
]

POLISH_CODAS = [
    "",
    "l",
    "ł",
    "n",
    "r",
    "s",
    "t",
    "m",
    "p",
    "k",
    "g",
    "d",
    "ch",
    "sz",
    "cz",
    "dz",
    "dź",
    "dż",
    "nd",
    "ng",
    "nk",
    "nt",
    "st",
    "rs",
    "rt",
    "rm",
]

COMMON_POLISH_WORDS = [
    "cześć",
    "dziękuję",
    "proszę",
    "dom",
    "pies",
    "kot",
    "kobieta",
    "mężczyzna",
    "woda",
    "ogień",
    "powietrze",
    "ziemia",
    "przyjaciel",
    "przyjaciółka",
    "noc",
    "dzień",
    "czas",
    "praca",
    "świat",
    "rodzina",
    "miłość",
    "życie",
    "matka",
    "ojciec",
    "brat",
    "siostra",
    "dużo",
    "mało",
    "tak",
    "nie",
    "jeden",
    "dwa",
    "trzy",
]


class PolishLanguagePlugin(LanguagePlugin):
    """Language plugin providing a Polish-flavored generator."""

    name = "polish"

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
            POLISH_ONSETS,
            POLISH_NUCLEI,
            POLISH_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [StaticWordSetDictionary(COMMON_POLISH_WORDS)]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(real_word_min_zipf=threshold, language="pl")
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Polish; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["PolishLanguagePlugin"]
