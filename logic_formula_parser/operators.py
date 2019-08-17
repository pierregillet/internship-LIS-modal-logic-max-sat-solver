from __future__ import annotations
from typing import *


class Proposition:
    def __init__(self, literal: str) -> None:
        self.literal = literal

    def __eq__(self, o: Proposition) -> bool:
        return isinstance(o, Proposition) and self.literal == o.literal

    def __hash__(self):
        return hash(self.literal)

    def __str__(self) -> str:
        return str(self.literal)


class Operator:
    def __init__(self, left: Formula = None, right: Formula = None) -> None:
        if not left and not right:
            raise ValueError("Both children of the operator are None.")
        self.left = left
        self.right = right

    def __eq__(self, o: Operator) -> bool:
        if not isinstance(o, Operator):
            return False
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
    def __str__(self) -> str:
        return f'¬{self.right}'


class L(UnaryOperator):
    def __str__(self) -> str:
        return f'L{self.right}'


class LNot(UnaryOperator):
    def __str__(self) -> str:
        return f'L¬{self.right}'


class H(UnaryOperator):
    def __str__(self) -> str:
        return f'H{self.right}'


class HNot(UnaryOperator):
    def __str__(self) -> str:
        return f'H¬{self.right}'


class HBox(UnaryOperator):
    def __str__(self) -> str:
        return f'[H]{self.right}'


class HBoxNot(UnaryOperator):
    def __str__(self) -> str:
        return f'[H]¬{self.right}'


class And(Operator):
    def __str__(self) -> str:
        return f'{self.left}∧{self.right}'


class Or(Operator):
    def __str__(self) -> str:
        return f'{self.left}∨{self.right}'


class Imply(Operator):
    def __str__(self) -> str:
        return f'{self.left}→{self.right}'


Formula = NewType('SubFormula', Union[Operator, Proposition])
Leaf = NewType('Leaf', Union[UnaryOperator, Proposition])
