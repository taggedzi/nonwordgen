from __future__ import annotations

import pytest

import nonwordgen.dictionaries as dictionaries_module
from nonwordgen.dictionary_base import DictionaryBackend
from nonwordgen.dictionaries import BuiltinCommonWordsDictionary, CompositeDictionary, WordfreqDictionary


class FakeDictionary(DictionaryBackend):
    """Predictable dictionary used to assert composite behavior."""

    def __init__(self, real_words: set[str]) -> None:
        self._real_words = {word.lower() for word in real_words}

    def is_real_word(self, word: str) -> bool:
        return word.lower() in self._real_words


def test_builtin_common_words_dictionary() -> None:
    backend = BuiltinCommonWordsDictionary()
    assert backend.is_real_word("the")
    assert not backend.is_real_word("florm")


def test_composite_dictionary_prefers_any_match() -> None:
    comp = CompositeDictionary([FakeDictionary({"glow"}), FakeDictionary({"brim"})])
    assert comp.is_real_word("brim")
    assert not comp.is_real_word("snarp")


def test_wordfreq_dictionary_threshold(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_zipf(word: str, lang: str) -> float:
        return 4.0 if word == "real" else 1.0

    monkeypatch.setattr(dictionaries_module, "zipf_frequency", fake_zipf)
    backend = WordfreqDictionary(real_word_min_zipf=2.5)
    assert backend.available
    assert backend.is_real_word("real")
    assert not backend.is_real_word("fake")
