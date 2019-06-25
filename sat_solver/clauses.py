"""
Verifications and manipulations of the clauses such as integer substitutions
or mono-literal checks.
"""

from __future__ import annotations
from typing import *
import string


class Clauses:
    """Set of clauses in conjunctive normal form."""

    def __init__(self, clauses: FrozenSet[FrozenSet[int]]) -> None:
        self._clauses: FrozenSet[FrozenSet[int]] = clauses

    @classmethod
    def from_str(cls, clauses: FrozenSet[FrozenSet[str]]):
        return cls(cls.convert_literals_to_integers(clauses))

    @classmethod
    def from_int(cls, clauses: FrozenSet[FrozenSet[int]]):
        return cls(clauses)

    @staticmethod
    def is_mono_literal(clause: FrozenSet[int]) -> bool:
        """Return true if the argument is a mono-literal."""
        return len(clause) == 1

    @staticmethod
    def convert_literals_to_integers(clauses: FrozenSet[FrozenSet[str]])\
            -> FrozenSet[FrozenSet[int]]:
        """ Replace literals in each clause with an integer corresponding
    to its position + 1 in the alphabet. If the literal is negative,
    the integer takes a negative value.

    1 is added to avoid the case of 0, which is problematic to work with
    (-0 is the same as +0, and the sign will disappear).
    """
        output: List[FrozenSet[int]] = []
        for formula in clauses:
            for char in formula:
                if char.isalpha():
                    output.append(string.ascii_letters.index(char) + 1)
                elif char == "¬":
                    output[-1] *= -1
        return frozenset(output)

    def _unit_propagate(self, mono_literal: List[str]) -> Clauses:
        clauses = self.clauses
        return Clauses(clauses)

    def contains_only_mono_literals(self) -> bool:
        """Return True if the list contains only mono-literals."""
        return True if [clause for clause in self.clauses
                        if not self.is_mono_literal(clause)] else False

    def find_mono_literals(self) -> FrozenSet[int]:
        """Return a FrozenSet containing every mono-literal."""
        return FrozenSet(clause for clause in self.clauses
                         if self.is_mono_literal(clause))

    def is_consistant_set_of_literals(self) -> bool:
        """Return True if the list contains a consistent set of literals.

        A consistent set of literals is a set that doesn't contain a literal
        and its contrary.
        """
        return False if {clause for clause in self.clauses
                         if not self.is_mono_literal(clause)} else True

    def contains_empty_clause(self):
        """Return True if the list contains an empty clause."""
        return bool([clause for clause in self.clauses if not clause])

    @property
    def yield_clauses(self):
        for clause in self.clauses:
            yield clause

    @property
    def clauses(self):
        return self._clauses
