# SPDX-License-Identifier: MIT
"""PyQt-based graphical interface for nonwordgen."""

from __future__ import annotations

import contextlib
import locale
import sys
from functools import partial
from importlib import resources
from types import SimpleNamespace
from typing import Any

from nonwordgen import __version__
from nonwordgen.config import ConfigError, Strictness, validate_config
from nonwordgen.generator import WordGenerator
from nonwordgen.languages import available_languages
from nonwordgen.textgen import generate_paragraphs, generate_sentences


def _lazy_import_qt():  # pragma: no cover - import guard
    try:
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QIcon, QPixmap
        from PyQt6.QtWidgets import (
            QApplication,
            QCheckBox,
            QComboBox,
            QFormLayout,
            QHBoxLayout,
            QLabel,
            QMainWindow,
            QMessageBox,
            QPlainTextEdit,
            QPushButton,
            QSpinBox,
            QTabWidget,
            QVBoxLayout,
            QWidget,
        )
    except Exception as exc:  # pragma: no cover - import guard
        raise ImportError(
            "PyQt6 is required for the GUI. Install via 'pip install PyQt6'."
        ) from exc
    return {
        "QApplication": QApplication,
        "QCheckBox": QCheckBox,
        "QComboBox": QComboBox,
        "QFormLayout": QFormLayout,
        "QHBoxLayout": QHBoxLayout,
        "QLabel": QLabel,
        "QMainWindow": QMainWindow,
        "QMessageBox": QMessageBox,
        "QPushButton": QPushButton,
        "QSpinBox": QSpinBox,
        "QTabWidget": QTabWidget,
        "QVBoxLayout": QVBoxLayout,
        "QWidget": QWidget,
        "QPlainTextEdit": QPlainTextEdit,
        "QIcon": QIcon,
        "QPixmap": QPixmap,
        "Qt": Qt,
    }


def _detect_default_language() -> str | None:
    """Best-effort detection of a suitable default language.

    Uses the operating system locale and maps it to one of the
    registered language plugin identifiers when possible.
    """
    # Map ISO language codes to plugin names
    locale_map = {
        "en": "english",
        "es": "spanish",
        "fr": "french",
        "pt": "portuguese",
        "id": "indonesian",
        "sw": "swahili",
        "de": "german",
        "tr": "turkish",
        "ru": "russian",
        "vi": "vietnamese",
        "hi": "hindi",
        "ko": "korean",
        "it": "italian",
        "nl": "dutch",
        "tl": "tagalog",
        "ro": "romanian",
        "sv": "swedish",
        "no": "norwegian",
        "da": "danish",
        "af": "afrikaans",
        "yo": "yoruba",
        "pl": "polish",
        "cs": "czech",
        "hu": "hungarian",
        "el": "greek",
        "th": "thai",
        "he": "hebrew",
        "ms": "malay",
    }

    try:
        # Try current locale first
        lang, _ = locale.getlocale()
        if not lang:
            # Fall back to default locale if necessary
            with contextlib.suppress(Exception):
                lang, _ = locale.getdefaultlocale()
    except Exception:
        lang = None

    if not lang:
        return None

    # Normalize values like "en_US", "en-US", etc.
    language_code = lang.split(".", 1)[0]
    language_code = language_code.replace("-", "_")
    language_code = language_code.split("_", 1)[0].lower()

    return locale_map.get(language_code)


