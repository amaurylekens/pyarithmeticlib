#!/usr/bin/python
# -*- coding: utf-8 -*-


from abc import ABC, abstractmethod


class Operand(ABC):

    """
    An abstract base class representing an operand in an arithmetic expression.
    It requires subclasses to implement `evaluate` and `__str__` methods.
    """

    @abstractmethod
    def evaluate(self) -> int:

        """
        Evaluates and returns the value of the operand.

        :return: The value of the operand.
        :rtype: int
        """

        pass

    @abstractmethod
    def __str__(self):

        pass

    def __hash__(self):

        return hash(str(self))


class Number(Operand):

    """
    Represents a numeric value in an arithmetic expression.
    """

    def __init__(self, value: int):

        """
        :param value: The numeric value of this operand.
        :type value: int
        """

        self.value = value

    def evaluate(self) -> int:

        """
        Evaluates and returns the value of the operand.

        :return: The value of the operand.
        :rtype: int
        """

        return self.value

    def __str__(self):

        return str(self.value)


class Suboperand(Operand):

    """
    Represents a suboperand, encapsulating another operand within parentheses.
    """

    def __init__(self, operand: Operand):

        """
        :param operand: The operand to be encapsulated.
        :type operand: Operand
        """

        self._operand = operand

    def evaluate(self) -> int:

        """
        Evaluates and returns the value of the operand.

        :return: The value of the operand.
        :rtype: int
        """

        return self._operand.evaluate()

    def __str__(self):

        return f"({str(self._operand)})"


class BinaryOperation(Operand):

    """
    An abstract base class for binary operations, representing an operation
    between two operands.
    """

    def __init__(self, left: Operand, right: Operand):

        """
        :param left: The left operand of the binary operation.
        :type left: Operand
        :param right: The right operand of the binary operation.
        :type right: Operand
        """

        self._left = left
        self._right = right

    def evaluate(self) -> int:

        """
        Evaluates and returns the value of the operand.

        :return: The value of the operand.
        :rtype: int
        """

        pass

    def __str__(self):
        pass


class Addition(BinaryOperation):

    """
    Represents an addition operation between two operands.
    """

    def evaluate(self) -> int:

        """
        Evaluates and returns the value of the operand.

        :return: The value of the operand.
        :rtype: int
        """

        return self._left.evaluate() + self._right.evaluate()

    def __str__(self):

        return f"{str(self._left)} + {str(self._right)}"


class Substraction(BinaryOperation):

    """
    Represents a subtraction operation between two operands.
    """

    def evaluate(self) -> int:

        """
        Evaluates and returns the value of the operand.

        :return: The value of the operand.
        :rtype: int
        """

        return self._left.evaluate() - self._right.evaluate()

    def __str__(self):

        left_str = str(self._left)
        right_str = f"({str(self._right)})" \
            if isinstance(self._right, BinaryOperation) \
            else f"{str(self._right)}"

        return f"{left_str} - {right_str}"


class Multiplication(BinaryOperation):

    """
    Represents a multiplication operation between two operands.
    """

    def evaluate(self) -> int:

        """
        Evaluates and returns the value of the operand.

        :return: The value of the operand.
        :rtype: int
        """

        return self._left.evaluate() * self._right.evaluate()

    def __str__(self):

        left_str = f"({str(self._left)})" \
            if isinstance(self._left, BinaryOperation) \
            else f"{str(self._left)}"
        right_str = f"({str(self._right)})" \
            if isinstance(self._right, BinaryOperation) \
            else f"{str(self._right)}"

        return f"{left_str} * {right_str}"


if __name__ == '__main__':

    expr1 = Suboperand(Substraction(Number(3), Addition(Number(1), Number(2))))
    expr2 = Multiplication(Substraction(Number(5), expr1), Number(3))
    expr3 = Multiplication(
        Addition(Multiplication(Number(5), Number(3)), Number(4)), expr2
    )

    print(expr1, '->', expr1.evaluate())
    print(expr2, '->', expr2.evaluate())
    print(expr3, '->', expr3.evaluate())

    print(hash(expr3))
