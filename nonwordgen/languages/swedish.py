"""Swedish language plugin implementation."""
from __future__ import annotations

import logging
import random

from ..dictionary_base import DictionaryBackend
from ..dictionaries import CompositeDictionary, StaticWordSetDictionary, WordfreqDictionary
from ..language_base import LanguagePlugin
from ..phonotactics import build_candidate_from_profile
from ..strictness import Strictness

logger = logging.getLogger(__name__)

SWEDISH_ONSETS = [
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

SWEDISH_NUCLEI = [
    "a",
    "e",
    "i",
    "o",
    "u",
    "y",
    "å",
    "ä",
    "ö",
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

SWEDISH_CODAS = [
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

COMMON_SWEDISH_WORDS = [
    "hej",
    "tack",
    "snälla",
    "hus",
    "hund",
    "katt",
    "kvinna",
    "man",
    "vatten",
    "eld",
    "luft",
    "jord",
    "vän",
    "väninna",
    "natt",
    "dag",
    "tid",
    "arbete",
    "värld",
    "familj",
    "kärlek",
    "liv",
    "mamma",
    "pappa",
    "bror",
    "syster",
    "mycket",
    "lite",
    "ja",
    "nej",
    "ett",
    "två",
    "tre",
]


class SwedishLanguagePlugin(LanguagePlugin):
    """Language plugin providing a Swedish-flavored generator."""

    name = "swedish"

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
            SWEDISH_ONSETS,
            SWEDISH_NUCLEI,
            SWEDISH_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [StaticWordSetDictionary(COMMON_SWEDISH_WORDS)]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(real_word_min_zipf=threshold, language="sv")
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Swedish; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["SwedishLanguagePlugin"]