class MainWindow:  # pragma: no cover - GUI heavy
    def __init__(self) -> None:
        qt = _lazy_import_qt()
        self.qt = qt
        QApplication = qt["QApplication"]
        QMainWindow = qt["QMainWindow"]
        QTabWidget = qt["QTabWidget"]
        QIcon = qt["QIcon"]
        QPixmap = qt["QPixmap"]
        QWidget = qt["QWidget"]
        QVBoxLayout = qt["QVBoxLayout"]
        QHBoxLayout = qt["QHBoxLayout"]
        QLabel = qt["QLabel"]
        QComboBox = qt["QComboBox"]
        QCheckBox = qt["QCheckBox"]
        QSpinBox = qt["QSpinBox"]

        self.app = QApplication.instance() or QApplication(sys.argv)
        self.window = QMainWindow()
        self.window.setWindowTitle("Nonword Generator")

        self._about_pixmap = None
        try:
            icon_path = resources.files("nonwordgen").joinpath("assets/nonword-gen.png")
        except Exception:
            icon_path = None
        if icon_path is not None:
            self.window.setWindowIcon(QIcon(str(icon_path)))
            self._about_pixmap = QPixmap(str(icon_path))

        menubar = self.window.menuBar()
        help_menu = menubar.addMenu("&Help")
        help_menu.addAction("About nonwordgen", self._show_about_dialog)

        central = QWidget()
        root_layout = QVBoxLayout()

        # Global controls
        control_layout = QHBoxLayout()

        self.language_combo = QComboBox()
        for lang in available_languages():
            self.language_combo.addItem(lang, lang)
        # Try to select a sensible default language based on system locale,
        # falling back to English if detection fails.
        detected_language = _detect_default_language()
        index = -1
        if detected_language is not None:
            index = self.language_combo.findData(detected_language)
        if index == -1:
            index = self.language_combo.findData("english")
        if index != -1:
            self.language_combo.setCurrentIndex(index)
        control_layout.addWidget(QLabel("Language"))
        control_layout.addWidget(self.language_combo)

        self.strictness_combo = QComboBox()
        for level in Strictness:
            self.strictness_combo.addItem(level.value, level.value)
        control_layout.addWidget(QLabel("Strictness"))
        control_layout.addWidget(self.strictness_combo)

        self.allow_real_words = QCheckBox("Allow real words")
        control_layout.addWidget(self.allow_real_words)

        self.min_length = QSpinBox()
        self.min_length.setRange(1, 64)
        self.min_length.setValue(4)
        self.max_length = QSpinBox()
        self.max_length.setRange(1, 64)
        self.max_length.setValue(10)
        control_layout.addWidget(QLabel("Min len"))
        control_layout.addWidget(self.min_length)
        control_layout.addWidget(QLabel("Max len"))
        control_layout.addWidget(self.max_length)

        self.min_syllables = QSpinBox()
        self.min_syllables.setRange(1, 10)
        self.min_syllables.setValue(1)
        self.max_syllables = QSpinBox()
        self.max_syllables.setRange(1, 10)
        self.max_syllables.setValue(3)
        control_layout.addWidget(QLabel("Min syll"))
        control_layout.addWidget(self.min_syllables)
        control_layout.addWidget(QLabel("Max syll"))
        control_layout.addWidget(self.max_syllables)

        root_layout.addLayout(control_layout)

        tabs = QTabWidget()
        tabs.addTab(self._build_words_tab(), "Words")
        tabs.addTab(self._build_sentences_tab(), "Sentences")
        tabs.addTab(self._build_paragraphs_tab(), "Paragraphs")
        root_layout.addWidget(tabs)

        central.setLayout(root_layout)
        self.window.setCentralWidget(central)

    def _show_about_dialog(self) -> None:
        QMessageBox = self.qt["QMessageBox"]
        Qt = self.qt["Qt"]

        dialog = QMessageBox(self.window)
        dialog.setWindowTitle("About nonwordgen")
        dialog.setWindowIcon(self.window.windowIcon())

        if self._about_pixmap is not None:
            scaled = self._about_pixmap.scaled(
                128,
                128,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            dialog.setIconPixmap(scaled)

        github_url = "https://github.com/taggedzi/nonwordgen"
        text = (
            "nonwordgen\n"
            f"Version: {__version__}\n\n"
            "Generate pseudo-words and text using language-aware phonotactics.\n\n"
            f"Source code (MIT) and build instructions are available at:\n"
            f"{github_url}\n\n"
            "This application binary bundles third-party components, including "
            "PyQt6 (GPLv3), wordfreq (Apache-2.0), and other libraries under their respective licenses. "
            "By distributing this binary you are also granted the rights "
            "to study, modify, and redistribute the corresponding source code "
            "under the terms of the MIT license for this project and the "
            "licenses of the included third-party components."
        )
        dialog.setText(text)
        dialog.exec()

    def _make_output_area(self):
        QPlainTextEdit = self.qt["QPlainTextEdit"]
        output = QPlainTextEdit()
        output.setReadOnly(True)
        return output

    def _build_words_tab(self):
        qt = self.qt
        QWidget = qt["QWidget"]
        QVBoxLayout = qt["QVBoxLayout"]
        QFormLayout = qt["QFormLayout"]
        QPushButton = qt["QPushButton"]
        QSpinBox = qt["QSpinBox"]

        container = QWidget()
        layout = QVBoxLayout()

        form = QFormLayout()
        self.word_count = QSpinBox()
        self.word_count.setRange(1, 1000)
        self.word_count.setValue(10)
        form.addRow("Count", self.word_count)
        layout.addLayout(form)

        btn_row = QVBoxLayout()
        self.words_output = self._make_output_area()
        generate_btn = QPushButton("Generate")
        generate_btn.clicked.connect(self._generate_words)
        copy_btn = QPushButton("Copy to clipboard")
        copy_btn.clicked.connect(partial(self._copy_output, self.words_output))
        btn_row.addWidget(generate_btn)
        btn_row.addWidget(copy_btn)

        layout.addLayout(btn_row)
        layout.addWidget(self.words_output)
        container.setLayout(layout)
        return container

    def _build_sentences_tab(self):
        qt = self.qt
        QWidget = qt["QWidget"]
        QVBoxLayout = qt["QVBoxLayout"]
        QFormLayout = qt["QFormLayout"]
        QPushButton = qt["QPushButton"]
        QSpinBox = qt["QSpinBox"]

        container = QWidget()
        layout = QVBoxLayout()

        form = QFormLayout()
        self.sentence_count = QSpinBox()
        self.sentence_count.setRange(1, 500)
        self.sentence_count.setValue(5)
        form.addRow("Sentences", self.sentence_count)

        self.min_words = QSpinBox()
        self.min_words.setRange(1, 50)
        self.min_words.setValue(4)
        self.max_words = QSpinBox()
        self.max_words.setRange(1, 50)
        self.max_words.setValue(9)
        form.addRow("Min words", self.min_words)
        form.addRow("Max words", self.max_words)

        layout.addLayout(form)

        btn_row = QVBoxLayout()
        self.sentences_output = self._make_output_area()
        generate_btn = QPushButton("Generate")
        generate_btn.clicked.connect(self._generate_sentences)
        copy_btn = QPushButton("Copy to clipboard")
        copy_btn.clicked.connect(partial(self._copy_output, self.sentences_output))
        btn_row.addWidget(generate_btn)
        btn_row.addWidget(copy_btn)

        layout.addLayout(btn_row)
        layout.addWidget(self.sentences_output)
        container.setLayout(layout)
        return container

    def _build_paragraphs_tab(self):
        qt = self.qt
        QWidget = qt["QWidget"]
        QVBoxLayout = qt["QVBoxLayout"]
        QFormLayout = qt["QFormLayout"]
        QPushButton = qt["QPushButton"]
        QSpinBox = qt["QSpinBox"]

        container = QWidget()
        layout = QVBoxLayout()

        form = QFormLayout()
        self.paragraph_count = QSpinBox()
        self.paragraph_count.setRange(1, 200)
        self.paragraph_count.setValue(3)
        form.addRow("Paragraphs", self.paragraph_count)

        self.min_sentences = QSpinBox()
        self.min_sentences.setRange(1, 50)
        self.min_sentences.setValue(2)
        self.max_sentences = QSpinBox()
        self.max_sentences.setRange(1, 50)
        self.max_sentences.setValue(5)
        form.addRow("Min sentences", self.min_sentences)
        form.addRow("Max sentences", self.max_sentences)

        self.min_words_para = QSpinBox()
        self.min_words_para.setRange(1, 50)
        self.min_words_para.setValue(4)
        self.max_words_para = QSpinBox()
        self.max_words_para.setRange(1, 50)
        self.max_words_para.setValue(9)
        form.addRow("Min words", self.min_words_para)
        form.addRow("Max words", self.max_words_para)

        layout.addLayout(form)

        btn_row = QVBoxLayout()
        self.paragraphs_output = self._make_output_area()
        generate_btn = QPushButton("Generate")
        generate_btn.clicked.connect(self._generate_paragraphs)
        copy_btn = QPushButton("Copy to clipboard")
        copy_btn.clicked.connect(partial(self._copy_output, self.paragraphs_output))
        btn_row.addWidget(generate_btn)
        btn_row.addWidget(copy_btn)

        layout.addLayout(btn_row)
        layout.addWidget(self.paragraphs_output)
        container.setLayout(layout)
        return container

    def _copy_output(self, widget) -> None:
        clipboard = self.qt["QApplication"].clipboard()
        clipboard.setText(widget.toPlainText())

    def _build_generator(self) -> WordGenerator:
        return WordGenerator(
            min_length=self.min_length.value(),
            max_length=self.max_length.value(),
            min_syllables=self.min_syllables.value(),
            max_syllables=self.max_syllables.value(),
            strictness=Strictness(self.strictness_combo.currentData()),
            allow_real_words=self.allow_real_words.isChecked(),
            language=self.language_combo.currentData(),
        )

    def _generate_words(self) -> None:
        QMessageBox = self.qt["QMessageBox"]
        cfg = SimpleNamespace(
            min_length=self.min_length.value(),
            max_length=self.max_length.value(),
            min_syllables=self.min_syllables.value(),
            max_syllables=self.max_syllables.value(),
        )
        try:
            validate_config(cfg)
        except ConfigError as exc:
            QMessageBox.warning(self.window, "Invalid settings", str(exc))
            return

        generator = self._build_generator()
        words = generator.generate_many(self.word_count.value())
        self.words_output.setPlainText("\n".join(words))

    def _generate_sentences(self) -> None:
        QMessageBox = self.qt["QMessageBox"]
        cfg = SimpleNamespace(
            min_length=self.min_length.value(),
            max_length=self.max_length.value(),
            min_syllables=self.min_syllables.value(),
            max_syllables=self.max_syllables.value(),
            min_words=self.min_words.value(),
            max_words=self.max_words.value(),
        )
        try:
            validate_config(cfg)
        except ConfigError as exc:
            QMessageBox.warning(self.window, "Invalid settings", str(exc))
            return

        generator = self._build_generator()
        sentences = generate_sentences(
            generator,
            count=self.sentence_count.value(),
            min_words=self.min_words.value(),
            max_words=self.max_words.value(),
        )
        self.sentences_output.setPlainText("\n".join(sentences))

    def _generate_paragraphs(self) -> None:
        QMessageBox = self.qt["QMessageBox"]
        cfg = SimpleNamespace(
            min_length=self.min_length.value(),
            max_length=self.max_length.value(),
            min_syllables=self.min_syllables.value(),
            max_syllables=self.max_syllables.value(),
            min_sentences=self.min_sentences.value(),
            max_sentences=self.max_sentences.value(),
            min_words=self.min_words_para.value(),
            max_words=self.max_words_para.value(),
        )
        try:
            validate_config(cfg)
        except ConfigError as exc:
            QMessageBox.warning(self.window, "Invalid settings", str(exc))
            return

        generator = self._build_generator()
        paragraphs = generate_paragraphs(
            generator,
            count=self.paragraph_count.value(),
            min_sentences=self.min_sentences.value(),
            max_sentences=self.max_sentences.value(),
            min_words=self.min_words_para.value(),
            max_words=self.max_words_para.value(),
        )
        self.paragraphs_output.setPlainText("\n\n".join(paragraphs))

    def run(self) -> int:
        self.window.show()
        return self.app.exec()


def main() -> int:
    """Launch the PyQt GUI."""
    try:
        window = MainWindow()
    except ImportError as exc:  # pragma: no cover - import guard
        message = f"{exc}"
        # In a console context, print a helpful error; in a frozen
        # GUI-only context (where stderr may be None), fall back to
        # a simple message box so users still see the error.
        if sys.stderr is not None:
            sys.stderr.write(message + "\n")
        else:  # pragma: no cover - Windows GUI / frozen error path
            try:
                import ctypes

                ctypes_mod: Any = ctypes
                user32 = getattr(ctypes_mod, "windll", None)
                if user32 is not None:
                    user32.user32.MessageBoxW(
                        0,
                        message,
                        "nonwordgen GUI error",
                        0x10,  # MB_ICONERROR
                    )
            except Exception:
                # As a last resort, ignore message box failures.
                pass
        return 1
    return window.run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
