# Third-party licenses and components

This document lists the main third-party components used by `nonwordgen`
and their licenses. It is provided to accompany both the source
distribution and any binary distributions (such as the `nonwords-gen.exe`
PyInstaller build of the GUI).

This file is informational only and does not replace the full license
texts of the respective projects. Please refer to the upstream projects
for the authoritative license terms.

## PyQt6

- **Purpose**: Provides the Qt-based graphical user interface toolkit
  used by the `nonwordgen` GUI.
- **Package**: `PyQt6`
- **Upstream**: https://www.riverbankcomputing.com/software/pyqt/
- **License**: GNU General Public License v3 (GPLv3), or a separate
  commercial license available from Riverbank Computing.

When the `nonwords-gen.exe` binary is built with PyInstaller, it
includes PyQt6 and therefore the distribution of that binary must
comply with the terms of the GPLv3 for the PyQt6 components it
contains. The `nonwordgen` application code itself is MIT-licensed
and GPL-compatible.

## wordfreq

- **Purpose**: Optional frequency-based filtering for dictionary
  lookups, used when the `dictionaries` extra is installed.
- **Package**: `wordfreq`
- **Upstream**: https://github.com/rspeer/wordfreq
- **License**: MIT License

If you install and redistribute `wordfreq` with your own builds, you
should include the MIT license notice from that project.

## wordset

- **Purpose**: Optional large English word list; treated as an
  external, optional dependency.
- **Package**: `wordset`
- **Upstream**: See the `wordset` project on PyPI or its source
  repository for details.
- **License**: Refer to the `wordset` project for the current license
  terms.

`wordset` is not required for normal use and is not bundled by default;
follow that project’s license if you choose to include it.

## PyInstaller

- **Purpose**: Build tool used to create standalone executables such as
  `nonwords-gen.exe`. It is not required at runtime by end users of the
  packaged binary.
- **Package**: `PyInstaller`
- **Upstream**: https://www.pyinstaller.org/
- **License**: GNU General Public License (GPL) with a special
  exception that explicitly permits using PyInstaller to build and
  distribute proprietary applications.

The PyInstaller license applies to the PyInstaller tool itself, not to
the applications built with it. The binaries produced by PyInstaller
may be licensed under terms of your choice, subject to the licenses of
the components you include (such as PyQt6).

## Project license

The `nonwordgen` project (source code, excluding bundled third-party
components) is released under the MIT License. See `LICENSE` for the
exact terms.

