"""Comprehensive tests for math_utils module."""

import pytest

from octo_compute.math_utils import (
    clamp,
    factorial,
    fibonacci,
    gcd,
    is_prime,
    lcm,
    mean,
    median,
)


class TestFactorial:
    def test_zero(self):
        assert factorial(0) == 1

    def test_one(self):
        assert factorial(1) == 1

    def test_five(self):
        assert factorial(5) == 120

    def test_negative_raises(self):
        with pytest.raises(ValueError, match="not defined for negative"):
            factorial(-1)

    def test_non_int_raises(self):
        with pytest.raises(TypeError, match="Expected int"):
            factorial(3.5)


class TestFibonacci:
    def test_zero(self):
        assert fibonacci(0) == []

    def test_one(self):
        assert fibonacci(1) == [0]

    def test_two(self):
        assert fibonacci(2) == [0, 1]

    def test_five(self):
        assert fibonacci(5) == [0, 1, 1, 2, 3]

    def test_negative(self):
        assert fibonacci(-1) == []

    def test_non_int_raises(self):
        with pytest.raises(TypeError, match="Expected int"):
            fibonacci(2.5)


class TestIsPrime:
    def test_small_primes(self):
        assert is_prime(2) is True
        assert is_prime(3) is True
        assert is_prime(5) is True
        assert is_prime(7) is True

    def test_non_primes(self):
        assert is_prime(0) is False
        assert is_prime(1) is False
        assert is_prime(4) is False
        assert is_prime(9) is False

    def test_larger_prime(self):
        assert is_prime(97) is True

    def test_larger_non_prime(self):
        assert is_prime(100) is False

    def test_negative(self):
        assert is_prime(-7) is False

    def test_even_composite(self):
        assert is_prime(6) is False

    def test_divisible_by_three(self):
        assert is_prime(15) is False

    def test_25(self):
        assert is_prime(25) is False


class TestGcd:
    def test_basic(self):
        assert gcd(12, 8) == 4

    def test_coprime(self):
        assert gcd(7, 13) == 1

    def test_same(self):
        assert gcd(5, 5) == 5

    def test_zero(self):
        assert gcd(0, 5) == 5
        assert gcd(5, 0) == 5

    def test_negatives(self):
        assert gcd(-12, 8) == 4


class TestLcm:
    def test_basic(self):
        assert lcm(4, 6) == 12

    def test_coprime(self):
        assert lcm(3, 7) == 21

    def test_zero(self):
        assert lcm(0, 5) == 0
        assert lcm(5, 0) == 0


class TestMean:
    def test_basic(self):
        assert mean([1, 2, 3, 4, 5]) == 3.0

    def test_single(self):
        assert mean([10]) == 10.0

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="Cannot compute mean"):
            mean([])


class TestMedian:
    def test_odd_count(self):
        assert median([3, 1, 2]) == 2

    def test_even_count(self):
        assert median([1, 2, 3, 4]) == 2.5

    def test_single(self):
        assert median([42]) == 42

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="Cannot compute median"):
            median([])


class TestClamp:
    def test_within_range(self):
        assert clamp(5, 0, 10) == 5

    def test_below_range(self):
        assert clamp(-5, 0, 10) == 0

    def test_above_range(self):
        assert clamp(15, 0, 10) == 10

    def test_at_boundary(self):
        assert clamp(0, 0, 10) == 0
        assert clamp(10, 0, 10) == 10

    def test_invalid_range_raises(self):
        with pytest.raises(ValueError, match="low must be <= high"):
            clamp(5, 10, 0)
