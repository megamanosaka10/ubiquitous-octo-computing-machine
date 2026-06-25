"""A simple stack-based calculator with history."""

from __future__ import annotations

from typing import List


class DivisionByZeroError(Exception):
    """Raised when division by zero is attempted."""


class Calculator:
    """Stateful calculator that keeps a running result and operation history."""

    def __init__(self, initial: float = 0.0) -> None:
        self._result: float = initial
        self._history: List[str] = [f"init({initial})"]

    @property
    def result(self) -> float:
        return self._result

    @property
    def history(self) -> List[str]:
        return list(self._history)

    def add(self, value: float) -> "Calculator":
        self._result += value
        self._history.append(f"add({value})")
        return self

    def subtract(self, value: float) -> "Calculator":
        self._result -= value
        self._history.append(f"subtract({value})")
        return self

    def multiply(self, value: float) -> "Calculator":
        self._result *= value
        self._history.append(f"multiply({value})")
        return self

    def divide(self, value: float) -> "Calculator":
        if value == 0:
            raise DivisionByZeroError("Cannot divide by zero")
        self._result /= value
        self._history.append(f"divide({value})")
        return self

    def power(self, exponent: float) -> "Calculator":
        self._result **= exponent
        self._history.append(f"power({exponent})")
        return self

    def sqrt(self) -> "Calculator":
        if self._result < 0:
            raise ValueError("Cannot take square root of negative number")
        self._result **= 0.5
        self._history.append("sqrt()")
        return self

    def negate(self) -> "Calculator":
        self._result = -self._result
        self._history.append("negate()")
        return self

    def reset(self, value: float = 0.0) -> "Calculator":
        self._result = value
        self._history.append(f"reset({value})")
        return self

    def undo(self) -> "Calculator":
        """Remove the last operation (recompute from history is NOT supported;
        this simply pops the last entry and is a best-effort convenience)."""
        if len(self._history) <= 1:
            raise IndexError("Nothing to undo")
        self._history.pop()
        return self

    def __repr__(self) -> str:
        return f"Calculator(result={self._result})"
