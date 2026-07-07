"""Load and bucket the bundled English word list."""

from __future__ import annotations

from collections import defaultdict
from importlib.resources import files
from pathlib import Path

WORDS_FILE = Path(str(files("helpish") / "words_alpha.txt"))


def load_words_by_length(path: Path) -> dict[int, list[str]]:
    """Read the word list once and bucket every word by its length."""
    buckets: dict[int, list[str]] = defaultdict(list)
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            word = line.strip()
            if word:
                buckets[len(word)].append(word)
    return buckets
