"""Mathematical utility functions."""

from __future__ import annotations

from typing import List


def factorial(n: int) -> int:
    """Return n! for non-negative integers."""
    if not isinstance(n, int):
        raise TypeError(f"Expected int, got {type(n).__name__}")
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def fibonacci(n: int) -> List[int]:
    """Return the first *n* Fibonacci numbers."""
    if not isinstance(n, int):
        raise TypeError(f"Expected int, got {type(n).__name__}")
    if n <= 0:
        return []
    seq = [0]
    if n == 1:
        return seq
    seq.append(1)
    for _ in range(2, n):
        seq.append(seq[-1] + seq[-2])
    return seq


def is_prime(n: int) -> bool:
    """Return True if *n* is a prime number."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def gcd(a: int, b: int) -> int:
    """Return the greatest common divisor of *a* and *b*."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Return the least common multiple of *a* and *b*."""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def mean(values: List[float]) -> float:
    """Return the arithmetic mean of *values*."""
    if not values:
        raise ValueError("Cannot compute mean of empty sequence")
    return sum(values) / len(values)


def median(values: List[float]) -> float:
    """Return the median of *values*."""
    if not values:
        raise ValueError("Cannot compute median of empty sequence")
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2
    return sorted_vals[mid]


def clamp(value: float, low: float, high: float) -> float:
    """Clamp *value* to the inclusive range [low, high]."""
    if low > high:
        raise ValueError("low must be <= high")
    return max(low, min(high, value))
