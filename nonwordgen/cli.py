"""Command-line interface for nonwordgen."""

from __future__ import annotations

import argparse
import random
from typing import Sequence

from .config import Strictness
from .generator import WordGenerator
from .languages import available_languages
from .textgen import (
    generate_paragraphs,
    generate_sentences,
)


def _generator_options_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--min-length",
        type=int,
        default=4,
        help="Minimum length of generated words.",
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=10,
        help="Maximum length of generated words.",
    )
    parser.add_argument(
        "--min-syllables",
        type=int,
        default=1,
        help="Minimum syllable count.",
    )
    parser.add_argument(
        "--max-syllables",
        type=int,
        default=3,
        help="Maximum syllable count.",
    )
    parser.add_argument(
        "--strictness",
        type=str,
        default=Strictness.MEDIUM.value,
        choices=[value.value for value in Strictness],
        help="Filtering strictness (loose, medium, strict, very_strict).",
    )
    parser.add_argument(
        "--allow-real-words",
        action="store_true",
        help="Allow real words to pass filtering.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Seed for the random number generator.",
    )
    parser.add_argument(
        "--language",
        type=str,
        default="english",
        choices=available_languages(),
        help="Language plugin to use (default: english).",
    )
    return parser


def _words_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=10,
        help="Number of non-words to generate (default: 10).",
    )
    return parser


def _sentences_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "-n",
        "--sentences",
        type=int,
        default=5,
        help="Number of sentences to generate (default: 5).",
    )
    parser.add_argument(
        "--min-words",
        type=int,
        default=4,
        help="Minimum words per sentence (default: 4).",
    )
    parser.add_argument(
        "--max-words",
        type=int,
        default=9,
        help="Maximum words per sentence (default: 9).",
    )
    return parser


def _paragraphs_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "-p",
        "--paragraphs",
        type=int,
        default=3,
        help="Number of paragraphs to generate (default: 3).",
    )
    parser.add_argument(
        "--min-sentences",
        type=int,
        default=2,
        help="Minimum sentences per paragraph (default: 2).",
    )
    parser.add_argument(
        "--max-sentences",
        type=int,
        default=5,
        help="Maximum sentences per paragraph (default: 5).",
    )
    parser.add_argument(
        "--min-words",
        type=int,
        default=4,
        help="Minimum words per sentence (default: 4).",
    )
    parser.add_argument(
        "--max-words",
        type=int,
        default=9,
        help="Maximum words per sentence (default: 9).",
    )
    return parser


def _build_parser() -> argparse.ArgumentParser:
    generator_parent = _generator_options_parser()
    words_parent = _words_parser()
    sentences_parent = _sentences_parser()
    paragraphs_parent = _paragraphs_parser()

    parser = argparse.ArgumentParser(
        description="Generate pseudo-words, sentences, or paragraphs from the command line.",
        parents=[generator_parent, words_parent],
    )
    subparsers = parser.add_subparsers(dest="command")
    parser.set_defaults(command="words")

    subparsers.add_parser(
        "words",
        parents=[generator_parent, words_parent],
        help="Generate words (default)",
    )

    subparsers.add_parser(
        "sentences",
        parents=[generator_parent, sentences_parent],
        help="Generate pseudo-sentences",
    )

    subparsers.add_parser(
        "paragraphs",
        parents=[generator_parent, paragraphs_parent],
        help="Generate pseudo-paragraphs",
    )

    subparsers.add_parser(
        "gui",
        parents=[generator_parent],
        help="Launch the PyQt GUI",
    )

    return parser


def _build_generator(args: argparse.Namespace) -> WordGenerator:
    rng = random.Random(args.seed) if args.seed is not None else None
    return WordGenerator(
        min_length=args.min_length,
        max_length=args.max_length,
        min_syllables=args.min_syllables,
        max_syllables=args.max_syllables,
        strictness=Strictness(args.strictness),
        allow_real_words=args.allow_real_words,
        rng=rng,
        language=args.language,
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point for the console script."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "gui":
        try:
            from . import gui as gui_module
        except ImportError as exc:  # pragma: no cover - import guard
            parser.error(f"GUI support not available: {exc}")
        return gui_module.main()

    generator = _build_generator(args)

    if args.command == "sentences":
        sentences = generate_sentences(
            generator,
            count=args.sentences,
            min_words=args.min_words,
            max_words=args.max_words,
        )
        for sentence in sentences:
            print(sentence)
        return 0

    if args.command == "paragraphs":
        paragraphs = generate_paragraphs(
            generator,
            count=args.paragraphs,
            min_sentences=args.min_sentences,
            max_sentences=args.max_sentences,
            min_words=args.min_words,
            max_words=args.max_words,
        )
        for paragraph in paragraphs:
            print(paragraph)
            print()
        return 0

    # Default: words
    words = generator.generate_many(args.count)
    for word in words:
        print(word)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
