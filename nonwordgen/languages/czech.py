"""Czech language plugin implementation."""
from __future__ import annotations

import logging
import random

from ..dictionary_base import DictionaryBackend
from ..dictionaries import CompositeDictionary, StaticWordSetDictionary, WordfreqDictionary
from ..language_base import LanguagePlugin
from ..phonotactics import build_candidate_from_profile
from ..strictness import Strictness

logger = logging.getLogger(__name__)

CZECH_ONSETS = [
    "",
    "b",
    "bl",
    "br",
    "c",
    "ch",
    "č",
    "cr",
    "d",
    "dr",
    "f",
    "fl",
    "fr",
    "g",
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
    "ř",
    "s",
    "sl",
    "sm",
    "sn",
    "sp",
    "st",
    "str",
    "š",
    "t",
    "tr",
    "v",
    "z",
    "ž",
]

CZECH_NUCLEI = [
    "a",
    "e",
    "i",
    "o",
    "u",
    "y",
    "á",
    "é",
    "í",
    "ó",
    "ú",
    "ů",
    "ý",
    "ia",
    "io",
    "ie",
    "ou",
]

CZECH_CODAS = [
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
    "ch",
    "č",
    "š",
    "ž",
    "nd",
    "ng",
    "nk",
    "nt",
    "st",
    "rs",
    "rt",
    "rm",
]

COMMON_CZECH_WORDS = [
    "ahoj",
    "děkuji",
    "prosím",
    "dům",
    "pes",
    "kočka",
    "žena",
    "muž",
    "voda",
    "oheň",
    "vzduch",
    "země",
    "přítel",
    "přítelkyně",
    "noc",
    "den",
    "čas",
    "práce",
    "svět",
    "rodina",
    "láska",
    "život",
    "matka",
    "otec",
    "bratr",
    "sestra",
    "hodně",
    "málo",
    "ano",
    "ne",
    "jedna",
    "dva",
    "tři",
]


class CzechLanguagePlugin(LanguagePlugin):
    """Language plugin providing a Czech-flavored generator."""

    name = "czech"

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
            CZECH_ONSETS,
            CZECH_NUCLEI,
            CZECH_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [StaticWordSetDictionary(COMMON_CZECH_WORDS)]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(real_word_min_zipf=threshold, language="cs")
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Czech; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["CzechLanguagePlugin"]
