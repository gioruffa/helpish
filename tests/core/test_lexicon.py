from helpish.core.lexicon import Lexicon, Word
from pytest import fixture, raises
import random
from unittest.mock import patch, MagicMock


@fixture
def simple_frequency_dict():
    return {"a": 0.1, "i": 0.3, "to": 0.1, "of": 0.2}


@fixture
def simple_words_by_length(simple_frequency_dict):
    return {
        1: [
            Word("a", simple_frequency_dict["a"]),
            Word("i", simple_frequency_dict["i"]),
        ],
        2: [
            Word("to", simple_frequency_dict["to"]),
            Word("of", simple_frequency_dict["of"]),
        ],
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


def test_lexicon_longest_length_returns_0_when_empty():
    sut = Lexicon({})
    assert sut.longest_length == 0


def test_lexicon_from_wordfreq(simple_frequency_dict, simple_lexicon):
    with patch("helpish.core.lexicon.get_frequency_dict") as the_mock:
        the_mock.return_value = simple_frequency_dict
        sut = Lexicon.from_wordfreq()
        assert sut == simple_lexicon
        the_mock.assert_called_once_with("en")


def test_lexicon_eq(simple_lexicon, simple_frequency_dict):
    assert simple_lexicon != simple_frequency_dict


def test_lexicon_from_wordfreq_unsupported_language():
    with raises(ValueError) as error:
        Lexicon.from_wordfreq("vogon")
    assert "Language vogon not supported." in error.value.args[0]
