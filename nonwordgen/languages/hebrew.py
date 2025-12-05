"""Modern Hebrew language plugin implementation."""
from __future__ import annotations

import logging
import random

from ..dictionary_base import DictionaryBackend
from ..dictionaries import CompositeDictionary, StaticWordSetDictionary, WordfreqDictionary
from ..language_base import LanguagePlugin
from ..phonotactics import build_candidate_from_profile
from ..strictness import Strictness

logger = logging.getLogger(__name__)

HEBREW_ONSETS = [
    "",
    "א",
    "ב",
    "ג",
    "ד",
    "ה",
    "ו",
    "ז",
    "ח",
    "ט",
    "י",
    "כ",
    "ל",
    "מ",
    "נ",
    "ס",
    "ע",
    "פ",
    "צ",
    "ק",
    "ר",
    "ש",
    "ת",
    "פל",
    "פר",
    "בר",
    "כר",
    "דר",
    "שפ",
    "שר",
]

HEBREW_NUCLEI = [
    "א",
    "ה",
    "ו",
    "י",
    "אַ",
    "אֵ",
    "אִ",
    "או",
    "אֻ",
    "ָ",
    "ֶ",
    "ִ",
    "ֹ",
    "ֻ",
]

HEBREW_CODAS = [
    "",
    "ב",
    "ג",
    "ד",
    "ה",
    "ך",
    "ל",
    "ם",
    "ן",
    "ס",
    "ף",
    "ץ",
    "ק",
    "ר",
    "ש",
    "ת",
]

COMMON_HEBREW_WORDS = [
    "שלום",
    "תודה",
    "בבקשה",
    "בית",
    "כלב",
    "חתול",
    "אישה",
    "גבר",
    "מים",
    "אש",
    "אוויר",
    "אדמה",
    "חבר",
    "חברה",
    "לילה",
    "יום",
    "זמן",
    "עבודה",
    "עולם",
    "משפחה",
    "אהבה",
    "חיים",
    "אמא",
    "אבא",
    "אח",
    "אחות",
    "הרבה",
    "מעט",
    "כן",
    "לא",
    "אחד",
    "שניים",
    "שלושה",
]


class HebrewLanguagePlugin(LanguagePlugin):
    """Language plugin providing a Modern Hebrew-flavored generator."""

    name = "hebrew"

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
            HEBREW_ONSETS,
            HEBREW_NUCLEI,
            HEBREW_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [StaticWordSetDictionary(COMMON_HEBREW_WORDS)]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(real_word_min_zipf=threshold, language="he")
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Hebrew; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["HebrewLanguagePlugin"]
