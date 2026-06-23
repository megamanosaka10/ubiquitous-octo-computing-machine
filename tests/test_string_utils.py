"""Tests for string_utils module."""

import pytest

from octo_compute.string_utils import (
    caesar_cipher,
    count_vowels,
    is_palindrome,
    reverse,
    slugify,
    title_case,
    truncate,
    word_count,
)


class TestReverse:
    def test_basic(self):
        assert reverse("hello") == "olleh"

    def test_empty(self):
        assert reverse("") == ""

    def test_single_char(self):
        assert reverse("a") == "a"

    def test_palindrome(self):
        assert reverse("racecar") == "racecar"


class TestIsPalindrome:
    def test_simple_palindrome(self):
        assert is_palindrome("racecar") is True

    def test_case_insensitive(self):
        assert is_palindrome("Racecar") is True

    def test_ignores_non_alphanumeric(self):
        assert is_palindrome("A man, a plan, a canal: Panama") is True

    def test_not_palindrome(self):
        assert is_palindrome("hello") is False

    def test_empty(self):
        assert is_palindrome("") is True


class TestWordCount:
    def test_basic(self):
        assert word_count("the cat sat on the mat") == {
            "the": 2,
            "cat": 1,
            "sat": 1,
            "on": 1,
            "mat": 1,
        }

    def test_empty(self):
        assert word_count("") == {}

    def test_punctuation_stripped(self):
        result = word_count("hello, world! hello.")
        assert result == {"hello": 2, "world": 1}


class TestTruncate:
    def test_no_truncation_needed(self):
        assert truncate("hi", 10) == "hi"

    def test_truncation_with_suffix(self):
        assert truncate("hello world", 8) == "hello..."

    def test_max_length_equals_suffix_length(self):
        assert truncate("hello world", 3) == "hel"

    def test_negative_max_length_raises(self):
        with pytest.raises(ValueError, match="max_length must be non-negative"):
            truncate("test", -1)

    def test_custom_suffix(self):
        assert truncate("hello world", 8, suffix="~") == "hello w~"


class TestSlugify:
    def test_basic(self):
        assert slugify("Hello World") == "hello-world"

    def test_special_characters_removed(self):
        assert slugify("Hello, World! #2024") == "hello-world-2024"

    def test_multiple_spaces_collapsed(self):
        assert slugify("hello   world") == "hello-world"

    def test_leading_trailing_stripped(self):
        assert slugify("  hello  ") == "hello"


class TestCaesarCipher:
    def test_shift_basic(self):
        assert caesar_cipher("abc", 3) == "def"

    def test_wraparound(self):
        assert caesar_cipher("xyz", 3) == "abc"

    def test_preserves_case(self):
        assert caesar_cipher("Hello", 1) == "Ifmmp"

    def test_non_alpha_unchanged(self):
        assert caesar_cipher("a b!c", 1) == "b c!d"

    def test_decrypt(self):
        encrypted = caesar_cipher("hello", 5)
        assert caesar_cipher(encrypted, -5) == "hello"


class TestCountVowels:
    def test_basic(self):
        assert count_vowels("hello") == 2

    def test_no_vowels(self):
        assert count_vowels("bcdfg") == 0

    def test_all_vowels(self):
        assert count_vowels("aeiou") == 5

    def test_case_insensitive(self):
        assert count_vowels("AeIoU") == 5

    def test_empty(self):
        assert count_vowels("") == 0


class TestTitleCase:
    def test_basic(self):
        assert title_case("hello world") == "Hello World"

    def test_already_title(self):
        assert title_case("Hello World") == "Hello World"

    def test_all_lower(self):
        assert title_case("foo bar baz") == "Foo Bar Baz"

    def test_empty(self):
        assert title_case("") == ""
