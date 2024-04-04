#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest

from pyarithmetic.generator import ExpressionGenerator
from pyarithmetic.expression import (
    Multiplication,
    Substraction,
    Suboperand,
    Addition,
    Number
)

SEED = 42  # Must stay fixed


# test ExpressionGenerator

# test ExpressionGenerator.__init__

test_values = [
    (
        0, 0, 1, 1, 1, 1, 1, {Addition, Substraction, Multiplication},
        ValueError()
    ),
    (
        0, 2, 1, 1, 1, 1, 1, {Addition, Substraction, Multiplication},
        ValueError()
    ),
    (
        0, 1, 1, 2, 1, 1, 1, {Addition, Substraction, Multiplication},
        ValueError()
    ),
    (
        0, 1, 1, 1, 1, 0, 1, {Addition, Substraction, Multiplication},
        ValueError()
    ),
    (
        0, 1, 1, 1, 1, 2, 1, {Addition, Substraction, Multiplication},
        ValueError()
    ),
    (
        0, 1, 1, 1, 1, 1, 1, set(),
        ValueError()
    )
]

@pytest.mark.parametrize(
    'max_depth, min_length, max_length, min_value, max_value, min_n_operands, '
    'max_n_operands, allowed_operations, expected', test_values
)
def test_expression_generator_init(
    max_depth, min_length, max_length, min_value, max_value, min_n_operands,
    max_n_operands, allowed_operations, expected
):

    if isinstance(expected, Exception):
        with pytest.raises(ValueError):
            actual = ExpressionGenerator(
                max_depth, min_length, max_length, min_value, max_value,
                min_n_operands, max_n_operands, allowed_operations
            )

    else:
        actual = ExpressionGenerator(
            max_depth, min_length, max_length, min_value, max_value,
            min_n_operands, max_n_operands, allowed_operations
        )
        assert actual == expected


# test ExpressionGenerator.generate

test_values = [
    (
        0, 1, 1, 1, 1, 1, 1, {Addition, Substraction, Multiplication}, 3,
        Number(1)
    ),
    (
        1, 2, 3, 1, 10, 1, 2, [Addition, Substraction, Multiplication], 3,
        Multiplication(
            Suboperand(Suboperand(Substraction(Number(10), Number(8)))),
            Number(8)
        )
    ),
    (
        1, 2, 3, 1, 10, 1, 2, [Addition, Substraction, Multiplication], 103,
        Addition(
            Number(10),
            Addition(
                Suboperand(Suboperand(Addition(Number(2), Number(2)))),
                Number(1)
            )
        )
    ),
    (
        1, 2, 4, 1, 30, 1, 3, [Addition, Substraction, Multiplication], 2,
        Addition(
            Number(12),
            Suboperand(Suboperand(Multiplication(Number(20), Number(19)))),
        )
    )
]


@pytest.mark.parametrize(
    'max_depth, min_length, max_length, min_value, max_value, min_n_operands, '
    'max_n_operands, allowed_operations, seed, expected', test_values
)
def test_expression_generate(
    max_depth, min_length, max_length, min_value, max_value, min_n_operands,
    max_n_operands, allowed_operations, seed, expected
):

    generator = ExpressionGenerator(
        max_depth=max_depth,
        min_length=min_length,
        max_length=max_length,
        min_value=min_value,
        max_value=max_value,
        min_n_operands=min_n_operands,
        max_n_operands=max_n_operands,
        allowed_operations=allowed_operations,
        seed=seed
    )

    generator._set_seed()

    actual = generator.generate()

    assert str(actual) == str(expected)


# test ExpressionGenerator.generate

test_values = [
    (
        0, 1, 1, 1, 1, 1, 1, {Addition, Substraction, Multiplication}, 3, 1,
        [Number(1)]
    ),
    (
        1, 2, 3, 1, 10, 1, 2, [Addition, Substraction, Multiplication], 3, 2,
        [
            Multiplication(
                Suboperand(Suboperand(Substraction(Number(10), Number(8)))),
                Number(8)
            ),
            Multiplication(
                Multiplication(
                    Substraction(Number(4), Number(9)),
                    Number(3)
                ),
                Suboperand(Number(8))
            )
        ]
    ),
    (
        1, 2, 3, 1, 10, 1, 2, [Addition, Substraction, Multiplication], 103, 3,
        [
            Addition(
                Number(10),
                Addition(
                    Suboperand(Suboperand(Addition(Number(2), Number(2)))),
                    Number(1)
                )
            ),
            Multiplication(
                Substraction(
                    Number(7),
                    Suboperand(Number(2))
                ),
                Number(10)
            ),
            Addition(
                Multiplication(
                    Substraction(Suboperand(Number(9)), Number(9)),
                    Suboperand(Number(7))
                ),
                Suboperand(
                    Substraction(
                        Number(8),
                        Suboperand(Number(5))
                    )
                )
            )
        ]
    )
]


@pytest.mark.parametrize(
    'max_depth, min_length, max_length, min_value, max_value, min_n_operands, '
    'max_n_operands, allowed_operations, seed, n, expected', test_values
)
def test_expression_generate(
    max_depth, min_length, max_length, min_value, max_value, min_n_operands,
    max_n_operands, allowed_operations, seed, n, expected
):

    generator = ExpressionGenerator(
        max_depth=max_depth,
        min_length=min_length,
        max_length=max_length,
        min_value=min_value,
        max_value=max_value,
        min_n_operands=min_n_operands,
        max_n_operands=max_n_operands,
        allowed_operations=allowed_operations,
        seed=seed
    )

    actual = [str(expr) for expr in generator.yield_expressions(n)]
    expected = [str(expr) for expr in expected]

    assert str(actual) == str(expected)
