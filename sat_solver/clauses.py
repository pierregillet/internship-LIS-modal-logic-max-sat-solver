"""
Verifications and manipulations of the clauses such as unit propagation
or mono-literal checks.
"""

from __future__ import annotations
from itertools import chain
from typing import *


class Clauses:
    """Set of clauses in conjunctive normal form."""

    def __init__(self, clauses: FrozenSet[FrozenSet[int]]) -> None:
        self._clauses: FrozenSet[FrozenSet[int]] = clauses

    @classmethod
    def from_int(cls, clauses: FrozenSet[FrozenSet[int]]):
        return cls(clauses)

    @staticmethod
    def is_mono_literal(clause: FrozenSet[int]) -> bool:
        """Return true if the argument is a mono-literal."""
        return len(clause) == 1

    def _unit_propagate(self, mono_literal: int) -> Clauses:
        clauses: Set[Set[int]] = set(map(set, self.clauses))

        for clause in clauses:
            if mono_literal in clause:
                clauses.remove(clause)
            elif -mono_literal in clause:
                clause.remove(-mono_literal)

        return Clauses(frozenset(map(frozenset, clauses)))

    def contains_only_mono_literals(self) -> bool:
        """Return True if the list contains only mono-literals."""
        multi_literals = filter(
            lambda x: not self.is_mono_literal(x), self.clauses
        )
        return True if not multi_literals else False

    def find_mono_literals(self) -> FrozenSet[int]:
        """Return a FrozenSet containing every mono-literal."""
        return frozenset(chain.from_iterable(
            filter(lambda x: self.is_mono_literal(x), self.clauses)
        ))

    def is_consistant_set_of_literals(self) -> bool:
        """Return True if the list contains a consistent set of literals.

        A consistent set of literals is a set that doesn't contain a literal
        and its contrary.
        """
        flat_set = frozenset(chain.from_iterable(self.clauses))
        inconsistencies = frozenset(filter(lambda x: -x in flat_set, flat_set))
        return False if inconsistencies else True

    def contains_empty_clause(self):
        """Return True if the list contains an empty clause."""
        return bool(list(filter(lambda x: not x, self.clauses)))

    @property
    def clauses(self):
        return self._clauses
