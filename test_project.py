import pytest
import sys
from project import (
    input_test,
    count_lines,
    count_words,
    count_car,
    count_blank_lines,
    frequent_words,
    extract_dates,
    extract_email,
    search_word,
)

def test_test_input_valid_file():
    sys.argv = ["script.py", "test_file.txt"]
    assert input_test() is None


def test_test_input_invalid_file():
    sys.argv = ["script.py", "test_file.doc"]
    with pytest.raises(SystemExit):
        input_test()


def test_test_input_too_many_arguments():
    sys.argv = ["script.py", "test_file.txt", "extra_arg", "arg", "arg2"]
    with pytest.raises(SystemExit):
        input_test()


def test_test_input_find_argument():
    sys.argv = ["script.py", "test_file.txt", "--find", "search_word"]
    assert input_test() == "search_word"


def test_test_input_find_argument_missing_word():
    sys.argv = ["script.py", "test_file.txt", "--find"]
    with pytest.raises(SystemExit):
        input_test()


def test_count_lines():
    txt = ["line 1\n", "line 2\n", "line 3"]
    assert count_lines(txt) == 3


def test_count_words():
    txt = "This is a test sentence."
    assert count_words(txt) == 5


def test_count_car():
    txt = "This is a test sentence."
    assert count_car(txt) == 24


def test_count_blank_lines():
    txt = ["line 1\n", "\n", "line 3"]
    assert count_blank_lines(txt) == 1


def test_frequent_words():
    txt = "word1 word2 word1 word3 word2 word3 word4"
    expected_output = "The 3 more frequent word(s) are: \n  - 'word1' occurring 2 times\n  - 'word2' occurring 2 times\n  - 'word3' occurring 2 times"
    assert frequent_words(txt) == expected_output


def test_extract_dates():
    txt = "Date1: 10-12-2022, Date2: 15-01-2023, No date here."
    expected_output = ["    10-12-2022", "    15-01-2023"]
    assert extract_dates(txt) == expected_output


def test_extract_dates_no_dates():
    txt = "No date in this text."
    assert extract_dates(txt) == "No dates found"


def test_extract_email():
    txt = "Email1: user@gmail.com, Email2: support@outlook.com, InvalidEmail"
    expected_output = ["    user@gmail.com", "    support@outlook.com"]
    assert extract_email(txt) == expected_output


def test_extract_email_no_emails():
    txt = "No email in this text."
    assert extract_email(txt) == "No email addresses found"


def test_search_word():
    txt = "word1 word2 word1 word3 word2 word3 word4"
    assert search_word(txt, "word1") == 2
