from __future__ import annotations

import random

import pytest

import nonwordgen.generator as generator_module
from nonwordgen.dictionary_base import DictionaryBackend
from nonwordgen.generator import WordGenerator


class AlwaysRealDictionary(DictionaryBackend):
    """Dictionary that labels every word as real to aid behavioral tests."""

    def is_real_word(self, word: str) -> bool:  # pragma: no cover - trivial
        return True


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


def test_length_constraints(monkeypatch: pytest.MonkeyPatch) -> None:
    responses = iter(["zo", "extralongword", "mistral"])

    def fake_candidate(rng, min_s, max_s, max_len) -> str:  # type: ignore[override]
        return next(responses)

    monkeypatch.setattr(generator_module, "build_candidate", fake_candidate)
    gen = WordGenerator(
        min_length=4,
        max_length=8,
        allow_real_words=True,
        rng=random.Random(0),
    )
    assert gen.generate_one(max_attempts=3) == "mistral"


def test_banned_words(monkeypatch: pytest.MonkeyPatch) -> None:
    responses = iter(["drale", "florin"])

    def fake_candidate(rng, min_s, max_s, max_len) -> str:  # type: ignore[override]
        return next(responses)

    monkeypatch.setattr(generator_module, "build_candidate", fake_candidate)
    gen = WordGenerator(
        banned_words={"drale"},
        allow_real_words=True,
        rng=random.Random(0),
    )
    assert gen.generate_one(max_attempts=2) == "florin"


def test_syllable_arguments_forwarded(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, int] = {}

    def fake_candidate(rng, min_s, max_s, max_len) -> str:  # type: ignore[override]
        captured["min"] = min_s
        captured["max"] = max_s
        captured["len"] = max_len
        return "slorn"

    monkeypatch.setattr(generator_module, "build_candidate", fake_candidate)
    gen = WordGenerator(
        min_syllables=2,
        max_syllables=4,
        max_length=9,
        allow_real_words=True,
        rng=random.Random(0),
    )
    gen.generate_one(max_attempts=1)
    assert captured == {"min": 2, "max": 4, "len": 9}


def test_dictionary_and_allow_real_words_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_candidate(rng, min_s, max_s, max_len) -> str:  # type: ignore[override]
        return "delta"

    monkeypatch.setattr(generator_module, "build_candidate", fake_candidate)

    blocking = WordGenerator(
        dictionary=AlwaysRealDictionary(),
        allow_real_words=False,
        rng=random.Random(0),
    )
    with pytest.raises(RuntimeError):
        blocking.generate_one(max_attempts=2)

    allowing = WordGenerator(
        dictionary=AlwaysRealDictionary(),
        allow_real_words=True,
        rng=random.Random(0),
    )
    assert allowing.generate_one(max_attempts=1) == "delta"
