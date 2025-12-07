# SPDX-License-Identifier: MIT
"""Strictness levels shared across language plugins."""

from __future__ import annotations

from enum import Enum


class Strictness(str, Enum):
    """Controls how aggressively real-word dictionaries reject candidates."""

    LOOSE = "loose"
    MEDIUM = "medium"
    STRICT = "strict"
    VERY_STRICT = "very_strict"


__all__ = ["Strictness"]
