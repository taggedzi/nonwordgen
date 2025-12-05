"""Russian language plugin implementation."""
from __future__ import annotations

import logging
import random

from ..dictionary_base import DictionaryBackend
from ..dictionaries import CompositeDictionary, StaticWordSetDictionary, WordfreqDictionary
from ..language_base import LanguagePlugin
from ..phonotactics import build_candidate_from_profile
from ..strictness import Strictness

logger = logging.getLogger(__name__)

RUSSIAN_ONSETS = [
    "",
    "б",
    "в",
    "г",
    "д",
    "ж",
    "з",
    "к",
    "л",
    "м",
    "н",
    "п",
    "р",
    "с",
    "т",
    "ф",
    "х",
    "ц",
    "ч",
    "ш",
    "щ",
    "бл",
    "бр",
    "гр",
    "др",
    "пр",
    "тр",
    "стр",
]

RUSSIAN_NUCLEI = [
    "а",
    "е",
    "ё",
    "и",
    "о",
    "у",
    "ы",
    "э",
    "ю",
    "я",
    "аи",
    "еи",
    "ои",
]

RUSSIAN_CODAS = [
    "",
    "б",
    "в",
    "г",
    "д",
    "ж",
    "з",
    "к",
    "л",
    "м",
    "н",
    "п",
    "р",
    "с",
    "т",
    "ф",
    "х",
    "ц",
    "ч",
    "ш",
    "щ",
    "н",
    "ст",
    "рт",
    "нд",
    "рь",
]

COMMON_RUSSIAN_WORDS = [
    "привет",
    "спасибо",
    "пожалуйста",
    "дом",
    "собака",
    "кошка",
    "женщина",
    "мужчина",
    "вода",
    "огонь",
    "воздух",
    "земля",
    "друг",
    "подруга",
    "ночь",
    "день",
    "время",
    "работа",
    "мир",
    "семья",
    "любовь",
    "жизнь",
    "мать",
    "отец",
    "брат",
    "сестра",
    "много",
    "мало",
    "да",
    "нет",
    "один",
    "два",
    "три",
]


class RussianLanguagePlugin(LanguagePlugin):
    """Language plugin providing a Russian-flavored generator."""

    name = "russian"

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
            RUSSIAN_ONSETS,
            RUSSIAN_NUCLEI,
            RUSSIAN_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [StaticWordSetDictionary(COMMON_RUSSIAN_WORDS)]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(real_word_min_zipf=threshold, language="ru")
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Russian; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["RussianLanguagePlugin"]
