from helpish.core.lexicon import Lexicon, Word
from pytest import fixture
import random


@fixture
def simple_words_by_length():
    return {
        1: [Word("a", 0.1), Word("i", 0.3)],
        2: [Word("to", 0.1), Word("of", 0.2)],
    }

@fixture
def simple_lexicon(simple_words_by_length):
    return Lexicon(words_by_length=simple_words_by_length)


def test_lexicon_search_by_length(simple_words_by_length):
    sut = Lexicon(words_by_length=simple_words_by_length)
    for length, word_of_length in simple_words_by_length.items():
        assert sut.search(length=length) == word_of_length


def test_lexicon_search_by_length_not_exist_returns_empty(simple_lexicon):
    assert simple_lexicon.search(3) == []


def test_lexicon_search_contains(simple_lexicon):
    assert simple_lexicon.search(1, "a") == [Word("a", 0.1)]
    assert simple_lexicon.search(1, "i") == [Word("i", 0.3)]
    assert simple_lexicon.search(1, "c") == []

    assert simple_lexicon.search(2, "t") == [Word("to", 0.1)]
    assert simple_lexicon.search(2, "f") == [Word("of", 0.2)]
    assert simple_lexicon.search(2, "o") == [Word("to", 0.1), Word("of", 0.2)]


def test_lexicon_search_contains_empty_returns_all(simple_words_by_length):
    sut = Lexicon(words_by_length=simple_words_by_length)
    for length, word_of_length in simple_words_by_length.items():
        assert sut.search(length=length, contains="") == word_of_length


def test_lexicon_search_returns_random_order(simple_words_by_length):
    for length in simple_words_by_length:
        # Note that since we are using randomly the seed will change at every run
        random.shuffle(simple_words_by_length[length])

    sut = Lexicon(words_by_length=simple_words_by_length)
    for length, word_of_length in simple_words_by_length.items():
        assert sut.search(length=length, contains="") == word_of_length


def test_lexicon_total_words(simple_lexicon):
    assert simple_lexicon.total_words == 4


def test_lexicon_longest_length(simple_lexicon):
    assert simple_lexicon.longest_length == 2
