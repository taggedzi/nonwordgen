"""Configuration helpers bridging user-facing APIs and language plugins."""

from __future__ import annotations

from typing import Any

from .dictionary_base import DictionaryBackend
from .language_base import LanguagePlugin
from .languages import get_language_plugin
from .strictness import Strictness

__all__ = [
    "ConfigError",
    "Strictness",
    "build_dictionary_for_strictness",
    "validate_config",
]


class ConfigError(Exception):
    """Raised when the nonwordgen configuration is invalid."""

    pass


def build_dictionary_for_strictness(
    strictness: Strictness,
    real_word_min_zipf: float = 2.7,
    *,
    language: str = "english",
    language_plugin: LanguagePlugin | None = None,
) -> DictionaryBackend:
    """Build a dictionary backend using the chosen language plugin."""
    plugin = language_plugin or get_language_plugin(language)
    return plugin.build_dictionary(strictness, real_word_min_zipf)


def _validate_range(name: str, minimum: int, maximum: int) -> list[str]:
    """Validate a numeric range and return any error messages."""
    errors: list[str] = []
    if minimum < 0 or maximum < 0:
        errors.append(
            f"{name}: values must be non-negative (got min={minimum}, max={maximum})."
        )
    if minimum > maximum:
        errors.append(
            f"{name}: min value {minimum} cannot be greater than max value {maximum}."
        )
    return errors


def validate_config(cfg: Any) -> None:
    """Validate a configuration object containing generator/text parameters.

    The configuration is expected to expose attributes with the same names
    as the command-line options and GUI controls, for example:

    - min_length / max_length
    - min_syllables / max_syllables
    - min_words / max_words
    - min_sentences / max_sentences

    Only attributes that are present on *cfg* are validated.
    """

    def _maybe_validate(
        human_name: str,
        min_attr: str,
        max_attr: str,
        errors: list[str],
    ) -> None:
        if hasattr(cfg, min_attr) and hasattr(cfg, max_attr):
            minimum = getattr(cfg, min_attr)
            maximum = getattr(cfg, max_attr)
            errors.extend(_validate_range(human_name, int(minimum), int(maximum)))

    errors: list[str] = []

    _maybe_validate("Word length", "min_length", "max_length", errors)
    _maybe_validate("Syllables per word", "min_syllables", "max_syllables", errors)
    _maybe_validate("Words per sentence", "min_words", "max_words", errors)
    _maybe_validate(
        "Sentences per paragraph", "min_sentences", "max_sentences", errors
    )

    if errors:
        bullet_list = "\n".join(f"- {msg}" for msg in errors)
        message = f"Invalid configuration:\n\n{bullet_list}"
        raise ConfigError(message)
