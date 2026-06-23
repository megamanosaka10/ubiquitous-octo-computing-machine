"""Data validation helpers."""

from __future__ import annotations

import re


def is_valid_email(email: str) -> bool:
    """Return True if *email* looks like a valid email address."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def is_valid_url(url: str) -> bool:
    """Return True if *url* looks like a valid HTTP(S) URL."""
    pattern = r"^https?://[^\s/$.?#].[^\s]*$"
    return bool(re.match(pattern, url))


def is_valid_ipv4(address: str) -> bool:
    """Return True if *address* is a valid IPv4 address."""
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False
        if part != str(num):  # reject leading zeros
            return False
    return True


def is_strong_password(password: str, min_length: int = 8) -> bool:
    """Return True if *password* meets basic strength requirements."""
    if len(password) < min_length:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
    return all([has_upper, has_lower, has_digit, has_special])


def is_valid_hex_color(color: str) -> bool:
    """Return True if *color* is a valid hex colour (e.g. '#ff00aa')."""
    pattern = r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$"
    return bool(re.match(pattern, color))


def is_within_range(value: float, low: float, high: float) -> bool:
    """Return True if *value* lies within [low, high]."""
    return low <= value <= high


def sanitize_input(text: str) -> str:
    """Strip leading/trailing whitespace and collapse internal whitespace."""
    return re.sub(r"\s+", " ", text.strip())
