"""Spanish language plugin implementation."""
from __future__ import annotations

import logging
import random

from ..dictionary_base import DictionaryBackend
from ..dictionaries import CompositeDictionary, StaticWordSetDictionary, WordfreqDictionary
from ..language_base import LanguagePlugin
from ..phonotactics import build_candidate_from_profile
from ..strictness import Strictness

logger = logging.getLogger(__name__)

SPANISH_ONSETS = [
    "",
    "b",
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
    "gr",
    "gu",
    "h",
    "j",
    "l",
    "ll",
    "m",
    "n",
    "ñ",
    "p",
    "pl",
    "pr",
    "qu",
    "r",
    "rr",
    "s",
    "t",
    "tr",
    "v",
    "y",
    "z",
]

SPANISH_NUCLEI = [
    "a",
    "e",
    "i",
    "o",
    "u",
    "á",
    "é",
    "í",
    "ó",
    "ú",
    "ü",
    "ai",
    "au",
    "ei",
    "ia",
    "ie",
    "io",
    "oa",
    "oi",
    "ua",
    "ue",
    "ui",
]

SPANISH_CODAS = [
    "",
    "l",
    "n",
    "ñ",
    "r",
    "s",
    "z",
    "m",
    "d",
    "t",
    "x",
    "ch",
    "ns",
    "nt",
    "rd",
    "rl",
    "rs",
    "rt",
]

COMMON_SPANISH_WORDS = [
    "hola",
    "adiós",
    "gracias",
    "por",
    "favor",
    "casa",
    "perro",
    "gato",
    "mujer",
    "hombre",
    "agua",
    "tierra",
    "fuego",
    "aire",
    "amigo",
    "amiga",
    "noche",
    "día",
    "trabajo",
    "mundo",
    "familia",
    "tiempo",
    "amor",
    "vida",
    "madre",
    "padre",
    "hermano",
    "hermana",
    "mucho",
    "poco",
    "sí",
    "no",
    "uno",
    "dos",
    "tres",
]


class SpanishLanguagePlugin(LanguagePlugin):
    """Language plugin providing a Spanish-flavored generator."""

    name = "spanish"

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
            SPANISH_ONSETS,
            SPANISH_NUCLEI,
            SPANISH_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [StaticWordSetDictionary(COMMON_SPANISH_WORDS)]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(real_word_min_zipf=threshold, language="es")
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Spanish; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["SpanishLanguagePlugin"]
