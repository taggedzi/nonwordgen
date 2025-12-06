"""Afrikaans language plugin implementation."""

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

AFRIKAANS_ONSETS = [
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

AFRIKAANS_NUCLEI = [
    "a",
    "e",
    "i",
    "o",
    "u",
    "aa",
    "ee",
    "oo",
    "oe",
    "ei",
    "ui",
    "ou",
    "ê",
    "ô",
    "û",
]

AFRIKAANS_CODAS = [
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
    "nd",
    "ng",
    "nk",
    "nt",
    "st",
    "rs",
    "rt",
    "rm",
]

COMMON_AFRIKAANS_WORDS = [
    "hallo",
    "dankie",
    "asseblief",
    "huis",
    "hond",
    "kat",
    "vrou",
    "man",
    "water",
    "vuur",
    "lug",
    "grond",
    "vriend",
    "vriendin",
    "nag",
    "dag",
    "tyd",
    "werk",
    "wêreld",
    "familie",
    "liefde",
    "lewe",
    "ma",
    "pa",
    "broer",
    "suster",
    "baie",
    "bietjie",
    "ja",
    "nee",
    "een",
    "twee",
    "drie",
]


class AfrikaansLanguagePlugin(LanguagePlugin):
    """Language plugin providing an Afrikaans-flavored generator."""

    name = "afrikaans"

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
            AFRIKAANS_ONSETS,
            AFRIKAANS_NUCLEI,
            AFRIKAANS_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [
            StaticWordSetDictionary(COMMON_AFRIKAANS_WORDS)
        ]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(
                real_word_min_zipf=threshold, language="af"
            )
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Afrikaans; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["AfrikaansLanguagePlugin"]
