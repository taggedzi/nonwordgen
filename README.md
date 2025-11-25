# nonwordgen

`nonwordgen` generates pseudo-words using a syllable-based phonotactic model and filters that attempt to discard real vocabulary via pluggable dictionary backends. The generator now loads language capabilities via plugins; each plugin ships with syllable inventories that include the native orthography (accents, umlauts, etc.) so the resulting strings look appropriate for the selected language.

## Installation

The package is pure Python and ships wheels for Windows, macOS, and Linux.

```bash
python -m pip install nonwordgen                 # base install
python -m pip install "nonwordgen[gui]"         # add PyQt6 for the GUI
python -m pip install "nonwordgen[dictionaries]"  # richer dictionary filtering
```

From a clone of this repository you can install in editable mode for development:

```bash
python -m pip install -e ".[dev]"
```

## Library usage

```python
from nonwordgen import WordGenerator, Strictness

gen = WordGenerator(
    min_length=5,
    max_length=9,
    strictness=Strictness.MEDIUM,
    language="english",  # default plugin
)

print(gen.generate_one())
print(gen.generate_many(10))
```

## CLI usage

```bash
# Words (English default)
nonwordgen -n 20 --min-length 4 --max-length 8 --strictness strict

# Words (Spanish)
nonwordgen -n 20 --min-length 4 --max-length 8 --strictness strict --language spanish

# Sentences
nonwordgen sentences -n 5 --language french --min-words 3 --max-words 8

# Paragraphs
nonwordgen paragraphs -p 2 --min-sentences 2 --max-sentences 4 --language german

# Launch GUI (requires PyQt6)
nonwordgen gui
```

## Languages

Available plugins: `english` (default), `spanish`, `french`, `portuguese`, `indonesian`, `swahili`, `german`, `turkish`, `russian`, `vietnamese`, `hindi`, `korean`, `italian`, `dutch`, `tagalog`, `romanian`, `swedish`, `norwegian`, `danish`, `afrikaans`, `yoruba`, `polish`, `czech`, `hungarian`, `greek`, `thai`, `hebrew`, `scb`, and `malay`. The CLI lists valid options via `--help`, and the Python API exposes `nonwordgen.available_languages()` if you need to inspect them programmatically.

## Optional dependencies

The package works out of the box with a small built-in dictionary. Installing the optional extras improves real-word detection:

- `wordfreq` enables frequency-based filtering (install via `pip install "nonwordgen[dictionaries]"`).
- `wordset` contributes a larger English word list if you happen to have that package available separately.
- `PyQt6` enables the GUI (`pip install "nonwordgen[gui]"`).

## Development

Run the test suite with:

```bash
pytest
```

To build distributable artifacts (wheel + sdist) locally:

```bash
python -m pip install --upgrade build
python -m build
```

The resulting files will be written to `dist/` and can be uploaded to an index such as PyPI with a tool like `twine`.

## Release process

nonwordgen uses a standard Python packaging and GitHub-based release flow.

1. Choose a new version  
   - Decide the next version number (for example `0.2.0`).  
   - Edit `nonwordgen/__init__.py` and update `__version__ = "0.2.0"`.  
   - Optionally update the README or changelog to describe the changes.

2. Run tests and build artifacts  
   ```bash
   pytest
   python -m pip install --upgrade build
   python -m build
   ```
   - This creates `dist/nonwordgen-<version>-py3-none-any.whl` and `dist/nonwordgen-<version>.tar.gz`.

3. Commit and tag the release  
   ```bash
   git status
   git add nonwordgen/__init__.py README.md
   git commit -m "Release v0.2.0"
   git tag -a v0.2.0 -m "Release v0.2.0"
   git push origin main --tags
   ```

4. Create a GitHub Release  
   - In the GitHub UI, go to “Releases” → “Draft a new release”.  
   - Select the tag you just pushed (e.g. `v0.2.0`) or create it there.  
   - Set the release title (for example `nonwordgen v0.2.0`) and description (high‑level changelog).  
   - Attach the built artifacts from `dist/` (`.whl` and `.tar.gz`) so users can download them directly.  
   - Publish the release.

5. (Optional) Upload to PyPI  
   ```bash
   python -m pip install --upgrade twine
   python -m twine upload dist/*
   ```
   - This makes the new version installable via `pip install nonwordgen` and `pip install "nonwordgen[gui]"`, etc.

All package data (including the GUI icon under `nonwordgen/assets/`) is included automatically in the built distributions by virtue of the `pyproject.toml` and `MANIFEST.in` configuration.

## License

Released under the MIT License. See `LICENSE` for details.

## AI disclosures

Parts of the project documentation and build guidance were drafted with generative AI assistance (OpenAI’s models) and reviewed before publication.

## Third-party notices

- **PyQt6** (GUI) – provided by The Qt Company under the GNU GPL v3 (or a commercial license) and LGPL-compatible runtime components; install via `pip install PyQt6>=6.5`.
- **wordfreq** (dictionary filtering) – MIT licensed; install via `pip install "nonwordgen[dictionaries]"`.
- **wordset** (optional large English word list) – follow that project’s license when you include it (it is treated as an optional, external dependency).

The optional extras above are not bundled in the base package but are clearly documented so users can install them when needed; their respective distributions contain the full license text you can inspect on PyPI or their source repositories. Any additional third-party assets (language inventories, help icon) ship under their original license via the hosting packages.
