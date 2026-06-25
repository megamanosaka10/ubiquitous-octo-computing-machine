"""Tests for the Calculator class."""

import pytest

from octo_compute.calculator import Calculator, DivisionByZeroError


class TestCalculatorInit:
    def test_default_initial_value(self):
        calc = Calculator()
        assert calc.result == 0.0

    def test_custom_initial_value(self):
        calc = Calculator(10.0)
        assert calc.result == 10.0

    def test_history_starts_with_init(self):
        calc = Calculator(5.0)
        assert calc.history == ["init(5.0)"]

    def test_repr(self):
        calc = Calculator(3.0)
        assert repr(calc) == "Calculator(result=3.0)"


class TestCalculatorArithmetic:
    def test_add(self):
        calc = Calculator(10).add(5)
        assert calc.result == 15

    def test_subtract(self):
        calc = Calculator(10).subtract(3)
        assert calc.result == 7

    def test_multiply(self):
        calc = Calculator(4).multiply(3)
        assert calc.result == 12

    def test_divide(self):
        calc = Calculator(10).divide(4)
        assert calc.result == 2.5

    def test_divide_by_zero(self):
        with pytest.raises(DivisionByZeroError, match="Cannot divide by zero"):
            Calculator(10).divide(0)

    def test_power(self):
        calc = Calculator(2).power(10)
        assert calc.result == 1024

    def test_sqrt(self):
        calc = Calculator(16).sqrt()
        assert calc.result == 4.0

    def test_sqrt_negative_raises(self):
        with pytest.raises(ValueError, match="Cannot take square root of negative"):
            Calculator(-1).sqrt()

    def test_negate(self):
        calc = Calculator(5).negate()
        assert calc.result == -5


class TestCalculatorChaining:
    def test_chained_operations(self):
        result = Calculator(0).add(10).multiply(2).subtract(5).result
        assert result == 15

    def test_history_records_all_operations(self):
        calc = Calculator(0).add(10).multiply(2)
        assert calc.history == ["init(0)", "add(10)", "multiply(2)"]


class TestCalculatorReset:
    def test_reset_to_zero(self):
        calc = Calculator(100).reset()
        assert calc.result == 0.0

    def test_reset_to_value(self):
        calc = Calculator(100).reset(42)
        assert calc.result == 42

    def test_reset_recorded_in_history(self):
        calc = Calculator(1).add(2).reset(0)
        assert "reset(0)" in calc.history


class TestCalculatorUndo:
    def test_undo_pops_last_history_entry(self):
        calc = Calculator(0).add(5).undo()
        assert calc.history == ["init(0)"]

    def test_undo_on_initial_state_raises(self):
        with pytest.raises(IndexError, match="Nothing to undo"):
            Calculator(0).undo()


class TestCalculatorHistoryImmutability:
    def test_history_returns_copy(self):
        calc = Calculator(0)
        history = calc.history
        history.append("fake")
        assert "fake" not in calc.history
