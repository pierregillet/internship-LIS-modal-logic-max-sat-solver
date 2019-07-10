"""
Verifications and manipulations of the clauses such as unit propagation
or mono-literal checks.
"""

from __future__ import annotations
from itertools import chain
from typing import *

from logic_formula_parser import logic_parser


class Clauses:
    """Class containing a set of clauses in conjunctive normal form."""

    def __init__(self, clauses: List[Set[int]],
                 translation: Dict[str, int] = None):
        """Construct an object from clauses with propositions as integers.
        Each clause must be its own list element (they must already be split).
        """
        self._clauses: List[Set[int]] = clauses
        self._translation: Dict[str, int] = translation

    def __copy__(self):
        """Create a shallow copy."""
        return Clauses(self._clauses[:], self.translation.copy())

    @classmethod
    def from_int(cls, clauses: List[Set[int]],
                 translation: Dict[str, int] = None) -> Clauses:
        """Return an instance of this class from clauses with literals
        as integers.
        """
        return cls(clauses, translation)

    @classmethod
    def from_str(cls, clauses: List[List[str]]) -> Clauses:
        """Create an instance of this class from clauses with propositions
        as strings. They will be replaced with integers.

        Replace literals in the formula with an integer greater than 2 (to
        keep 0 for False and 1 for True).
        If the literal is negative, the integer takes a negative value.
        """
        for clause in clauses:
            if not Clauses.is_clausal_form(clause):
                raise ValueError(f"{clauses} is not a proper clause")
        # clauses += Clauses.generate_modal_axioms(clauses)
        translation = Clauses._create_translation(clauses)
        clauses_as_int = [Clauses.str_to_int(clause, translation)
                          for clause in clauses]
        return cls(clauses_as_int, translation)

    @staticmethod
    def _create_translation(clauses: Collection[Collection[str]])\
            -> Dict[str, int]:
        _OFFSET = 2  # Offset to avoid adding 0 and 1 to the translation table.
        translation: Dict[str, int] = {}
        unique_propositions = Clauses.get_distinct_propositions(clauses)
        for index, value in enumerate(unique_propositions):
            translation[value] = index + _OFFSET
        return translation

    @staticmethod
    def generate_modal_axioms(clauses: List[List[str]]) \
            -> List[List[str]]:
        output: List[List[str]] = []
        propositions = Clauses.get_distinct_propositions(clauses)
        for f in propositions:
            # ☐f→f <=> ¬☐f∨f
            output.append([f, "☐", "¬", f])
            # ☐f→¬◇¬f <=> ¬☐f∨¬◇¬f
            output.append([f, "☐", "¬", f, "¬", "◇", "¬"])
            # ☐f→◇f <=> ¬☐f∨◇f
            output.append([f, "☐", "¬", f, "◇"])
        return output

    @staticmethod
    def str_to_int(clause: List[str], translation: Dict[str, int]) \
            -> Set[int]:
        """Replace literals in the formula with an integer corresponding
        to its position + 1 in the alphabet. If the literal is negative,
        the integer takes a negative value.

        1 is added to avoid the case of 0, which is problematic to work with
        (as -0 is the same as +0, and the sign will disappear).
        """
        output: List[int] = []
        for element in clause:
            if element == "¬":
                output[-1] *= -1
            elif element == "∨":
                continue
            else:
                if element not in translation:
                    raise ValueError(f"{element} was not found"
                                     f" in the translation table.")
                output.append(translation[element])
        return set(output)

    @staticmethod
    def is_clausal_form(formula: List[str]) -> bool:
        for element in formula:
            if len(element) == 0:
                raise ValueError(f"Empty clause encountered.")
            if not element[0].isalpha() and element not in ["∨", "¬"]:
                return False
        return True

    @staticmethod
    def is_mono_literal(clause: Set[int]) -> bool:
        """Return true if the argument is a mono-literal."""
        return len(clause) == 1

    def add_clause(self, clause: Set[int]) -> None:
        """Append the clause to the _clauses attribute."""
        self._clauses.append(clause)

    def unit_propagate(self, mono_literal: int) -> None:
        """Propagates the mono-literal in the whole formula.

        Remove all the clauses containing the mono-literal, and remove the
        negative value of the mono-literal from the clauses containing it.
        """
        for clause in self._clauses[:]:
            if mono_literal in clause:
                self._clauses.remove(clause)
            elif -mono_literal in clause:
                tmp = set(clause)
                tmp.remove(-mono_literal)
                self._clauses.remove(clause)
                self._clauses.append(tmp)

    def find_pure_literals(self) -> Set[int]:
        """Return a set containing every pure literal in the formula.

        A pure literal is a literal whose contrary doesn't exist
        in the formula.
        """
        literals_set = set(chain.from_iterable(self._clauses))
        return {literal for literal in literals_set
                if -literal not in literals_set}

    def assign_pure_literal(self, pure_literal: int) -> None:
        """Assign the pure literal passed as parameter.

        The returned object only contains clauses without the pure literal.
        """

        def filter_function(x): return pure_literal not in x

        self._clauses = list(filter(filter_function, self._clauses))

    def contains_only_mono_literals(self) -> bool:
        """Return True if the list contains only mono-literals."""
        multi_literals = list(filter(
            lambda x: not self.is_mono_literal(x), self._clauses
        ))
        return True if not multi_literals else False

    def find_mono_literals(self) -> Set[int]:
        """Return a Set containing every mono-literal."""
        return set(chain.from_iterable(
            filter(self.is_mono_literal, self._clauses)
        ))

    def is_consistant_set_of_literals(self) -> bool:
        """Return True if the list contains a consistent set of literals.

        A consistent set of literals is a set that doesn't contain a literal
        and its contrary.
        """
        flat_set = self.get_distinct_propositions(self._clauses)
        inconsistencies = {filter(lambda x: -x in flat_set, flat_set)}
        return False if inconsistencies else True

    def contains_empty_clause(self):
        """Return True if the list contains an empty clause."""
        return bool(list(filter(lambda x: not x, self._clauses)))

    T = TypeVar('T')
    @staticmethod
    def get_distinct_propositions(clauses: Collection[Collection[T]])\
            -> Set[T]:
        return set(filter(lambda x: not logic_parser.is_operator(x),
                          chain.from_iterable(clauses)))

    @property
    def clauses(self):
        return self._clauses

    @property
    def translation(self):
        return self._translation

    @property
    def literal_clauses(self):
        output = []
        for clause in self._clauses:
            current_clause = set()
            for proposition in clause:
                for key, value in self._translation.items():
                    if value == proposition:
                        current_clause.add(key)
                    elif -value == proposition:
                        current_clause.add(f"¬{key}")
            output.append(current_clause)
        return output
