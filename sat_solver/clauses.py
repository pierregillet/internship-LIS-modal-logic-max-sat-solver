"""
Verifications and manipulations of the clauses such as unit propagation
or mono-literal checks.
"""

from __future__ import annotations

import re
from itertools import chain
from typing import *

from logic_formula_parser.operators import *  # as op
from logic_formula_parser import parser


class Clauses:
    """Class containing a set of clauses in conjunctive normal form."""

    def __init__(self, clauses: List[Set[int]],
                 translation: Dict[Leaf, int] = None):
        """Construct an object from clauses with propositions as integers.
        Each clause must be its own list element (they must already be split).
        """
        self._clauses: List[Set[int]] = clauses
        self._translation: Dict[Leaf, int] = translation

    @classmethod
    def from_file(cls, filename: str):
        """Create the clauses from the file."""
        # TODO: Refactor this classmethod ; the comments syntax
        #       should be handled by the parser instead (in the grammar).
        clauses = []
        with open(filename) as f:
            for line in f:
                stripped_line = line.strip()
                if stripped_line is None or re .match(r'^#.*', stripped_line):
                    continue
                parsed_line = parser.parse(stripped_line)
                if parsed_line is not None:
                    clauses.append(parsed_line)
        return Clauses.from_literal_formulas(clauses)

    @classmethod
    def from_literal_formulas(cls, formulas: List[Formula]) -> Clauses:
        """Create an instance of this class from clauses with propositions
        as strings. They will be replaced with integers.

        Replace literals in the formula with an integer greater than 2 (to
        keep 0 for False and 1 for True).
        If the literal is negative, the integer takes a negative value.
        """
        modal_formulas = generate_modal_axioms(formulas)
        clauses, translation = _convert_to_int(formulas + modal_formulas)
        return cls(clauses, translation)

    def __copy__(self):
        """Create a shallow copy."""
        return Clauses(self._clauses[:], self.translation.copy())

    def __eq__(self, other: Clauses):
        return self.clauses == other.clauses

    def __str__(self) -> str:
        def translate(number: int) -> Leaf:
            for leaf, value in self._translation.items():
                if value == number:
                    return leaf
                elif value == -number:
                    return Not(leaf)

        output = ""
        for clause in self._clauses:
            for index, proposition in enumerate(clause):
                if index > 0:
                    output += '∨'
                output += str(translate(proposition))
            output += '\n'
        return str(output)

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
            lambda x: not _is_mono_literal(x), self._clauses
        ))
        return True if not multi_literals else False

    def find_mono_literals(self) -> Set[int]:
        """Return a Set containing every mono-literal."""
        return set(chain.from_iterable(
            filter(_is_mono_literal, self._clauses)
        ))

    def is_consistant_set_of_literals(self) -> bool:
        """Return True if the list contains a consistent set of literals.

        A consistent set of literals is a set that doesn't contain a literal
        and its contrary.
        """
        flat_set = self.get_distinct_propositions()
        inconsistencies = {filter(lambda x: -x in flat_set, flat_set)}
        return False if inconsistencies else True

    def contains_empty_clause(self):
        """Return True if the list contains an empty clause."""
        return bool(list(filter(lambda x: not x, self._clauses)))

    def get_distinct_propositions(self) -> Set[int]:
        return set(filter(lambda x: not isinstance(x, Operator),
                          chain.from_iterable(self._clauses)))

    @property
    def clauses(self):
        return self._clauses

    @property
    def translation(self):
        return self._translation


def generate_modal_axioms(formulas: Collection[Formula]) -> List[Formula]:
    output: List[Formula] = []
    propositions = _get_propositions(formulas)
    # for f in propositions:
    #     # ☐f→f <=> ¬☐f∨f
    #     output.append(
    #         Or(Proposition(f),
    #            Not(Box(Proposition(f))))
    #     )
    #     # ☐f→¬◇¬f <=> ¬☐f∨¬◇¬f
    #     output.append(
    #         Or(Not(Box(Proposition(f))),
    #            Not(DiamondNot(Proposition(f))))
    #     )
    #     # ☐f→◇f <=> ¬ ☐f∨◇f
    #     output.append(
    #         Or(Not(Box(Proposition(f))),
    #            Diamond(Proposition(f)))
    #     )
    return output


def _is_clausal_form(formula: List[str]) -> bool:
    raise RuntimeError("Not yet implemented.")
    # for element in formula:
    #     if len(element) == 0:
    #         raise ValueError(f"Empty clause encountered.")
    #     if not element[0].isalpha() and element not in ["∨", "¬"]:
    #         return False
    # return True


def _convert_to_int(formulas: Collection[Formula]) \
        -> Tuple[List[Set[int]], Dict[Leaf, int]]:
    translation = _create_translation(formulas)
    output = []
    for formula in formulas:
        # TODO: Check if the input is not in clausal form
        # if not _is_clausal_form(formula):
        #     raise ValueError('Formula is not in clausal form.')
        leaves = _get_leaves(formula)
        output.append(set(translation[leaf] for leaf in leaves))
    return output, translation


def _create_translation(clauses: Collection[Formula]) -> Dict[Leaf, int]:
    _OFFSET = 2  # Offset to avoid adding 0 and 1 to the translation table.
    translation: Dict[Leaf, int] = {}
    unique_propositions = set()
    # for clause in clauses:
    #     unique_propositions |= _get_literals(clause)
    unique_propositions: Set[Proposition] = _get_literals(clauses)
    for index, variable in enumerate(unique_propositions):
        translation[variable] = index + _OFFSET
        translation[Not(variable)] = -index - _OFFSET
    return translation


def _get_literals(formulas: Collection[Formula]) -> Set[Proposition]:
    """Return a set containing the literals found in the tree.
    """

    def recursively_search(formula: Formula) -> Set[Proposition]:
        if isinstance(formula, Proposition):
            return {formula}
        elif formula is not None:
            leaves: Set[Leaf] = set()
            for child in formula.children:
                if child is not None:
                    leaves |= recursively_search(child)
            return leaves

    output = set()
    for formula in formulas:
        output |= recursively_search(formula)
    return output


def _get_propositions(formulas: Collection[Formula]) -> Set[Proposition]:
    """Return a set containing the individual propositions found in the tree.
    """

    def recursively_search(formula: Formula) -> Set[Proposition]:
        if _is_leaf(formula):
            return {formula}
        elif formula is not None:
            leaves: Set[Leaf] = set()
            for child in formula.children:
                if child is not None:
                    leaves |= recursively_search(child)
            return leaves

    output = set()
    for formula in formulas:
        output |= recursively_search(formula)
    return output


def _get_leaves(formula: Formula) -> Set[Leaf]:
    """Return a set of leaves of the tree. This includes propositions and
    negative propositions such as Not(Proposition('a')).
    """
    if _is_leaf(formula):
        return {formula}
    leaves: Set[Leaf] = set()
    for child in formula.children:
        if child is not None:  # and not isinstance(child, Proposition):
            leaves |= {child} if _is_leaf(child) else _get_leaves(child)
    return leaves


def _is_leaf(element: Leaf) -> bool:
    """Return True if the element is a leaf, i.e. either a proposition or a
    negative proposition such as Not(Proposition('a')).
    """
    if isinstance(element, Proposition):
        return True
    elif isinstance(element, Not) \
            and isinstance(element.children[1], Proposition):
        return True
    elif element.children[0] is None \
            and isinstance(element.children[1], Proposition):
        return True
    else:
        return False


def _is_mono_literal(clause: Set[int]) -> bool:
    """Return true if the argument is a mono-literal."""
    return len(clause) == 1
