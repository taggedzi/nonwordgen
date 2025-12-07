# SPDX-License-Identifier: MIT
from __future__ import annotations

import random

import nonwordgen.textgen as textgen
from nonwordgen.dictionary_base import DictionaryBackend
from nonwordgen.generator import WordGenerator
from nonwordgen.language_base import LanguagePlugin
from nonwordgen.strictness import Strictness


class DummyDictionary(DictionaryBackend):
    def is_real_word(self, word: str) -> bool:  # pragma: no cover - trivial
        return False


class DummyLanguage(LanguagePlugin):
    name = "dummy"

    def __init__(self) -> None:
        self._words = ["alpha", "beta", "gamma"]
        self._idx = 0

    def build_candidate(self, rng, min_syllables, max_syllables, max_length) -> str:  # type: ignore[override]
        word = self._words[self._idx % len(self._words)]
        self._idx += 1
        return word

    def build_dictionary(self, strictness: Strictness, real_word_min_zipf: float = 2.7) -> DictionaryBackend:  # type: ignore[override]
        return DummyDictionary()


class DummyGenerator(WordGenerator):
    def __init__(self) -> None:
        super().__init__(
            allow_real_words=True,
            rng=random.Random(0),
            language_plugin=DummyLanguage(),
        )


def test_generate_sentence_capitalizes_and_punctuates() -> None:
    gen = DummyGenerator()
    sentence = textgen.generate_sentence(gen, min_words=3, max_words=3)
    assert sentence[0].isupper()
    assert sentence[-1] in textgen.PUNCTUATION
    assert len(sentence.split()) == 3


def test_generate_paragraphs_chain_sentences() -> None:
    gen = DummyGenerator()
    paragraphs = textgen.generate_paragraphs(
        gen,
        count=2,
        min_sentences=2,
        max_sentences=2,
        min_words=2,
        max_words=2,
    )
    assert len(paragraphs) == 2
    for paragraph in paragraphs:
        # Each paragraph should end with punctuation from the final sentence
        assert paragraph[-1] in textgen.PUNCTUATION
        assert (
            len(paragraph.split()) >= 4
        )  # two sentences of two words each, plus punctuation
