# SPDX-License-Identifier: MIT
# 🧩 Contributing to **nonwordgen**

Thank you for considering contributing to **nonwordgen**!
This project thrives on modularity, clarity, and a little bit of silliness - so contributions are welcome whether you're fixing a bug, improving docs, or adding a brand-new language plugin.

---

## 🛠️ 1. Setting Up a Development Environment

**Requirements:**

* Python **3.11** (project is tested against 3.10–3.13, but dev uses 3.11)
* `pip` or `pipx`
* `nox` for automation (recommended but optional)
* Git

**Steps:**

```bash
# 1. Clone the repo
git clone https://github.com/taggedzi/nonwordgen.git
cd nonwordgen

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
# OR
.\.venv\Scripts\activate       # Windows

# 3. Install dev dependencies
pip install -e ".[dev]"
```

If you're using **nox**, simply run:

```bash
nox
```

This will install environments as needed for tests, linting, formatting, and type checking.

---

## 🧪 2. Running Tests

Tests use **pytest** and are automated via **nox**.

### Run tests directly

```bash
pytest
```

### Run tests via nox (recommended)

```bash
nox -s tests
```

Coverage report:

```bash
nox -s coverage
```

---

## 🎨 3. Coding Style

nonwordgen follows a consistent and strict-but-friendly coding style.

We use:

| Tool        | Purpose                              |
| ----------- | ------------------------------------ |
| **ruff**    | Linting & some auto-fixes            |
| **black**   | Code formatting (PEP 8-ish)          |
| **mypy**    | Type checking                        |
| **pytest**  | Testing                              |
| **tox/nox** | Automation (depending on your setup) |

### Before submitting a PR

```bash
nox -s format      # runs ruff --fix + black
nox -s lint        # runs ruff check
nox -s typecheck   # runs mypy
nox -s tests       # ensures all tests pass
```

Or manually:

```bash
ruff check .
ruff format .
black .
mypy src/
pytest
```

All new code **must include type hints** and should include tests unless trivial.

---

## 🌍 4. Adding a New Language Plugin (MOST IMPORTANT!)

Language support in **nonwordgen** is fully pluggable.
Each plugin defines:

* Its own **language code** (e.g., `en`, `es`, `jp`)
* A **syllable inventory**
* Optional **orthography** variations
* Optional **dictionary backends** to filter out real words

Plugins live inside:

```bash
src/nonwordgen/plugins/
```

### 4.1. Create the plugin file

Example for a Spanish plugin:

```bash
src/nonwordgen/plugins/es.py
```

### 4.2. Basic plugin structure

Every plugin must expose:

```python
from nonwordgen.language import LanguagePlugin

class SpanishPlugin(LanguagePlugin):
    code = "es"
    name = "Spanish"

    syllables = [
        "ma", "me", "mi", "mo", "mu",
        "pa", "pe", "pi", "po", "pu",
        "ca", "que", "qui", "co", "cu",
        # ...
    ]

    # Optional: accents, special orthography behavior
    orthography = {
        "ñ": 1,
        "ll": 1,
        "ch": 1,
        # ...
    }

    # Optional: dictionary for filtering real Spanish words
    dictionary_files = ["data/dictionaries/es.txt"]
```

### 4.3. Register the plugin

Add your plugin to:

```bash
src/nonwordgen/plugins/__init__.py
```

Example:

```python
from .es import SpanishPlugin
available_plugins["es"] = SpanishPlugin()
```

### 4.4. Add tests for your plugin

Create a file:

```bash
tests/plugins/test_es.py
```

With basics like:

```python
from nonwordgen.plugins import available_plugins

def test_es_plugin_loads():
    assert "es" in available_plugins
    p = available_plugins["es"]
    assert len(p.syllables) > 0
```

### 4.5. Document your plugin

Add your language to:

* README language list
* Changelog (if applicable)

---

## 🧵 5. Branching & PR Guidelines

* Use feature branches: `feature/my-cool-thing`
* Keep PRs focused & small
* Include tests and type hints
* Update docs where needed
* Ensure `nox` passes all tasks

---

## 💬 6. Getting Help

Open a GitHub Issue or start a Discussion if you're unsure about anything.
Whether you're fixing a typo or adding a full new orthographic system, your contribution is welcome!

Absolutely — here’s a clean, professional, concise section you can drop directly into **CONTRIBUTING.md** under a heading such as *“Labeling Conventions”* or *“Pull Request Labels”*.
I kept it consistent with your project’s tone: friendly, structured, and helpful.

---

# 📛 Pull Request & Issue Labels

To keep the repository organized and make reviews easier, GitHub automatically applies labels based on which files are changed.
Below is a quick guide to what each label means and when it appears.

### **`core`**

Changes to the primary nonwordgen logic located under:

```bash
src/nonwordgen/
```

(excluding language modules).
This includes syllable generation, filtering logic, paragraph/sentence generators, and internal helpers.

---

### **`language-module`**

Updates to any language implementation under:

```bash
src/nonwordgen/languages/
```

Examples:

* Adding a new language
* Modifying phonotactic rules
* Updating syllable sets or orthography

---

### **`cli`**

Changes affecting the command-line interface:

```bash
src/cli/
src/nonwordgen/__main__.py
```

Examples:

* Flags
* Options
* User-facing CLI behavior

---

### **`gui`**

Changes affecting the graphical application:

```bash
src/gui/
```

Examples:

* UI layout
* Widgets
* Event handling
* Visual styles

---

### **`tests`**

Any changes to tests or test infrastructure:

```bash
tests/
noxfile.py
.github/workflows/test.yml
```

---

### **`documentation`**

Changes to markdown files, docs, or top-level project descriptions:

```bash
README.md
CONTRIBUTING.md
SECURITY.md
CODE_OF_CONDUCT.md
SUPPORT.md
RELEASE.md
docs/
```

This label applies whether you fix typos, rewrite paragraphs, or add new sections.

---

### **`ci`**

Changes to GitHub Actions workflows:

```bash
.github/workflows/
```

Examples:

* Test matrix updates
* Build pipelines
* Release automation

---

### **`packaging`**

Changes affecting how the project is built or distributed:

```bash
pyproject.toml
setup.cfg / setup.py
MANIFEST.in
noxfile.py
```

Examples:

* Dependency metadata
* Entry points
* Wheel configuration

---

### **`config`**

Changes to development or repository hygiene files:

```bash
.pre-commit-config.yaml
.editorconfig
.gitignore
mypy.ini
ruff config
.vscode/
.idea/
```

Includes formatting, editor settings, and static analysis rules.

---

### **`dependencies`**

Updates to project or dev dependencies:

```bash
pyproject.toml
requirements*.txt
```

---

### **`changelog`**

Changes specifically to release notes or project history:

```bash
CHANGELOG.md
RELEASE.md
```

---

# 💡 Why These Labels Matter

* Makes PR review faster
* Helps automatic changelog generation
* Helps contributors understand which part of the project they're changing
* Keeps the repo clean and organized over time
* Allows filtering PRs/issues easily
