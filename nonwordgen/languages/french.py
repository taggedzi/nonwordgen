"""French language plugin implementation."""
from __future__ import annotations

import logging
import random

from ..dictionary_base import DictionaryBackend
from ..dictionaries import (
    CompositeDictionary,
    StaticWordSetDictionary,
    WordfreqDictionary,
    WordsetDictionary,
)
from ..language_base import LanguagePlugin
from ..phonotactics import build_candidate_from_profile
from ..strictness import Strictness

logger = logging.getLogger(__name__)

FRENCH_ONSETS = [
    "",
    "b",
    "br",
    "bl",
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
    "qu",
    "r",
    "s",
    "t",
    "tr",
    "v",
    "vr",
]

FRENCH_NUCLEI = [
    "a",
    "e",
    "i",
    "o",
    "u",
    "y",
    "ai",
    "au",
    "ei",
    "eu",
    "ia",
    "ie",
    "io",
    "oi",
    "ou",
    "ue",
]

FRENCH_CODAS = [
    "",
    "l",
    "n",
    "r",
    "s",
    "t",
    "x",
    "z",
    "nd",
    "nt",
    "rd",
    "rt",
    "rs",
    "re",
    "que",
    "che",
]

COMMON_FRENCH_WORDS = [
    "bonjour",
    "merci",
    "bonjour",
    "pardon",
    "maison",
    "fromage",
    "vin",
    "pain",
    "eau",
    "ami",
    "amie",
    "femme",
    "homme",
    "jour",
    "nuit",
    "temps",
    "travail",
    "monde",
    "famille",
    "amour",
    "vie",
    "mere",
    "pere",
    "frere",
    "soeur",
    "beaucoup",
    "peu",
    "oui",
    "non",
    "un",
    "deux",
    "trois",
]


class FrenchLanguagePlugin(LanguagePlugin):
    """Language plugin providing a French-flavored generator."""

    name = "french"

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
            FRENCH_ONSETS,
            FRENCH_NUCLEI,
            FRENCH_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [StaticWordSetDictionary(COMMON_FRENCH_WORDS)]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(real_word_min_zipf=threshold, language="fr")
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for French; %s strictness is degraded.",
                    strictness.value,
                )

        if strictness in {Strictness.STRICT, Strictness.VERY_STRICT}:
            wordset_backend = WordsetDictionary(language="fr")
            if getattr(wordset_backend, "available", False):
                backends.append(wordset_backend)
            else:
                logger.warning(
                    "wordset backend unavailable for French; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["FrenchLanguagePlugin"]
