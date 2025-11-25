from __future__ import annotations

import random
from typing import Iterable, Iterator, Optional

import pytest

from nonwordgen.dictionary_base import DictionaryBackend
from nonwordgen.generator import WordGenerator
from nonwordgen.language_base import LanguagePlugin
from nonwordgen.strictness import Strictness


class AlwaysRealDictionary(DictionaryBackend):
    """Dictionary that labels every word as real to aid behavioral tests."""

    def is_real_word(self, word: str) -> bool:  # pragma: no cover - trivial
        return True


class AlwaysFalseDictionary(DictionaryBackend):
    """Dictionary that never flags words as real."""

    def is_real_word(self, word: str) -> bool:  # pragma: no cover - trivial
        return False


class StubLanguagePlugin(LanguagePlugin):
    """Language plugin that yields predetermined candidates."""

    name = "stub"

    def __init__(
        self,
        candidates: Iterable[str],
        dictionary: Optional[DictionaryBackend] = None,
    ) -> None:
        self._candidates: Iterator[str] = iter(candidates)
        self._dictionary = dictionary or AlwaysFalseDictionary()

    def build_candidate(
        self,
        rng: random.Random,
        min_syllables: int,
        max_syllables: int,
        max_length: int,
    ) -> str:
        return next(self._candidates)

    def build_dictionary(
        self, strictness: Strictness, real_word_min_zipf: float = 2.7
    ) -> DictionaryBackend:
        return self._dictionary


def test_generate_one_word() -> None:
    gen = WordGenerator(allow_real_words=True, rng=random.Random(123))
    word = gen.generate_one()
    assert isinstance(word, str)
    assert 4 <= len(word) <= 10


def test_generate_many_count() -> None:
    gen = WordGenerator(allow_real_words=True, rng=random.Random(456))
    words = gen.generate_many(5)
    assert len(words) == 5
    assert len(set(words)) == len(words)


def test_length_constraints() -> None:
    plugin = StubLanguagePlugin(["zo", "extralongword", "mistral"])
    gen = WordGenerator(
        min_length=4,
        max_length=8,
        allow_real_words=True,
        rng=random.Random(0),
        language_plugin=plugin,
    )
    assert gen.generate_one(max_attempts=3) == "mistral"


def test_banned_words() -> None:
    plugin = StubLanguagePlugin(["drale", "florin"])
    gen = WordGenerator(
        banned_words={"drale"},
        allow_real_words=True,
        rng=random.Random(0),
        language_plugin=plugin,
    )
    assert gen.generate_one(max_attempts=2) == "florin"


def test_syllable_arguments_forwarded() -> None:
    captured: dict[str, int] = {}

    class RecordingPlugin(StubLanguagePlugin):
        def build_candidate(
            self,
            rng: random.Random,
            min_syllables: int,
            max_syllables: int,
            max_length: int,
        ) -> str:
            captured["min"] = min_syllables
            captured["max"] = max_syllables
            captured["len"] = max_length
            return super().build_candidate(rng, min_syllables, max_syllables, max_length)

    plugin = RecordingPlugin(["slorn"])
    gen = WordGenerator(
        min_syllables=2,
        max_syllables=4,
        max_length=9,
        allow_real_words=True,
        rng=random.Random(0),
        language_plugin=plugin,
    )
    gen.generate_one(max_attempts=1)
    assert captured == {"min": 2, "max": 4, "len": 9}


def test_dictionary_and_allow_real_words_flag() -> None:
    plugin_blocking = StubLanguagePlugin(["delta", "delta"])
    blocking = WordGenerator(
        dictionary=AlwaysRealDictionary(),
        allow_real_words=False,
        rng=random.Random(0),
        language_plugin=plugin_blocking,
    )
    with pytest.raises(RuntimeError):
        blocking.generate_one(max_attempts=2)

    plugin_allowing = StubLanguagePlugin(["delta"])
    allowing = WordGenerator(
        dictionary=AlwaysRealDictionary(),
        allow_real_words=True,
        rng=random.Random(0),
        language_plugin=plugin_allowing,
    )
    assert allowing.generate_one(max_attempts=1) == "delta"


def test_spanish_language_plugin_generates_words() -> None:
    gen = WordGenerator(allow_real_words=True, rng=random.Random(9876), language="spanish")
    word = gen.generate_one()
    assert isinstance(word, str)
    assert len(word) >= 2


def test_available_languages_list() -> None:
    from nonwordgen import available_languages

    langs = available_languages()
    assert "english" in langs
    assert "spanish" in langs
    assert "french" in langs
    assert "portuguese" in langs


def test_french_language_plugin_generates_words() -> None:
    gen = WordGenerator(allow_real_words=True, rng=random.Random(1234), language="french")
    word = gen.generate_one()
    assert isinstance(word, str)
    assert len(word) >= 2


def test_portuguese_language_plugin_generates_words() -> None:
    gen = WordGenerator(
        allow_real_words=True,
        rng=random.Random(4321),
        language="portuguese",
    )
    word = gen.generate_one()
    assert isinstance(word, str)
    assert len(word) >= 2
