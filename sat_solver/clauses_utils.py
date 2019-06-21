"""
Lists and strings manipulations for clauses such as integer substitutions
and mono-literal checks.
"""

from typing import *
import string


def is_mono_literal(clause: List[str]) -> bool:
    """Return true if the argument is a mono-literal."""
    return len(clause) == 1 and clause[0].isalpha()


def contains_only_mono_literals(clauses: List[List[str]]) -> bool:
    """Return True if the list contains only mono-literals."""
    return True if [clause for clause in clauses
                    if not is_mono_literal(clause)] else False


def find_mono_literals(clauses: List[List[str]]) -> List[List[str]]:
    """Return a list of every mono-literal."""
    return [clause for clause in clauses if is_mono_literal(clause)]


def is_consistant_set_of_literals(clauses: List[List[str]]) -> bool:
    """Return True if the list contains a consistent set of literals.

    A consistent set of literals is a set that doesn't contain a literal
    and its contrary.
    """
    return False if [clause for clause in clauses
                    if not is_mono_literal(clause)] else True


def convert_literals_to_integers(clauses: List[List[str]]):
    """ Replace literals in each clause with an integer corresponding
    to its position + 1 in the alphabet. If the literal is negative,
    the integer takes a negative value.

    1 is added to avoid the case of 0, which is problematic to work with
    (-0 is the same as +0, and the sign will disappear).
    """
    output: List[List[str]] = []
    for formula in clauses:
        for char in formula:
            if char.isalpha():
                output.append(string.ascii_letters.index(char) + 1)
            elif char == "¬":
                output[-1] *= -1
