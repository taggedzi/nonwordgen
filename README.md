# SPDX-License-Identifier: MIT
# nonwordgen

> **nonwordgen** - because real words are overrated!

---

<p align="center">
  <!-- Identity & License -->
  <img src="https://img.shields.io/badge/License-MIT-ff69b4?style=for-the-badge" />

  <!-- Platforms -->
  <img src="https://img.shields.io/badge/OS-Windows-0078D6?logo=windows&style=for-the-badge&logoColor=white" />
  <img src="https://img.shields.io/badge/OS-Linux-FCC624?logo=linux&style=for-the-badge&logoColor=black" />
  <img src="https://img.shields.io/badge/macOS-Untested-lightgrey?logo=apple&style=for-the-badge" />

  <!-- Project State -->
  <img src="https://img.shields.io/badge/Status-Actively%20Perplexing-00cc66?style=for-the-badge" />
  <img src="https://img.shields.io/github/v/release/taggedzi/nonwordgen?style=for-the-badge&color=blueviolet" />
  <img src="https://img.shields.io/github/downloads/taggedzi/nonwordgen/total?style=for-the-badge&color=orange" />
</p>

<p align="center">
  <!-- Tech Stack -->
  <img src="https://img.shields.io/badge/Python-3776ab?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Automation-NOX-7e57c2?style=for-the-badge" />
  <img src="https://img.shields.io/badge/PyInstaller-2e9afe?style=for-the-badge" />

  <!-- Quality Assurance -->
  <img src="https://img.shields.io/github/actions/workflow/status/taggedzi/nonwordgen/ci.yml?style=for-the-badge&label=Tests&color=brightgreen" />
  <img src="https://img.shields.io/github/actions/workflow/status/taggedzi/nonwordgen/release.yml?style=for-the-badge&label=Release%20Build&color=purple" />
  <img src="https://img.shields.io/badge/Lint-Ruff%20Wrangled-fc4f30?style=for-the-badge&logo=ruff&logoColor=white" />
  <img src="https://img.shields.io/badge/Typecheck-mypy-1f9aff?style=for-the-badge" />

  <!-- Fun -->
  <img src="https://img.shields.io/badge/Certified%20Fake-100%25%20Non--Words!-ff5722?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Silliness-Maximum-f50057?style=for-the-badge" />
</p>


---

`nonwordgen` is a multilingual text generator that creates **fake words, sentences, and paragraphs** that *look like* they belong to real languages - but aren’t.  
It’s ideal for **lorem ipsum–style filler text**, **UI design**, **test data**, **creative writing**, or anywhere you need realistic-looking nonsense.

Under the hood, it uses a **phonotactic syllable model**, **language plugins**, and **dictionary-based filters** to ensure generated text looks plausible while avoiding real vocabulary.  
But using it is easy: pick a language, choose strictness, and generate.

---

## ✨ Features

- ✔️ Generate **nonwords**, **sentences**, and full **paragraphs**  
- ✔️ Supports **29 languages** with accurate orthography  
- ✔️ **Plugin-based** architecture for easy language expansion  
- ✔️ Optional dictionary filtering  
- ✔️ **GUI**, **CLI**, and **Python API**  
- ✔️ Works on Windows and Linux

**macOS users:**  
The project will probably run on macOS, but I don’t have access to a Mac to test or build for it.  
If you're a macOS user and try it out, feedback is appreciated!

---

## 📥 Installation

Since `nonwordgen` is not yet published to PyPI, download it directly from **GitHub Releases**:

