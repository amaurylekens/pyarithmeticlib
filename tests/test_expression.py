#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest

from pyarithmeticlib.expression import (
    Multiplication,
    Substraction,
    Suboperand,
    Addition,
    Number
)

# test Number

# test Number.__init__
test_values = [
    (0, Number(0)),
    (1, Number(1)),
    (100, Number(100)),
    (-2, ValueError())
]


@pytest.mark.parametrize('value, expected', test_values)
def test_number_init(value, expected):

    if isinstance(expected, Exception):
        with pytest.raises(ValueError):
            Number(value)

    else:
        actual = Number(value)
        assert str(actual) == str(expected)


# test Number.evaluate
test_values = [
    (Number(0), 0),
    (Number(1), 1),
    (Number(100), 100)
]


@pytest.mark.parametrize('number, expected', test_values)
def test_number_evaluate(number, expected):

    actual = number.evaluate()
    assert actual == expected


# test Number.__str__
test_values = [
    (Number(0), "0"),
    (Number(1), "1"),
    (Number(100), "100")
]


@pytest.mark.parametrize('number, expected', test_values)
def test_number_str(number, expected):

    actual = str(number)
    assert actual == expected

# test Addition

# test Addition.evaluate
test_values = [
    (Number(0), Number(0), 0),
    (Number(1), Number(2), 3),
    (Number(2), Addition(Number(1), Number(2)), 5)
]


@pytest.mark.parametrize('left, right, expected', test_values)
def test_addition_evaluate(left, right, expected):

    addition = Addition(left, right)
    actual = addition.evaluate()

    assert actual == expected


# test Addition.__str__
test_values = [
    (Number(0), Number(0), "0 + 0"),
    (Number(1), Number(2), "1 + 2"),
    (Number(2), Addition(Number(1), Number(2)), "2 + 1 + 2")
]


@pytest.mark.parametrize('left, right, expected', test_values)
def test_addition_str(left, right, expected):

    actual = Addition(left, right)

    assert str(actual) == expected


# test Substraction

# test Substraction.evaluate
test_values = [
    (Number(0), Number(0), 0),
    (Number(2), Number(1), 1),
    (Number(1), Number(2), -1),
    (Addition(Number(1), Number(2)), Number(2), 1),
    (Number(2), Addition(Number(1), Number(2)), -1)
]


@pytest.mark.parametrize('left, right, expected', test_values)
def test_substraction_evaluate(left, right, expected):

    addition = Substraction(left, right)
    actual = addition.evaluate()

    assert actual == expected


# test Substraction.__str__
test_values = [
    (Number(0), Number(0), "0 - 0"),
    (Number(2), Number(1), "2 - 1"),
    (Addition(Number(1), Number(2)), Number(2), "1 + 2 - 2"),
    (Number(2), Addition(Number(1), Number(2)), "2 - (1 + 2)")
]


@pytest.mark.parametrize('left, right, expected', test_values)
def test_substraction_str(left, right, expected):

    actual = Substraction(left, right)

    assert str(actual) == expected


# test Multiplication

# test Multiplication.evaluate
test_values = [
    (Number(0), Number(0), 0),
    (Number(2), Number(1), 2),
    (Number(1), Number(2), 2),
    (Addition(Number(1), Number(2)), Number(2), 6),
    (Number(2), Addition(Number(1), Number(2)), 6)
]


@pytest.mark.parametrize('left, right, expected', test_values)
def test_multiplication_evaluate(left, right, expected):

    multiplication = Multiplication(left, right)
    actual = multiplication.evaluate()

    assert actual == expected


# test Multiplication.__str__
test_values = [
    (Number(0), Number(0), "0 * 0"),
    (Number(2), Number(1), "2 * 1"),
    (Addition(Number(1), Number(2)), Number(2), "(1 + 2) * 2"),
    (Number(2), Addition(Number(1), Number(2)), "2 * (1 + 2)")
]


@pytest.mark.parametrize('left, right, expected', test_values)
def test_multiplication_str(left, right, expected):

    actual = Multiplication(left, right)

    assert str(actual) == expected


# test Suboperand

# test Suboperand.evaluate
test_values = [
    (Number(0), 0),
    (Addition(Number(1), Number(2)), 3),
    (Substraction(Number(2), Addition(Number(1), Number(2))), -1)
]


@pytest.mark.parametrize('operand, expected', test_values)
def test_suboperand_evaluate(operand, expected):

    suboperand = Suboperand(operand)
    actual = suboperand.evaluate()

    assert actual == expected


# test Suboperand.__str__
test_values = [
    (Number(0), "(0)"),
    (Number(2), "(2)"),
    (Addition(Number(1), Number(2)), "(1 + 2)"),
    (Substraction(Number(2), Addition(Number(1), Number(2))), "(2 - (1 + 2))")
]


@pytest.mark.parametrize('operand, expected', test_values)
def test_suboperand_str(operand, expected):

    actual = Suboperand(operand)

    assert str(actual) == expected


# test Operand

# test Operand.__eq__

test_values = [
    (Number(0), Number(0), True),
    (Number(1), Number(0), False),
    (Addition(Number(2), Number(1)), Number(3), True),
    (
        Addition(Number(2), Number(1)),
        Suboperand(Substraction(Number(3), Number(0))),
        True
    ),
    (Number(0), 0, ValueError())
]


@pytest.mark.parametrize('operand_a, operand_b, expected', test_values)
def test_operand_eq(operand_a, operand_b, expected):

    if isinstance(expected, Exception):
        with pytest.raises(ValueError):
            actual = operand_a == operand_b

    else:
        actual = operand_a == operand_b
        assert actual == expected


# test Operand.__gt__

test_values = [
    (Number(0), Number(0), False),
    (Number(1), Number(0), True),
    (Addition(Number(3), Number(1)), Number(3), True),
    (
        Addition(Number(2), Number(1)),
        Suboperand(Substraction(Number(3), Number(0))),
        False
    ),
    (Number(0), 0, ValueError())
]


@pytest.mark.parametrize('operand_a, operand_b, expected', test_values)
def test_operand_gt(operand_a, operand_b, expected):

    if isinstance(expected, Exception):
        with pytest.raises(ValueError):
            actual = operand_a > operand_b

    else:
        actual = operand_a > operand_b
        assert actual == expected
