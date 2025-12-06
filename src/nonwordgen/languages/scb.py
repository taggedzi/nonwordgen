"""Serbian/Croatian/Bosnian language plugin implementation (Latin script)."""

from __future__ import annotations

import logging
import random

from ..dictionaries import (
    CompositeDictionary,
    StaticWordSetDictionary,
    WordfreqDictionary,
)
from ..dictionary_base import DictionaryBackend
from ..language_base import LanguagePlugin
from ..phonotactics import build_candidate_from_profile
from ..strictness import Strictness

logger = logging.getLogger(__name__)

SCB_ONSETS = [
    "",
    "b",
    "bl",
    "br",
    "c",
    "č",
    "ć",
    "d",
    "dr",
    "f",
    "g",
    "gl",
    "gr",
    "h",
    "j",
    "k",
    "kl",
    "kr",
    "l",
    "lj",
    "m",
    "n",
    "nj",
    "p",
    "pl",
    "pr",
    "r",
    "s",
    "š",
    "sl",
    "sm",
    "sn",
    "sp",
    "st",
    "str",
    "t",
    "tr",
    "v",
    "z",
    "ž",
]

SCB_NUCLEI = [
    "a",
    "e",
    "i",
    "o",
    "u",
    "aa",
    "io",
    "ie",
    "oa",
    "oi",
    "ua",
    "ue",
]

SCB_CODAS = [
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
    "č",
    "ć",
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

COMMON_SCB_WORDS = [
    "zdravo",
    "hvala",
    "molim",
    "kuća",
    "pas",
    "mačka",
    "žena",
    "muškarac",
    "voda",
    "vatra",
    "zrak",
    "zemlja",
    "prijatelj",
    "prijateljica",
    "noć",
    "dan",
    "vrijeme",
    "posao",
    "svijet",
    "obitelj",
    "ljubav",
    "život",
    "majka",
    "otac",
    "brat",
    "sestra",
    "mnogo",
    "malo",
    "da",
    "ne",
    "jedan",
    "dva",
    "tri",
]


class SCBLanguagePlugin(LanguagePlugin):
    """Language plugin providing a Serbian/Croatian/Bosnian-flavored generator."""

    name = "scb"

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
            SCB_ONSETS,
            SCB_NUCLEI,
            SCB_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [StaticWordSetDictionary(COMMON_SCB_WORDS)]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            # Use Croatian as representative language code for frequencies
            wordfreq_backend = WordfreqDictionary(
                real_word_min_zipf=threshold, language="hr"
            )
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for SCB; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["SCBLanguagePlugin"]
