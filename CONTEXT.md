# Context

Domain vocabulary for **helpish** — a terminal app that lists English words by
length, handy for writing Pilish.

## Terms

**Lexicon**
The English vocabulary, bucketed by word length. Owns the words and answers
searches — `search(length, contains)` returns every word of a given length,
in descending-frequency order, optionally filtered by a substring. Built from
the wordfreq word list via `Lexicon.from_wordfreq()`.

**Search**
A length-plus-substring query answered by the Lexicon. Case-insensitive on the
substring; an empty substring matches every word of that length.
