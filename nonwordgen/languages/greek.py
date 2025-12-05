"""Modern Greek language plugin implementation."""
from __future__ import annotations

import logging
import random

from ..dictionary_base import DictionaryBackend
from ..dictionaries import CompositeDictionary, StaticWordSetDictionary, WordfreqDictionary
from ..language_base import LanguagePlugin
from ..phonotactics import build_candidate_from_profile
from ..strictness import Strictness

logger = logging.getLogger(__name__)

GREEK_ONSETS = [
    "",
    "β",
    "γ",
    "δ",
    "ζ",
    "θ",
    "κ",
    "λ",
    "μ",
    "ν",
    "π",
    "ρ",
    "σ",
    "τ",
    "φ",
    "χ",
    "ψ",
    "μπ",
    "ντ",
    "γκ",
    "τσ",
    "τζ",
    "στ",
    "σκ",
    "σπ",
    "στρ",
    "πλ",
    "κρ",
    "τρ",
    "δρ",
]

GREEK_NUCLEI = [
    "α",
    "ε",
    "η",
    "ι",
    "ο",
    "υ",
    "ω",
    "αι",
    "ει",
    "οι",
    "ου",
    "υι",
    "αυ",
    "ευ",
    "ηυ",
]

GREEK_CODAS = [
    "",
    "ς",
    "ν",
    "ς",
    "ντ",
    "ρ",
    "λ",
    "μ",
    "ξ",
    "ψ",
    "στ",
    "ρθ",
    "ρξ",
    "ρψ",
]

COMMON_GREEK_WORDS = [
    "γεια",
    "ευχαριστώ",
    "παρακαλώ",
    "σπίτι",
    "σκύλος",
    "γάτα",
    "γυναίκα",
    "άντρας",
    "νερό",
    "φωτιά",
    "αέρας",
    "γη",
    "φίλος",
    "φίλη",
    "νύχτα",
    "μέρα",
    "ώρα",
    "δουλειά",
    "κόσμος",
    "οικογένεια",
    "αγάπη",
    "ζωή",
    "μητέρα",
    "πατέρας",
    "αδελφός",
    "αδελφή",
    "πολύ",
    "λίγο",
    "ναι",
    "όχι",
    "ένα",
    "δύο",
    "τρία",
]


class GreekLanguagePlugin(LanguagePlugin):
    """Language plugin providing a Modern Greek-flavored generator."""

    name = "greek"

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
            GREEK_ONSETS,
            GREEK_NUCLEI,
            GREEK_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [StaticWordSetDictionary(COMMON_GREEK_WORDS)]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(real_word_min_zipf=threshold, language="el")
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Greek; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["GreekLanguagePlugin"]
