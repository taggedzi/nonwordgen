from __future__ import annotations

from types import SimpleNamespace

import pytest

from nonwordgen.config import ConfigError, validate_config


def test_validate_config_accepts_valid_ranges() -> None:
    cfg = SimpleNamespace(
        min_length=4,
        max_length=10,
        min_syllables=1,
        max_syllables=3,
        min_words=2,
        max_words=5,
        min_sentences=1,
        max_sentences=3,
    )

    # Should not raise for a valid configuration.
    validate_config(cfg)


def test_validate_config_rejects_invalid_word_length_range() -> None:
    cfg = SimpleNamespace(
        min_length=10,
        max_length=5,
        min_syllables=1,
        max_syllables=3,
    )

    with pytest.raises(ConfigError) as excinfo:
        validate_config(cfg)

    message = str(excinfo.value)
    assert "Word length" in message
    assert "min value 10 cannot be greater than max value 5" in message


def test_validate_config_rejects_invalid_syllable_range() -> None:
    cfg = SimpleNamespace(
        min_length=4,
        max_length=10,
        min_syllables=5,
        max_syllables=2,
    )

    with pytest.raises(ConfigError) as excinfo:
        validate_config(cfg)

    message = str(excinfo.value)
    assert "Syllables per word" in message


def test_validate_config_rejects_invalid_word_count_range() -> None:
    cfg = SimpleNamespace(
        min_length=4,
        max_length=10,
        min_syllables=1,
        max_syllables=3,
        min_words=10,
        max_words=5,
    )

    with pytest.raises(ConfigError) as excinfo:
        validate_config(cfg)

    message = str(excinfo.value)
    assert "Words per sentence" in message


def test_validate_config_rejects_invalid_sentence_count_range() -> None:
    cfg = SimpleNamespace(
        min_length=4,
        max_length=10,
        min_syllables=1,
        max_syllables=3,
        min_sentences=4,
        max_sentences=2,
    )

    with pytest.raises(ConfigError) as excinfo:
        validate_config(cfg)

    message = str(excinfo.value)
    assert "Sentences per paragraph" in message

