# SPDX-License-Identifier: MIT
"""Language plugin protocols for nonwordgen."""

from __future__ import annotations

import abc
import random

from .dictionary_base import DictionaryBackend
from .strictness import Strictness


class LanguagePlugin(abc.ABC):
    """A plugin provides phonotactics and dictionaries for a language."""

    name: str

    @abc.abstractmethod
    def build_candidate(
        self,
        rng: random.Random,
        min_syllables: int,
        max_syllables: int,
        max_length: int,
    ) -> str:
        """Return a candidate non-word obeying syllable and length limits."""

    @abc.abstractmethod
    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        """Construct the dictionary backend chain for the language."""
