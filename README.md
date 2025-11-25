# nonwordgen

`nonwordgen` generates pseudo-words using a syllable-based phonotactic model and filters that attempt to discard real vocabulary via pluggable dictionary backends. The generator now loads language capabilities via plugins; the built-in English plugin replicates the previous behavior and a new Spanish plugin ships alongside it so additional languages can be added later without affecting the public API.

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
# English (default)
nonwordgen -n 20 --min-length 4 --max-length 8 --strictness strict

# Spanish
nonwordgen -n 20 --min-length 4 --max-length 8 --strictness strict --language spanish
```

## Languages

Available plugins: `english` (default), `spanish`, `french`, `portuguese`, `indonesian`, and `swahili`. The CLI lists valid options via `--help`, and the Python API exposes `nonwordgen.available_languages()` if you need to inspect them programmatically.

## Optional dependencies

The package works out of the box with a small built-in dictionary. Installing the optional extras improves real-word detection:

- `wordfreq` enables frequency-based filtering (install via `pip install "nonwordgen[dictionaries]"`).
- `wordset` contributes a larger English word list if you happen to have that package available separately.

## Development

Run the test suite with:

```bash
pytest
```
