"""Portuguese language plugin implementation."""
from __future__ import annotations

import logging
import random

from ..dictionary_base import DictionaryBackend
from ..dictionaries import CompositeDictionary, StaticWordSetDictionary, WordfreqDictionary
from ..language_base import LanguagePlugin
from ..phonotactics import build_candidate_from_profile
from ..strictness import Strictness

logger = logging.getLogger(__name__)

PORTUGUESE_ONSETS = [
    "",
    "b",
    "br",
    "c",
    "ch",
    "cl",
    "cr",
    "ç",
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
    "lh",
    "m",
    "n",
    "nh",
    "p",
    "pl",
    "pr",
    "qu",
    "r",
    "s",
    "t",
    "tr",
    "v",
    "z",
]

PORTUGUESE_NUCLEI = [
    "a",
    "e",
    "i",
    "o",
    "u",
    "á",
    "â",
    "ã",
    "à",
    "é",
    "ê",
    "í",
    "ó",
    "ô",
    "õ",
    "ú",
    "ai",
    "ei",
    "ia",
    "ie",
    "io",
    "oa",
    "oi",
    "ua",
    "ue",
    "ui",
    "ão",
    "õe",
    "ou",
    "eu",
]

PORTUGUESE_CODAS = [
    "",
    "l",
    "m",
    "n",
    "r",
    "s",
    "z",
    "ns",
    "nt",
    "rd",
    "rs",
    "rt",
    "rm",
    "x",
    "es",
    "em",
    "ão",
    "ções",
]

COMMON_PORTUGUESE_WORDS = [
    "olá",
    "adeus",
    "obrigado",
    "por",
    "favor",
    "casa",
    "cachorro",
    "gato",
    "mulher",
    "homem",
    "água",
    "terra",
    "fogo",
    "ar",
    "amigo",
    "amiga",
    "noite",
    "dia",
    "trabalho",
    "mundo",
    "família",
    "tempo",
    "amor",
    "vida",
    "mãe",
    "pai",
    "irmão",
    "irmã",
    "muito",
    "pouco",
    "sim",
    "não",
    "um",
    "dois",
    "três",
]


class PortugueseLanguagePlugin(LanguagePlugin):
    """Language plugin providing a Portuguese-flavored generator."""

    name = "portuguese"

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
            PORTUGUESE_ONSETS,
            PORTUGUESE_NUCLEI,
            PORTUGUESE_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [StaticWordSetDictionary(COMMON_PORTUGUESE_WORDS)]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(real_word_min_zipf=threshold, language="pt")
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Portuguese; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["PortugueseLanguagePlugin"]
