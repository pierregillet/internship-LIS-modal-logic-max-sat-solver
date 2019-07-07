"""
Verifications and manipulations of the clauses such as unit propagation
or mono-literal checks.
"""

from __future__ import annotations
from itertools import chain
from typing import *


class Clauses:
    """Class containing a set of clauses in conjunctive normal form."""

    def __init__(self, clauses: FrozenSet[FrozenSet[int]],
                 translation: Dict[str, int] = None):
        """Construct an object from clauses with literals as integers."""
        self._clauses: FrozenSet[FrozenSet[int]] = clauses
        self._translation: Dict[str, int] = translation

    @classmethod
    def from_int(cls, clauses: FrozenSet[FrozenSet[int]],
                 translation: Dict[str, int] = None) -> Clauses:
        """Return an instance of this class from clauses with literals
        as integers.
        """
        return cls(clauses, translation)

    @classmethod
    def from_str(cls, clauses: Tuple[Tuple[str, ...], ...]) -> Clauses:
        """Return an instance of this class from clauses with literals
        as strings. They will be replaced with integers.

        Replace literals in the formula with an integer greater than 2 (to
        keep 0 for False and 1 for True).
        If the literal is negative, the integer takes a negative value.
        """
        _OFFSET = 2  # Offset to avoid adding 0 and 1 to the translation table.
        translation: Dict[str, int] = {}
        unique_propositions = Clauses.get_distinct_propositions(clauses)
        for index, value in enumerate(unique_propositions):
            translation[value] = index + _OFFSET
        clauses_as_int = frozenset(Clauses.str_to_int(clause, translation)
                                   for clause in clauses)

        return cls(clauses_as_int, translation)

    @staticmethod
    def str_to_int(clause: Tuple[str, ...], translation: Dict[str, int])\
            -> FrozenSet[int]:
        """Replace literals in the formula with an integer corresponding
        to its position + 1 in the alphabet. If the literal is negative,
        the integer takes a negative value.

        1 is added to avoid the case of 0, which is problematic to work with
        (-0 is the same as +0, and the sign will disappear).
        """
        output: List[int] = []
        for operand in clause:
            if operand == "¬":
                output[-1] *= -1
            else:
                if operand not in translation:
                    raise ValueError(f"{operand} was not found"
                                     f" in the translation table.")
                output.append(translation[operand])
        return frozenset(output)

    @staticmethod
    def is_clausal_form(formula: Tuple[str, ...]) -> bool:
        for element in formula:
            if not element.isalpha() and element not in ["∧", "∨"]:
                return False
        return True

    def split_to_clauses(self):
        pass

    @staticmethod
    def is_mono_literal(clause: FrozenSet[int]) -> bool:
        """Return true if the argument is a mono-literal."""
        return len(clause) == 1

    def add_clause_to_copy(self, clause: FrozenSet[int]) -> Clauses:
        """Return a new instance of Clauses with the parameter added."""
        clauses: List[FrozenSet[int]] = list(self.clauses)
        clauses.append(clause)
        return Clauses.from_int(frozenset(clauses), self.translation)

    def unit_propagate(self, mono_literal: int) -> Clauses:
        """Propagates the mono-literal in the whole formula.

        Remove all the clauses containing the mono-literal, and remove the
        negative value of the mono-literal from the clauses containing it.
        """
        clauses: List[List[int]] = list(map(list, self.clauses))
        for clause in clauses[:]:
            if mono_literal in clause:
                clauses.remove(clause)
            elif -mono_literal in clause:
                clause.remove(-mono_literal)
        return Clauses(frozenset(map(frozenset, clauses)), self.translation)

    def find_pure_literals(self) -> Set[int]:
        """Return a set containing every pure literal in the formula.

        A pure literal is a literal whose contrary doesn't exist
        in the formula.
        """
        literals_set = set(chain.from_iterable(self.clauses))
        return {literal for literal in literals_set
                if -literal not in literals_set}

    def assign_pure_literal(self, pure_literal: int) -> Clauses:
        """Assign the pure literal passed as parameter.

        The returned object only contains clauses without the pure literal.
        """
        clauses = list(filter(lambda x: pure_literal not in x, self.clauses))
        clauses = frozenset(map(frozenset, clauses))
        return Clauses(clauses, self.translation)

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
        flat_set = self.get_distinct_propositions(self.clauses)
        inconsistencies = frozenset(filter(lambda x: -x in flat_set, flat_set))
        return False if inconsistencies else True

    def contains_empty_clause(self):
        """Return True if the list contains an empty clause."""
        return bool(list(filter(lambda x: not x, self.clauses)))

    @staticmethod
    def get_distinct_propositions(clauses: Collection) -> frozenset:
        propositions = filter(lambda x: x != "¬", chain.from_iterable(clauses))
        return frozenset(propositions)

    # def get_distinct_int_propositions(self) -> FrozenSet[int]:
    #     return frozenset(chain.from_iterable(self.clauses))

    @property
    def clauses(self):
        return self._clauses

    @property
    def translation(self):
        return self._translation

    @property
    def literal_clauses(self):
        output = set()
        for clause in self.clauses:
            current_clause = set()
            for proposition in clause:
                for key, value in self._translation.items():
                    if value == proposition:
                        current_clause.add(key)
            output.add(frozenset(current_clause))
        return frozenset(output)
