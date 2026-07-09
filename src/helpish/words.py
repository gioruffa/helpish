"""Bucket the wordfreq English vocabulary by length."""

from __future__ import annotations

from collections import defaultdict

from wordfreq import iter_wordlist


def load_words_by_length(language: str = "en") -> dict[int, list[str]]:
    """Bucket every alphabetic word from wordfreq by its length.

    Words arrive in descending-frequency order, so each bucket is
    already sorted most-frequent-first.
    """
    buckets: dict[int, list[str]] = defaultdict(list)
    for word in iter_wordlist(language):
        if word.isalpha():
            buckets[len(word)].append(word)
    return buckets
