"""The Lexicon: an English vocabulary that answers word-length searches."""

from __future__ import annotations

from collections import defaultdict

from wordfreq import get_frequency_dict

from dataclasses import dataclass


@dataclass
class Word:
    """A word as part of a language, together with useful metadata."""

    word: str
    frequency: float


class Lexicon:
    """An vocabulary bucketed by word length.

    Owns the vocabulary and answers length/substring searches, keeping each
    bucket in descending-frequency order so callers get the most frequent
    words first.
    """

    def __init__(self, words_by_length: dict[int, list[Word]]) -> None:
        self._words_by_length = words_by_length
        self._total_words = sum(len(words) for words in self._words_by_length.values())
        self._longest_length = max(self._words_by_length, default=0)

    @classmethod
    def from_wordfreq(cls, language: str = "en") -> Lexicon:
        """Build a Lexicon from the wordfreq vocabulary for ``language``.

        Words arrive in descending-frequency order, so each bucket is already
        sorted most-frequent-first.
        """
        buckets: dict[int, list[Word]] = defaultdict(list)
        for word, frequency in get_frequency_dict(language).items():
            if word.isalpha():
                buckets[len(word)].append(Word(word=word, frequency=frequency))
        return cls(dict(buckets))

    @property
    def total_words(self) -> int:
        """How many words the Lexicon holds across every length."""
        return self._total_words

    @property
    def longest_length(self) -> int:
        """Length of the longest word, or 0 when the Lexicon is empty."""
        return self._longest_length

    def search(self, length: int, contains: str = "") -> list[Word]:
        """Return every Word of ``length`` containing ``contains``.

        ``contains`` is matched case-insensitively; 
        An empty string matches every word of that length.
        There are no guarantees on ordering.
        """
        words = self._words_by_length.get(length, [])
        query = contains.strip().lower()
        if query:
            words = [word for word in words if query in word.word]
        return words
