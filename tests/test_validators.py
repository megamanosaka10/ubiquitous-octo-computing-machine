"""Tests for validators module."""

from octo_compute.validators import (
    is_strong_password,
    is_valid_email,
    is_valid_hex_color,
    is_valid_ipv4,
    is_valid_url,
    is_within_range,
    sanitize_input,
)


class TestIsValidEmail:
    def test_valid(self):
        assert is_valid_email("user@example.com") is True

    def test_valid_with_dots(self):
        assert is_valid_email("first.last@example.co.uk") is True

    def test_missing_at(self):
        assert is_valid_email("userexample.com") is False

    def test_missing_domain(self):
        assert is_valid_email("user@") is False

    def test_missing_tld(self):
        assert is_valid_email("user@example") is False


class TestIsValidUrl:
    def test_http(self):
        assert is_valid_url("http://example.com") is True

    def test_https(self):
        assert is_valid_url("https://example.com/path?q=1") is True

    def test_no_scheme(self):
        assert is_valid_url("example.com") is False

    def test_ftp(self):
        assert is_valid_url("ftp://example.com") is False


class TestIsValidIpv4:
    def test_valid(self):
        assert is_valid_ipv4("192.168.1.1") is True

    def test_zeros(self):
        assert is_valid_ipv4("0.0.0.0") is True

    def test_max(self):
        assert is_valid_ipv4("255.255.255.255") is True

    def test_too_few_octets(self):
        assert is_valid_ipv4("192.168.1") is False

    def test_leading_zeros_rejected(self):
        assert is_valid_ipv4("192.168.01.1") is False

    def test_non_numeric(self):
        assert is_valid_ipv4("abc.def.ghi.jkl") is False

    def test_out_of_range(self):
        assert is_valid_ipv4("256.0.0.1") is False


class TestIsStrongPassword:
    def test_strong(self):
        assert is_strong_password("Str0ng!Pass") is True

    def test_too_short(self):
        assert is_strong_password("S1!a") is False

    def test_no_uppercase(self):
        assert is_strong_password("str0ng!pass") is False

    def test_no_lowercase(self):
        assert is_strong_password("STR0NG!PASS") is False

    def test_no_digit(self):
        assert is_strong_password("Strong!Pass") is False

    def test_no_special(self):
        assert is_strong_password("Str0ngPass1") is False

    def test_custom_min_length(self):
        assert is_strong_password("S1!a", min_length=4) is True


class TestIsValidHexColor:
    def test_six_digit(self):
        assert is_valid_hex_color("#ff00aa") is True

    def test_three_digit(self):
        assert is_valid_hex_color("#f0a") is True

    def test_uppercase(self):
        assert is_valid_hex_color("#FF00AA") is True

    def test_missing_hash(self):
        assert is_valid_hex_color("ff00aa") is False

    def test_wrong_length(self):
        assert is_valid_hex_color("#ff00a") is False


class TestIsWithinRange:
    def test_within(self):
        assert is_within_range(5, 1, 10) is True

    def test_at_low_boundary(self):
        assert is_within_range(1, 1, 10) is True

    def test_at_high_boundary(self):
        assert is_within_range(10, 1, 10) is True

    def test_below(self):
        assert is_within_range(0, 1, 10) is False

    def test_above(self):
        assert is_within_range(11, 1, 10) is False


class TestSanitizeInput:
    def test_strips_whitespace(self):
        assert sanitize_input("  hello  ") == "hello"

    def test_collapses_internal_whitespace(self):
        assert sanitize_input("hello   world") == "hello world"

    def test_tabs_and_newlines(self):
        assert sanitize_input("hello\t\n  world") == "hello world"

    def test_already_clean(self):
        assert sanitize_input("hello") == "hello"