➡ **Download the latest wheel or source package:**  
[nonwordgen Releases](https://github.com/taggedzi/nonwordgen/releases)

Install using pip (point to your downloaded file):

```bash
# Install from wheel
python -m pip install nonwordgen-<version>-py3-none-any.whl

# Or install from source
python -m pip install nonwordgen-<version>.tar.gz
````

For development:

```bash
git clone https://github.com/taggedzi/nonwordgen.git
cd nonwordgen
python -m pip install -e ".[dev]"
```

Extras are available if you want GUI or dictionary support during development as well:

```bash
# GUI support
python -m pip install ".[gui]"

# Dictionary / wordfreq support
python -m pip install ".[dictionaries]"
```

---

## 🧩 Library Usage

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

---

## 🖥️ CLI Usage

Words (English):

```bash
nonwordgen -n 20 --min-length 4 --max-length 8 --strictness strict
```

Words (Spanish):

```bash
nonwordgen -n 20 --language spanish --min-length 4 --max-length 8
```

Sentences:

```bash
nonwordgen sentences -n 5 --language french --min-words 3 --max-words 8
```

Paragraphs:

```bash
nonwordgen paragraphs -p 2 --language german --min-sentences 2 --max-sentences 4
```

Launch GUI:

```bash
nonwordgen gui
```

You can also launch the GUI directly via the separate entry point:

```bash
nonwordgen-gui
```

Select your language, chose your options and click generate!

![Screenshot](docs/images/nonwords-gen_screenshot.png)

---

## 🌍 Supported Languages

`nonwordgen` includes plugins for:

**english**, **spanish**, **french**, **portuguese**, **indonesian**,
**swahili**, **german**, **turkish**, **russian**, **vietnamese**,
**hindi**, **korean**, **italian**, **dutch**, **tagalog**, **romanian**,
**swedish**, **norwegian**, **danish**, **afrikaans**, **yoruba**,
**polish**, **czech**, **hungarian**, **greek**, **thai**, **hebrew**,
**scb**, **malay**

To inspect programmatically:

```python
import nonwordgen
print(nonwordgen.available_languages())
```

---

## 📦 Optional Dependencies

These are **optional** and must be installed separately if desired:

- `wordfreq` - frequency-based dictionary filtering
- `PyQt6` - enables the GUI

Install one or more manually:

```bash
pip install wordfreq
pip install PyQt6

# Or via extras when installing from source / editable:
python -m pip install ".[dictionaries]"
python -m pip install ".[gui]"
```

---

## 🛠 Development

Install dev dependencies and nox:

```bash
python -m pip install -e ".[dev]"
python -m pip install nox
```

Common tasks via nox:

```bash
nox                              # run default sessions (tests + lint)
nox -s tests                     # run test suite
nox -s coverage                  # run tests with coverage + coverage.xml
nox -s lint                      # run Ruff lint checks
nox -s format                    # auto-fix with Ruff + Black
nox -s typecheck                 # run mypy
nox -s spdx                      # run test to confirm spdx license text included
nox -s spdx -- add               # Add the spdx license text to any file that does not have it.
nox -s build                     # build GUI release via build_release.py
nox -s build_package             # build wheel + sdist into dist/
nox -s build_dist                # Linux-only sdist + wheel build (CI-friendly)
nox -s build_exe                 # build standalone Windows EXE (no-op on non-Windows)
nox -s bundle_release            # bundles artifacts/files into a versioned Zip for release
nox -s publish_release -- 1.2.1  # publishes a release, update changelog, commit, create tags, push to github for release generation
```

You can still run `pytest` or `python -m build` directly if you prefer, but the GitHub Actions CI uses the nox sessions above so you can reproduce CI locally with the same commands.

Artifacts from builds appear under `dist/` (wheels/sdists from `build_package`, and the Windows executable from `build` / `build_exe`).

---

## 📤 Release Process (GitHub Only)

1. Update version in `pyproject.toml` (`[project].version`)
2. Run tests & build artifacts
3. Commit → tag → push
4. Draft a GitHub Release

   - Upload `.whl` and `.tar.gz` files
   - Add changelog notes

No PyPI steps required unless you publish there later.

---

## 📄 License

MIT License - see [LICENSE](./LICENSE).

---

## 🤖 AI Disclosure

Some documentation and text were drafted with assistance from OpenAI models and reviewed manually.

---

## 📚 Third-Party Notices

- **PyQt6** - GUI backend
- **wordfreq** - Apache-2.0 licensed

All optional extras are installed separately and not bundled by default.

---

## 🤝 Code of Conduct

This project follows a simple, respectful [Code of Conduct](./CODE_OF_CONDUCT.md).
By participating, you agree to uphold these guidelines and help keep the community welcoming and constructive.

---

## 🛡 Security

If you believe you’ve found a security issue, please review the project’s
[Security Policy](./SECURITY.md).

This project is maintained by a single developer with limited availability. I may not always be able to respond quickly, but I take security
concerns seriously and appreciate responsible disclosure.

---

## 📜 Changelog

For a history of changes, see the [Changelog](./CHANGELOG.md).

The changelog is generated automatically from git tags and commit messages.
