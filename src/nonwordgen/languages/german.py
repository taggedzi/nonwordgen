"""German language plugin implementation."""

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

GERMAN_ONSETS = [
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
    "k",
    "kl",
    "kr",
    "l",
    "m",
    "n",
    "p",
    "pf",
    "pl",
    "pr",
    "qu",
    "r",
    "s",
    "sch",
    "sp",
    "st",
    "str",
    "t",
    "tr",
    "w",
    "z",
]

GERMAN_NUCLEI = [
    "a",
    "e",
    "i",
    "o",
    "u",
    "ä",
    "ö",
    "ü",
    "ai",
    "ei",
    "au",
    "eu",
    "äu",
]

GERMAN_CODAS = [
    "",
    "b",
    "d",
    "g",
    "h",
    "k",
    "l",
    "m",
    "n",
    "r",
    "s",
    "t",
    "x",
    "ch",
    "ld",
    "lt",
    "ng",
    "nk",
    "nt",
    "rst",
    "rt",
    "ß",
]

COMMON_GERMAN_WORDS = [
    "hallo",
    "danke",
    "bitte",
    "haus",
    "hund",
    "katze",
    "frau",
    "mann",
    "wasser",
    "feuer",
    "luft",
    "erde",
    "freund",
    "freundin",
    "tag",
    "nacht",
    "zeit",
    "arbeit",
    "welt",
    "familie",
    "liebe",
    "leben",
    "mutter",
    "vater",
    "bruder",
    "schwester",
    "viel",
    "wenig",
    "ja",
    "nein",
    "eins",
    "zwei",
    "drei",
    "mädchen",
    "groß",
    "früh",
]


class GermanLanguagePlugin(LanguagePlugin):
    """Language plugin providing a German-flavored generator."""

    name = "german"

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
            GERMAN_ONSETS,
            GERMAN_NUCLEI,
            GERMAN_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [
            StaticWordSetDictionary(COMMON_GERMAN_WORDS)
        ]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(
                real_word_min_zipf=threshold, language="de"
            )
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for German; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["GermanLanguagePlugin"]
