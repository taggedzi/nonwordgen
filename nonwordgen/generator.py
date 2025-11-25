"""High-level word generator API."""
from __future__ import annotations

import random
from typing import Iterable, Optional

from .config import Strictness, build_dictionary_for_strictness
from .dictionary_base import DictionaryBackend
from .phonotactics import build_candidate


class WordGenerator:
    """Generate English-like non-words while filtering real ones."""

    def __init__(
        self,
        min_length: int = 4,
        max_length: int = 10,
        min_syllables: int = 1,
        max_syllables: int = 3,
        strictness: Strictness = Strictness.MEDIUM,
        allow_real_words: bool = False,
        banned_words: Optional[Iterable[str]] = None,
        dictionary: Optional[DictionaryBackend] = None,
        rng: Optional[random.Random] = None,
    ) -> None:
        if min_length < 1:
            raise ValueError("min_length must be at least 1.")
        if max_length < min_length:
            raise ValueError("max_length must be >= min_length.")
        if min_syllables < 1:
            raise ValueError("min_syllables must be at least 1.")
        if max_syllables < min_syllables:
            raise ValueError("max_syllables must be >= min_syllables.")

        self.min_length = min_length
        self.max_length = max_length
        self.min_syllables = min_syllables
        self.max_syllables = max_syllables
        self.strictness = strictness
        self.allow_real_words = allow_real_words
        self._dictionary = dictionary or build_dictionary_for_strictness(strictness)
        self._rng = rng or random.Random()
        self._banned_words = (
            {word.lower() for word in banned_words} if banned_words else set()
        )

    def generate_one(self, max_attempts: int = 1000) -> str:
        """Generate a single non-word, raising if the attempt budget is exhausted."""
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1.")

        for _ in range(max_attempts):
            candidate = build_candidate(
                self._rng,
                self.min_syllables,
                self.max_syllables,
                self.max_length,
            )

            if len(candidate) < self.min_length or len(candidate) > self.max_length:
                continue
            if candidate in self._banned_words:
                continue
            if not self.allow_real_words and self._dictionary.is_real_word(candidate):
                continue
            return candidate

        raise RuntimeError(
            "Unable to generate a non-word that satisfies the constraints "
            f"after {max_attempts} attempts."
        )

    def generate_many(self, count: int, unique: bool = True) -> list[str]:
        """Generate *count* words; optionally ensure they are unique."""
        if count < 1:
            raise ValueError("count must be at least 1.")

        results: list[str] = []
        seen: set[str] | None = set() if unique else None

        while len(results) < count:
            word = self.generate_one()
            if seen is not None:
                if word in seen:
                    continue
                seen.add(word)
            results.append(word)

        return results
