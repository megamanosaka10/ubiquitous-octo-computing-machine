"""String manipulation utilities."""

from __future__ import annotations

import re
from typing import Dict, List


def reverse(s: str) -> str:
    """Return *s* reversed."""
    return s[::-1]


def is_palindrome(s: str) -> bool:
    """Return True if *s* reads the same forwards and backwards (case-insensitive, ignoring non-alphanumeric)."""
    cleaned = re.sub(r"[^a-zA-Z0-9]", "", s).lower()
    return cleaned == cleaned[::-1]


def word_count(text: str) -> Dict[str, int]:
    """Return a mapping of word -> frequency for words in *text*."""
    counts: Dict[str, int] = {}
    for word in text.lower().split():
        word = re.sub(r"[^\w]", "", word)
        if word:
            counts[word] = counts.get(word, 0) + 1
    return counts


def truncate(s: str, max_length: int, suffix: str = "...") -> str:
    """Truncate *s* to *max_length* characters, appending *suffix* when truncated."""
    if max_length < 0:
        raise ValueError("max_length must be non-negative")
    if len(s) <= max_length:
        return s
    if max_length <= len(suffix):
        return s[:max_length]
    return s[: max_length - len(suffix)] + suffix


def slugify(s: str) -> str:
    """Convert *s* into a URL-friendly slug."""
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def caesar_cipher(text: str, shift: int) -> str:
    """Apply a Caesar cipher with the given *shift* to *text*."""
    result: List[str] = []
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return "".join(result)


def count_vowels(s: str) -> int:
    """Return the number of vowels (a, e, i, o, u) in *s*."""
    return sum(1 for ch in s.lower() if ch in "aeiou")


def title_case(s: str) -> str:
    """Convert *s* to title case, capitalising the first letter of each word."""
    return " ".join(word.capitalize() for word in s.split())
