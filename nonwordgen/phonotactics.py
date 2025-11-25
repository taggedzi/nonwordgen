"""Syllable-based candidate builder for pseudo-English words."""
from __future__ import annotations

import random
from typing import Sequence

ONSETS: Sequence[str] = [
    "",
    "b",
    "c",
    "d",
    "f",
    "g",
    "h",
    "j",
    "k",
    "l",
    "m",
    "n",
    "p",
    "q",
    "r",
    "s",
    "t",
    "v",
    "w",
    "y",
    "z",
    "bl",
    "br",
    "cl",
    "cr",
    "dr",
    "fl",
    "fr",
    "gl",
    "gr",
    "pl",
    "pr",
    "sl",
    "sm",
    "sn",
    "sp",
    "st",
    "str",
    "sw",
    "tr",
    "ch",
    "sh",
    "th",
    "wh",
]

NUCLEI: Sequence[str] = [
    "a",
    "e",
    "i",
    "o",
    "u",
    "aa",
    "ae",
    "ai",
    "au",
    "ea",
    "ee",
    "ei",
    "ia",
    "ie",
    "io",
    "oa",
    "oe",
    "oi",
    "oo",
    "ou",
    "ua",
    "ue",
    "ui",
]

CODAS: Sequence[str] = [
    "",
    "b",
    "d",
    "f",
    "g",
    "h",
    "k",
    "l",
    "m",
    "n",
    "p",
    "r",
    "s",
    "t",
    "v",
    "x",
    "y",
    "z",
    "ck",
    "ft",
    "ld",
    "lk",
    "lm",
    "lp",
    "lt",
    "mp",
    "nd",
    "ng",
    "nk",
    "nt",
    "pt",
    "rd",
    "rk",
    "rn",
    "rst",
    "rt",
    "sh",
    "sk",
    "sp",
    "st",
    "th",
    "ts",
    "ch",
]

_MAX_PATTERN_ATTEMPTS = 8


def _has_ugly_patterns(word: str) -> bool:
    """Return True if the candidate contains obviously ugly character runs."""
    lowered = word.lower()
    if len(lowered) < 3:
        return False
    for idx in range(len(lowered) - 2):
        if lowered[idx] == lowered[idx + 1] == lowered[idx + 2]:
            return True
    if "qq" in lowered or "yyy" in lowered:
        return True
    return False


def build_candidate_from_profile(
    rng: random.Random,
    min_syllables: int,
    max_syllables: int,
    max_length: int,
    onsets: Sequence[str],
    nuclei: Sequence[str],
    codas: Sequence[str],
) -> str:
    """Build a candidate word using the provided syllable profile."""
    if min_syllables < 1:
        raise ValueError("min_syllables must be at least 1.")
    if min_syllables > max_syllables:
        raise ValueError("min_syllables cannot exceed max_syllables.")
    if max_length < 1:
        raise ValueError("max_length must be at least 1.")

    last_candidate = ""
    for _ in range(_MAX_PATTERN_ATTEMPTS):
        syllable_target = rng.randint(min_syllables, max_syllables)
        pieces: list[str] = []
        length_so_far = 0

        for _ in range(syllable_target):
            onset = rng.choice(onsets)
            nucleus = rng.choice(nuclei)
            coda = rng.choice(codas)
            syllable = f"{onset}{nucleus}{coda}"
            projected_length = length_so_far + len(syllable)
            if projected_length > max_length and pieces:
                break
            pieces.append(syllable)
            length_so_far = projected_length
            if length_so_far >= max_length:
                break

        candidate = "".join(pieces).lower()
        if len(candidate) > max_length:
            candidate = candidate[:max_length]
        if not candidate:
            continue

        last_candidate = candidate
        if not _has_ugly_patterns(candidate):
            return candidate

    return last_candidate or rng.choice(nuclei).lower()


def build_candidate(
    rng: random.Random,
    min_syllables: int,
    max_syllables: int,
    max_length: int,
) -> str:
    """Build an English-style candidate word."""
    return build_candidate_from_profile(
        rng,
        min_syllables,
        max_syllables,
        max_length,
        ONSETS,
        NUCLEI,
        CODAS,
    )


__all__ = ["build_candidate", "build_candidate_from_profile"]
