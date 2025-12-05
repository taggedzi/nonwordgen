"""Vietnamese language plugin implementation."""
from __future__ import annotations

import logging
import random

from ..dictionary_base import DictionaryBackend
from ..dictionaries import CompositeDictionary, StaticWordSetDictionary, WordfreqDictionary
from ..language_base import LanguagePlugin
from ..phonotactics import build_candidate_from_profile
from ..strictness import Strictness

logger = logging.getLogger(__name__)

VIETNAMESE_ONSETS = [
    "",
    "b",
    "c",
    "ch",
    "d",
    "đ",
    "g",
    "gh",
    "h",
    "k",
    "kh",
    "l",
    "m",
    "n",
    "ng",
    "nh",
    "ph",
    "qu",
    "s",
    "t",
    "th",
    "tr",
    "v",
    "x",
]

VIETNAMESE_NUCLEI = [
    "a",
    "à",
    "á",
    "ả",
    "ã",
    "ạ",
    "ă",
    "ắ",
    "ằ",
    "ẳ",
    "ẵ",
    "ặ",
    "â",
    "ấ",
    "ầ",
    "ẩ",
    "ẫ",
    "ậ",
    "e",
    "é",
    "è",
    "ẻ",
    "ẽ",
    "ẹ",
    "ê",
    "ế",
    "ề",
    "ể",
    "ễ",
    "ệ",
    "i",
    "í",
    "ì",
    "ỉ",
    "ĩ",
    "ị",
    "o",
    "ó",
    "ò",
    "ỏ",
    "õ",
    "ọ",
    "ô",
    "ố",
    "ồ",
    "ổ",
    "ỗ",
    "ộ",
    "ơ",
    "ớ",
    "ờ",
    "ở",
    "ỡ",
    "ợ",
    "u",
    "ú",
    "ù",
    "ủ",
    "ũ",
    "ụ",
    "ư",
    "ứ",
    "ừ",
    "ử",
    "ữ",
    "ự",
    "y",
    "ý",
    "ỳ",
    "ỷ",
    "ỹ",
    "ỵ",
    "ia",
    "iê",
    "ua",
    "uô",
    "ưa",
]

VIETNAMESE_CODAS = [
    "",
    "c",
    "ch",
    "m",
    "n",
    "ng",
    "nh",
    "p",
    "t",
]

COMMON_VIETNAMESE_WORDS = [
    "xin",
    "chào",
    "cảm",
    "ơn",
    "vui",
    "lòng",
    "nhà",
    "chó",
    "mèo",
    "phụ",
    "nữ",
    "đàn",
    "ông",
    "nước",
    "lửa",
    "không",
    "khí",
    "đất",
    "bạn",
    "gia",
    "đình",
    "thời",
    "gian",
    "tình",
    "yêu",
    "cuộc",
    "sống",
    "mẹ",
    "cha",
    "anh",
    "chị",
    "nhiều",
    "ít",
    "có",
    "không",
    "một",
    "hai",
    "ba",
]


class VietnameseLanguagePlugin(LanguagePlugin):
    """Language plugin providing a Vietnamese-flavored generator."""

    name = "vietnamese"

    def build_candidate(
        self,
        rng: random.Random,
        min_syllables: int,
        max_syllables: int,
        max_length: int,
    ) -> str:
        return build_candidate_from_profile(
            rng,
            min_syllables,
            max_syllables,
            max_length,
            VIETNAMESE_ONSETS,
            VIETNAMESE_NUCLEI,
            VIETNAMESE_CODAS,
        )

    def build_dictionary(
        self,
        strictness: Strictness,
        real_word_min_zipf: float = 2.7,
    ) -> DictionaryBackend:
        backends: list[DictionaryBackend] = [StaticWordSetDictionary(COMMON_VIETNAMESE_WORDS)]

        if strictness in {Strictness.MEDIUM, Strictness.STRICT, Strictness.VERY_STRICT}:
            threshold = real_word_min_zipf
            if strictness == Strictness.VERY_STRICT:
                threshold = min(real_word_min_zipf, 2.0)
            wordfreq_backend = WordfreqDictionary(real_word_min_zipf=threshold, language="vi")
            if getattr(wordfreq_backend, "available", False):
                backends.append(wordfreq_backend)
            else:
                logger.warning(
                    "wordfreq backend unavailable for Vietnamese; %s strictness is degraded.",
                    strictness.value,
                )

        if len(backends) == 1:
            return backends[0]
        return CompositeDictionary(backends)


__all__ = ["VietnameseLanguagePlugin"]
