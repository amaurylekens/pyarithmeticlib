#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Set, Type
import random

from expression import (
    BinaryOperation,
    Suboperand,
    Number
)


class ExpressionGenerator:

    """
    Class to Generate arithmetic expressions based on specified criteria
    including depth, length, value ranges, number of operands, and allowed
    operations.
    """

    def __init__(
        self, max_depth: int, min_length: int, max_length: int, min_value: int,
        max_value: int, min_n_operands: int, max_n_operands: int,
        allowed_operations: Set[Type[BinaryOperation]]
    ):

        """
        :param max_depth: Maximum depth of nested operations in the expression.
        :param min_length: Minimum length of the expression in terms of number
                           of operand.
        :param max_length: Maximum length of the expression in terms of number
                           of operands.
        :param min_value: Minimum numeric value for number in the expression.
        :param max_value: Maximum numeric value for number in the expression.
        :param min_n_operands: Minimum number of operands inside an operand.
        :param max_n_operands: Maximum number of operands inside an operand.
        :param allowed_operations: Set of allowed binary operation classes.
        """

        if max_depth < 0:
            raise ValueError("max_depth must be at least 0.")

        if min_length < 1:
            raise ValueError("min_length must be at least 1.")

        if max_length < min_length:
            raise ValueError(
                "max_length must be greater than or equal to min_length."
            )

        if max_value < min_value:
            raise ValueError(
                "max_value must be greater than or equal to min_value."
            )

        if max_n_operands < min_n_operands:
            raise ValueError(
                "max_n_operands must be greater than or equal to "
                "min_n_operands."
            )

        if not allowed_operations:
            raise ValueError(
                "allowed_operations must not be empty."
            )

        self._max_depth = max_depth
        self._min_length = min_length
        self._max_length = max_length
        self._min_value = min_value
        self._max_value = max_value
        self._min_n_operands = min_n_operands
        self._max_n_operands = max_n_operands
        self._allowed_operations = allowed_operations

    def create_number(self):

        return Number(random.randint(self._min_value, self._max_value))

    def create_operation(self, left, right):

        if not self._allowed_operations:
            raise ValueError("No allowed operations specified")

        op = random.choice(list(self._allowed_operations))

        return op(left, right)

    def generate_operand(self, depth=0):

        n_operands = random.randint(self._min_n_operands, self._max_n_operands)

        operands = list()
        for _ in range(n_operands):

            operand_type = random.choice(
                ['number', 'suboperand']
            )
            if operand_type == 'number' or depth == self._max_depth:
                operands.append(self.create_number())

            elif operand_type == 'suboperand':
                operands.append(Suboperand(self.generate_operand(depth + 1)))

        componed_operand = operands[0]
        for operand in operands[1:]:
            componed_operand = self.create_operation(
                componed_operand, operand
            )

        if len(operands) > 1:
            componed_operand = Suboperand(componed_operand)

        return componed_operand

    def generate(self):

        length = random.randint(self._min_length, self._max_length)
        operands = [self.generate_operand() for _ in range(length)]

        expression = operands[0]
        for next_expr in operands[1:]:
            expression = self.create_operation(expression, next_expr)

        return expression


if __name__ == '__main__':

    from expression import Addition

    max_depth = 0
    min_length = 1
    max_length = 3
    min_value = 0
    max_value = 100
    min_n_operands = 1
    max_n_operands = 1
    allowed_operations = {Addition}

    generator = ExpressionGenerator(
        max_depth=max_depth,
        min_length=min_length,
        max_length=max_length,
        min_value=min_value,
        max_value=max_value,
        min_n_operands=min_n_operands,
        max_n_operands=max_n_operands,
        allowed_operations=allowed_operations,
    )

    expr = generator.generate()

    print(expr)
    print(expr.evaluate())
