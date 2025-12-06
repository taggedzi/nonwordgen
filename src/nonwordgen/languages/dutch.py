"""Dutch language plugin implementation."""

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

DUTCH_ONSETS = [
    "",
    "b",
    "bl",
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
    "sch",
    "sl",
    "sm",
    "sn",
    "sp",
    "st",
    "str",
    "t",
    "tr",
    "v",
    "vl",
    "vr",
    "w",
    "z",
]

DUTCH_NUCLEI = [
    "a",
    "e",
    "i",
    "o",
    "u",
    "aa",
    "ee",
    "oo",
    "eu",
    "ie",
    "ij",
    "oe",
    "ui",
    "ou",
    "au",
]

DUTCH_CODAS = [
    "",
    "l",
    "n",
    "r",
    "s",
    "t",
    "f",
    "g",
    "k",
    "m",
    "p",
    "ch",
    "cht",
    "nd",
    "ng",
    "nk",
    "nt",
    "rd",
    "rt",
    "st",
    "rs",
    "rm",
]

COMMON_DUTCH_WORDS = [
    "hallo",
    "dank",
    "dankjewel",
    "alsjeblieft",
    "huis",
    "hond",
    "kat",
    "vrouw",
    "man",
    "water",
    "vuur",
    "lucht",
    "aarde",
    "vriend",
    "vriendin",
    "nacht",
    "dag",
    "tijd",
    "werk",
    "wereld",
    "familie",
    "liefde",
    "leven",
    "moeder",
    "vader",
    "broer",
    "zus",
    "veel",
    "weinig",
    "ja",
    "nee",
    "een",
    "twee",
    "drie",
]


class DutchLanguagePlugin(LanguagePlugin):
    """Language plugin providing a Dutch-flavored generator."""

    name = "dutch"

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
            DUTCH_ONSETS,
            DUTCH_NUCLEI,
            DUTCH_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [
            StaticWordSetDictionary(COMMON_DUTCH_WORDS)
        ]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(
                real_word_min_zipf=threshold, language="nl"
            )
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Dutch; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["DutchLanguagePlugin"]
