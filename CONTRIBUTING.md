# 🧩 Contributing to **nonword-gen**

Thank you for considering contributing to **nonword-gen**!
This project thrives on modularity, clarity, and a little bit of silliness — so contributions are welcome whether you're fixing a bug, improving docs, or adding a brand-new language plugin.

---

## 🛠️ 1. Setting Up a Development Environment

**Requirements:**

* Python **3.11** (project is tested against 3.9–3.13, but dev uses 3.11)
* `pip` or `pipx`
* `nox` for automation (recommended but optional)
* Git

**Steps:**

```bash
# 1. Clone the repo
git clone https://github.com/<yourname>/nonword-gen.git
cd nonword-gen

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

nonword-gen follows a consistent and strict-but-friendly coding style.

We use:

| Tool        | Purpose                              |
| ----------- | ------------------------------------ |
| **ruff**    | Linting & some auto-fixes            |
| **black**   | Code formatting (PEP 8-ish)          |
| **mypy**    | Type checking                        |
| **pytest**  | Testing                              |
| **tox/nox** | Automation (depending on your setup) |

### Before submitting a PR:

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

Language support in **nonword-gen** is fully pluggable.
Each plugin defines:

* Its own **language code** (e.g., `en`, `es`, `jp`)
* A **syllable inventory**
* Optional **orthography** variations
* Optional **dictionary backends** to filter out real words

Plugins live inside:

```
src/nonwordgen/plugins/
```

### 4.1. Create the plugin file

Example for a Spanish plugin:

```
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

```
src/nonwordgen/plugins/__init__.py
```

Example:

```python
from .es import SpanishPlugin
available_plugins["es"] = SpanishPlugin()
```

### 4.4. Add tests for your plugin

Create a file:

```
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
