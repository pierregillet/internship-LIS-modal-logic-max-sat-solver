from __future__ import annotations
from typing import *


class Proposition:
    def __init__(self, literal: str) -> None:
        self.literal = literal

    def __eq__(self, o: Proposition) -> bool:
        return isinstance(o, Proposition) and self.literal == o.literal

    def __hash__(self):
        return hash(self.literal)


class Operator:
    def __init__(self, left: Formula = None, right: Formula = None) -> None:
        if not left and not right:
            raise ValueError("Both children of the operator are None.")
        self.left = left
        self.right = right

    def __eq__(self, o: Operator) -> bool:
        return self.left == o.left and self.right == o.right

    def __hash__(self):
        return hash((self.left, self.right))

    @property
    def children(self):
        return [self.left, self.right]


class UnaryOperator(Operator):
    def __init__(self, right: Leaf) -> None:
        super().__init__(right=right)


class Not(UnaryOperator):
    pass


class Box(UnaryOperator):
    pass


class BoxNot(UnaryOperator):
    pass


class Diamond(UnaryOperator):
    pass


class DiamondNot(UnaryOperator):
    pass


class Imply(Operator):
    pass


class And(Operator):
    pass


class Or(Operator):
    pass


Formula = NewType('SubFormula', Union[Operator, Proposition])
Leaf = NewType('Leaf', Union[UnaryOperator, Proposition])

# class Proposition:
#     def __init__(self, literal: str) -> None:
#         self.literal = literal
#
#
# class Operator:
#     pass
#
#
# class Formula:
#     def __init__(self, formula: Union[Operator, Proposition]) -> None:
#         self.formula = formula
#
#
# class UnaryOperator(Operator):
#     def __init__(self, right: Union[Operator, Proposition]) -> None:
#         self.right = right
#
#
# class TerminalUnaryOperator(UnaryOperator):
#     def __init__(self, right: Proposition) -> None:
#         super().__init__(right)
#
#
# class BinaryOperator(Operator):
#     def __init__(self, left: Union[Operator, Proposition],
#                  right: Union[Operator, Proposition]) -> None:
#         self.left = left
#         self.right = right
#
#
# class Not(UnaryOperator):
#     pass
#
#
# class Box(TerminalUnaryOperator):
#     pass
#
#
# class BoxNot(TerminalUnaryOperator):
#     pass
#
#
# class Diamond(TerminalUnaryOperator):
#     pass
#
#
# class DiamondNot(TerminalUnaryOperator):
#     pass
#
#
# class Imply(BinaryOperator):
#     pass
#
#
# class And(BinaryOperator):
#     pass
#
#
# class Or(BinaryOperator):
#     pass
#
