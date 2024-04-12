#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Set, Type, Generator, Optional
from random import Random

from pyarithmeticlib.expression import (
    BinaryOperation,
    Multiplication,
    Suboperand,
    Addition,
    Operand,
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
        allowed_operations: Set[Type[BinaryOperation]],
        seed: Optional[int] = None
    ):

        """
        :param max_depth: Maximum depth of nested operations in the expression.
        :type max_depth: int
        :param min_length: Minimum length of the expression in terms of number
                           of operand.
        :type max_depth: int
        :param max_length: Maximum length of the expression in terms of number
                           of operands.
        :type max_length: int
        :param min_value: Minimum numeric value for number in the expression.
        :type min_value: int
        :param max_value: Maximum numeric value for number in the expression.
        :type min_value: int
        :param min_n_operands: Minimum number of operands inside an operand.
        :type min_n_operands: int
        :param max_n_operands: Maximum number of operands inside an operand.
        :type max_n_operands: int
        :param allowed_operations: Set of allowed binary operation classes.
        :type allowed_operations: Set[Type[BinaryOperation]]
        :param seed: Optional seed for random number generator to ensure
                     reproducible results. If provided, the generator will
                     produce the same sequence of expressions for the same seed
                     value. If not provided, the sequence of expressions will
                     be random and different each time.
        :type seed: Optional[int]

        :raises ValueError: If any of the minimum values are greater than the
                            corresponding maximum values, or if the allowed
                            operations set is empty.
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

        if min_n_operands < 1:
            raise ValueError("min_n_operands must be at least 1.")

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

        self._seed = seed

        if seed:
            self._random = Random(seed)
        else:
            self._random = Random()

    def _random_number(self) -> int:

        return self._random.randint(self._min_value, self._max_value)

    def _random_operation(self) -> Type[BinaryOperation]:

        return self._random.choice(list(self._allowed_operations))

    def _random_operand_type(self) -> str:

        return self._random.choice(['number', 'suboperand'])

    def _random_n_operands(self) -> int:

        return self._random.randint(self._min_n_operands, self._max_n_operands)

    def _random_length(self) -> int:

        return self._random.randint(self._min_length, self._max_length)

    def _create_number(self) -> Number:

        """
        Generates a Number instance with a value within the specified range.

        :return: A Number instance.
        :rtype: Number
        """

        return Number(self._random_number())

    def _create_operation(
        self, left: Operand, right: Operand
    ) -> BinaryOperation:

        """
        Generates an instance of a randomly chosen allowed binary operation
        with the given left and right operands.

        :param left: The left operand of the binary operation.
        :type left: Operand
        :param right: The right operand of the binary operation.
        :type right: Operand

        :return: An instance of a BinaryOperation subclass.
        :rtype: BinaryOperation
        """

        operation = self._random_operation()

        return operation(left, right)

    def _generate_operand(self, depth: int = 0) -> Operand:

        """
        Recursively generates a complex operand composed of numbers,
        suboperands, and binary operations up to the specified depth.

        :param depth: The current depth in the operand tree.
        :type depth: int

        :return: A complex operand possibly containing nested operations.
        :rtype: Operand
        """

        n_operands = self._random_n_operands()

        operands = list()
        for _ in range(n_operands):

            operand_type = self._random_operand_type()

            if operand_type == 'number' or depth == self._max_depth:
                operands.append(self._create_number())

            elif operand_type == 'suboperand':
                operands.append(Suboperand(self._generate_operand(depth + 1)))

        componed_operand = operands[0]
        for operand in operands[1:]:
            componed_operand = self._create_operation(
                componed_operand, operand
            )

        if len(operands) > 1:
            componed_operand = Suboperand(componed_operand)

        return componed_operand

    def generate(self) -> Operand:

        """
        Generates an arithmetic expression based on the initialized criteria.

        :return: The root of the generated arithmetic expression tree.
        :rtype: Operand

        :Example:
            >>> generator = ExpressionGenerator(
            ...     max_depth=2, min_length=2, max_length=4, min_value=1,
            ...     max_value=10, min_n_operands=1, max_n_operands=3,
            ...     allowed_operations={Addition, Multiplication}, seed=42
            ... )
            >>> expr = generator.generate()
            >>> print(expr)
            3 + 4 + (2 * 2)
        """

        length = self._random_length()
        operands = [self._generate_operand() for _ in range(length)]

        expression = operands[0]
        for next_expr in operands[1:]:
            expression = self._create_operation(expression, next_expr)

        return expression

    def yield_expressions(self, n: int) -> Generator[Operand, None, None]:

        """
        Yields a specified number of unique arithmetic expressions based on the
        initialized criteria. Uniqueness is determined by the string
        representation of the expressions.

        :param n: The number of unique expressions to generate.
        :type n: int

        :return: A list of unique Operand instances.
        :rtype: List[Operand]

        :raises RuntimeError: If it fails to generate the required number of
                              unique expressions within a reasonable number of
                              attempts.

        :Example:
            >>> generator = ExpressionGenerator(
            ...     max_depth=2, min_length=2, max_length=4, min_value=1,
            ...     max_value=10, min_n_operands=1, max_n_operands=3,
            ...     allowed_operations={Addition, Multiplication}, seed=42
            ... )
            >>> unique_expressions = list(generator.yield_expressions(5))
            >>> for expr in unique_expressions:
            ...     print(expr)
            3 + 2
            (1 * 2) + 3
            4 * (2 + 1)
            2 + (3 * 1)
            (4 + 1) * 2
        """

        expressions = set()
        attempts = 0
        max_attempts = n * 10  # Arbitrary choice to prevent infinite loops

        while len(expressions) < n and attempts < max_attempts:
            expression = self.generate()
            if expression not in expressions:
                expressions.add(expression)
                yield expression
            attempts += 1

        if attempts == max_attempts:
            raise RuntimeError(
                f"Failed to yields {n} unique expressions after "
                f"{max_attempts} attempts."
            )
