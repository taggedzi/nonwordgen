"""Hungarian language plugin implementation."""
from __future__ import annotations

import logging
import random

from ..dictionary_base import DictionaryBackend
from ..dictionaries import CompositeDictionary, StaticWordSetDictionary, WordfreqDictionary
from ..language_base import LanguagePlugin
from ..phonotactics import build_candidate_from_profile
from ..strictness import Strictness

logger = logging.getLogger(__name__)

HUNGARIAN_ONSETS = [
    "",
    "b",
    "c",
    "cs",
    "d",
    "dz",
    "dzs",
    "f",
    "g",
    "gy",
    "h",
    "j",
    "k",
    "l",
    "ly",
    "m",
    "n",
    "ny",
    "p",
    "r",
    "s",
    "sz",
    "t",
    "ty",
    "v",
    "z",
    "zs",
]

HUNGARIAN_NUCLEI = [
    "a",
    "e",
    "i",
    "o",
    "u",
    "á",
    "é",
    "í",
    "ó",
    "ö",
    "ő",
    "ú",
    "ü",
    "ű",
    "ia",
    "ie",
    "io",
    "ua",
    "ue",
]

HUNGARIAN_CODAS = [
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
    "sz",
    "cs",
    "zs",
    "nd",
    "ng",
    "nk",
    "nt",
    "st",
    "rs",
    "rt",
    "rm",
]

COMMON_HUNGARIAN_WORDS = [
    "szia",
    "köszönöm",
    "kérem",
    "ház",
    "kutya",
    "macska",
    "nő",
    "férfi",
    "víz",
    "tűz",
    "levegő",
    "föld",
    "barát",
    "barátnő",
    "éj",
    "nap",
    "idő",
    "munka",
    "világ",
    "család",
    "szerelem",
    "élet",
    "anya",
    "apa",
    "fiútestvér",
    "lánytestvér",
    "sok",
    "kevés",
    "igen",
    "nem",
    "egy",
    "kettő",
    "három",
]


class HungarianLanguagePlugin(LanguagePlugin):
    """Language plugin providing a Hungarian-flavored generator."""

    name = "hungarian"

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
            HUNGARIAN_ONSETS,
            HUNGARIAN_NUCLEI,
            HUNGARIAN_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [StaticWordSetDictionary(COMMON_HUNGARIAN_WORDS)]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(real_word_min_zipf=threshold, language="hu")
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Hungarian; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["HungarianLanguagePlugin"]
