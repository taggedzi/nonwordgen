"""Higher-level text generation helpers built atop WordGenerator."""
from __future__ import annotations

import random
from typing import Iterable

from .generator import WordGenerator

PUNCTUATION = [".", "!", "?"]


def _rng_for_generator(generator: WordGenerator) -> random.Random:
    # Reuse the generator's RNG when possible for reproducibility
    rng = getattr(generator, "_rng", None)
    if isinstance(rng, random.Random):
        return rng
    return random.Random()


def generate_sentence(
    generator: WordGenerator,
    min_words: int = 4,
    max_words: int = 9,
) -> str:
    """Generate a pseudo-sentence by combining generated words."""
    if min_words < 1 or max_words < min_words:
        raise ValueError("word count bounds are invalid")
    rng = _rng_for_generator(generator)
    word_count = rng.randint(min_words, max_words)
    words = generator.generate_many(word_count, unique=False)
    if not words:
        return ""
    words[0] = words[0].capitalize()
    punct = rng.choice(PUNCTUATION)
    return " ".join(words) + punct


def generate_sentences(
    generator: WordGenerator,
    count: int,
    min_words: int = 4,
    max_words: int = 9,
) -> list[str]:
    """Generate multiple pseudo-sentences."""
    if count < 1:
        raise ValueError("count must be at least 1")
    return [generate_sentence(generator, min_words, max_words) for _ in range(count)]


def generate_paragraph(
    generator: WordGenerator,
    min_sentences: int = 2,
    max_sentences: int = 5,
    min_words: int = 4,
    max_words: int = 9,
) -> str:
    """Generate a paragraph composed of pseudo-sentences."""
    if min_sentences < 1 or max_sentences < min_sentences:
        raise ValueError("sentence count bounds are invalid")
    rng = _rng_for_generator(generator)
    sentence_count = rng.randint(min_sentences, max_sentences)
    sentences = generate_sentences(generator, sentence_count, min_words, max_words)
    return " ".join(sentences)


def generate_paragraphs(
    generator: WordGenerator,
    count: int,
    min_sentences: int = 2,
    max_sentences: int = 5,
    min_words: int = 4,
    max_words: int = 9,
) -> list[str]:
    """Generate multiple paragraphs."""
    if count < 1:
        raise ValueError("count must be at least 1")
    return [
        generate_paragraph(generator, min_sentences, max_sentences, min_words, max_words)
        for _ in range(count)
    ]


__all__ = [
    "generate_sentence",
    "generate_sentences",
    "generate_paragraph",
    "generate_paragraphs",
]
