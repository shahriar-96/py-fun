import pytest
from calculator.calculator import Calculator


def test_calculator_initialization():
    """Test that the calculator initializes correctly."""
    calc = Calculator()
    assert calc is not None


def test_placeholder_functionality():
    """Basic assertion to verify test execution."""
    assert True


def test_calculator_basic_arithmetic():
    """Test add, sub, mul, and div operations."""
    calc = Calculator()
    assert calc.add(2, 3) == 5
    assert calc.sub(10, 4) == 6
    assert calc.mul(3, 4) == 12
    assert calc.div(20, 4) == 5


def test_calculator_words_and_factorize():
    """Test word parsing and prime factorization."""
    calc = Calculator()
    assert calc.add("two", "drei") == 5
    assert calc.factorize(12) == [2, 2, 3]
