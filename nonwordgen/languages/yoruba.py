"""Yoruba language plugin implementation."""
from __future__ import annotations

import logging
import random

from ..dictionary_base import DictionaryBackend
from ..dictionaries import CompositeDictionary, StaticWordSetDictionary, WordfreqDictionary
from ..language_base import LanguagePlugin
from ..phonotactics import build_candidate_from_profile
from ..strictness import Strictness

logger = logging.getLogger(__name__)

YORUBA_ONSETS = [
    "",
    "b",
    "d",
    "f",
    "g",
    "gb",
    "h",
    "j",
    "k",
    "l",
    "m",
    "n",
    "p",
    "r",
    "s",
    "ṣ",
    "t",
    "w",
    "y",
]

YORUBA_NUCLEI = [
    "a",
    "e",
    "ẹ",
    "i",
    "o",
    "ọ",
    "u",
    "à",
    "á",
    "è",
    "é",
    "ẹ̀",
    "ẹ́",
    "ì",
    "í",
    "ò",
    "ó",
    "ọ̀",
    "ọ́",
    "ù",
    "ú",
]

YORUBA_CODAS = [
    "",
    "n",
]

COMMON_YORUBA_WORDS = [
    "bawo",
    "ẹkáàrọ̀",
    "ẹkáàsán",
    "alafia",
    "baba",
    "ìyá",
    "ọmọ",
    "ilé",
    "ọkọ",
    "ọ̀rẹ́",
    "ọrẹ",
    "àpò",
    "ọjà",
    "ìwò",
    "òkè",
    "omi",
    "ina",
    "afẹ́fẹ́",
    "aiyé",
    "ọrun",
    "òwúrọ̀",
    "ìrọ̀lẹ́",
    "ọ̀nà",
    "ìfẹ́",
    "àánú",
    "ọjọ́",
    "owó",
]


class YorubaLanguagePlugin(LanguagePlugin):
    """Language plugin providing a Yoruba-flavored generator."""

    name = "yoruba"

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
            YORUBA_ONSETS,
            YORUBA_NUCLEI,
            YORUBA_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [StaticWordSetDictionary(COMMON_YORUBA_WORDS)]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(real_word_min_zipf=threshold, language="yo")
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Yoruba; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["YorubaLanguagePlugin"]
