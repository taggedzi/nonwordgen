# nonwordgen

`nonwordgen` generates English-like non-words using a syllable-based phonotactic model and filters that attempt to discard real English vocabulary via pluggable dictionary backends.

## Library usage

```python
from nonwordgen import WordGenerator, Strictness

gen = WordGenerator(
    min_length=5,
    max_length=9,
    strictness=Strictness.MEDIUM,
)

print(gen.generate_one())
print(gen.generate_many(10))
```

## CLI usage

```bash
nonwordgen -n 20 --min-length 4 --max-length 8 --strictness strict
```

## Optional dependencies

The package works out of the box with a small built-in dictionary. Installing the optional extras improves real-word detection:

- `wordfreq` enables frequency-based filtering (install via `pip install "nonwordgen[dictionaries]"`).
- `wordset` contributes a larger English word list if you happen to have that package available separately.

## Development

Run the test suite with:

```bash
pytest
```
