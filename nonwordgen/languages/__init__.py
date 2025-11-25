"""Language plugin registry and helpers."""
from __future__ import annotations

from typing import Dict

from ..language_base import LanguagePlugin
from .english import EnglishLanguagePlugin
from .french import FrenchLanguagePlugin
from .german import GermanLanguagePlugin
from .hindi import HindiLanguagePlugin
from .indonesian import IndonesianLanguagePlugin
from .italian import ItalianLanguagePlugin
from .tagalog import TagalogLanguagePlugin
from .korean import KoreanLanguagePlugin
from .portuguese import PortugueseLanguagePlugin
from .spanish import SpanishLanguagePlugin
from .swahili import SwahiliLanguagePlugin
from .turkish import TurkishLanguagePlugin
from .russian import RussianLanguagePlugin
from .vietnamese import VietnameseLanguagePlugin
from .dutch import DutchLanguagePlugin
from .romanian import RomanianLanguagePlugin
from .swedish import SwedishLanguagePlugin
from .norwegian import NorwegianLanguagePlugin
from .danish import DanishLanguagePlugin
from .norwegian import NorwegianLanguagePlugin

_REGISTERED_PLUGINS: Dict[str, LanguagePlugin] = {}


def register_language(plugin: LanguagePlugin) -> None:
    """Register a language plugin by its lowercase name."""
    _REGISTERED_PLUGINS[plugin.name.lower()] = plugin


register_language(EnglishLanguagePlugin())
register_language(FrenchLanguagePlugin())
register_language(GermanLanguagePlugin())
register_language(HindiLanguagePlugin())
register_language(IndonesianLanguagePlugin())
register_language(ItalianLanguagePlugin())
register_language(TagalogLanguagePlugin())
register_language(KoreanLanguagePlugin())
register_language(PortugueseLanguagePlugin())
register_language(SpanishLanguagePlugin())
register_language(SwahiliLanguagePlugin())
register_language(TurkishLanguagePlugin())
register_language(RussianLanguagePlugin())
register_language(VietnameseLanguagePlugin())
register_language(DutchLanguagePlugin())
register_language(RomanianLanguagePlugin())
register_language(SwedishLanguagePlugin())
register_language(NorwegianLanguagePlugin())
register_language(DanishLanguagePlugin())


def available_languages() -> list[str]:
    """Return the list of registered language identifiers."""
    return sorted(_REGISTERED_PLUGINS)


def get_language_plugin(name: str | None = None) -> LanguagePlugin:
    """Retrieve a language plugin by name, defaulting to English."""
    key = (name or "english").lower()
    if key not in _REGISTERED_PLUGINS:
        raise ValueError(
            f"Unknown language '{name}'. Available languages: {', '.join(available_languages())}."
        )
    return _REGISTERED_PLUGINS[key]


__all__ = ["available_languages", "get_language_plugin", "register_language"]
