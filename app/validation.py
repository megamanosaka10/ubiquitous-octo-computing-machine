"""
Input validation module.

SECURITY BEST PRACTICE: Validate and sanitize all user input before processing.
Reject invalid input early with clear error messages.
"""

import re

import bleach


# Strict patterns for common inputs
USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_]{3,30}$")
EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def validate_username(username: str) -> tuple[bool, str]:
    """Validate a username: alphanumeric + underscore, 3-30 chars."""
    if not username:
        return False, "Username is required"
    if not USERNAME_PATTERN.match(username):
        return False, "Username must be 3-30 alphanumeric characters or underscores"
    return True, ""


def validate_email(email: str) -> tuple[bool, str]:
    """Validate an email address format."""
    if not email:
        return False, "Email is required"
    if len(email) > 254:
        return False, "Email is too long"
    if not EMAIL_PATTERN.match(email):
        return False, "Invalid email format"
    return True, ""


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength.

    Requirements: 8+ chars, at least one uppercase, one lowercase, one digit.
    """
    if not password:
        return False, "Password is required"
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if len(password) > 128:
        return False, "Password must be at most 128 characters"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit"
    return True, ""


def sanitize_html(content: str) -> str:
    """
    Sanitize user-provided content to prevent XSS.

    Allows only safe tags and attributes.
    """
    allowed_tags = ["b", "i", "u", "em", "strong", "p", "br", "ul", "ol", "li"]
    allowed_attrs = {}
    return bleach.clean(content, tags=allowed_tags, attributes=allowed_attrs, strip=True)


def validate_post_title(title: str) -> tuple[bool, str]:
    """Validate a post title."""
    if not title:
        return False, "Title is required"
    if len(title) > 200:
        return False, "Title must be at most 200 characters"
    return True, ""


def validate_post_content(content: str) -> tuple[bool, str]:
    """Validate post content."""
    if not content:
        return False, "Content is required"
    if len(content) > 10000:
        return False, "Content must be at most 10000 characters"
    return True, ""
