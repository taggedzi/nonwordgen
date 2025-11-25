"""Dictionary backend abstractions."""
from __future__ import annotations

import abc


class DictionaryBackend(abc.ABC):
    """Interface that decides whether a generated word already exists."""

    @abc.abstractmethod
    def is_real_word(self, word: str) -> bool:
        """Return True if *word* should be treated as a real English word."""
