"""Launcher script for the nonwordgen GUI.

This is used as the entry point when building a standalone
Windows executable with PyInstaller so that double-clicking
the generated .exe opens the GUI directly.
"""
from __future__ import annotations

from nonwordgen.gui import main


if __name__ == "__main__":
    raise SystemExit(main())

