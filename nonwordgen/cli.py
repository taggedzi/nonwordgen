"""Command-line interface for nonwordgen."""
from __future__ import annotations

import argparse
import random
from typing import Sequence

from .config import Strictness
from .generator import WordGenerator
from .languages import available_languages


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate English-like non-words from the command line."
    )
    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=10,
        help="Number of non-words to generate (default: 10).",
    )
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


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point for the console script."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    rng = random.Random(args.seed) if args.seed is not None else None
    generator = WordGenerator(
        min_length=args.min_length,
        max_length=args.max_length,
        min_syllables=args.min_syllables,
        max_syllables=args.max_syllables,
        strictness=Strictness(args.strictness),
        allow_real_words=args.allow_real_words,
        rng=rng,
        language=args.language,
    )

    for word in generator.generate_many(args.count):
        print(word)

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
