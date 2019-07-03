"""
SAT Solver reading clauses from file. It expects the clauses in conjunctive
normal form.
Based upon the DPLL algorithm.
"""

import pathlib
import random
from itertools import chain
from typing import *

from logic_parser import LogicParser
from clauses import Clauses


class SatSolver:
    """SAT Solver using the DPLL algorithm."""
    def __init__(self, clauses: Clauses) -> None:
        self.clauses = clauses

    @classmethod
    def from_file(cls, filename: str):
        """Create solver with the clauses from the file."""
        with open(filename) as f:
            clauses = frozenset(frozenset(LogicParser(line).clause)
                                for line in f if line[0] != "#")
        return cls(Clauses.from_int(clauses))

    def solve(self) -> Optional[Clauses]:
        """Return the solution if the formula is solvable."""
        return self._davis_putnam_algorithm(self.clauses)

    def _davis_putnam_algorithm(self, clauses: Clauses,
                                backtrack: Optional[Set[int]] = None)\
            -> Optional[Clauses]:
        """Return True if the clauses are solvable.

        Uses the DPLL algorithm to solve the formula under clausal form.
        """
        if backtrack is None:
            backtrack = set()

        if clauses.is_consistant_set_of_literals():
            return clauses
        if clauses.contains_empty_clause():
            return None
        mono_literals: FrozenSet[int] = clauses.find_mono_literals()
        while mono_literals:
            mono_literal = next(iter(mono_literals))
            backtrack.add(mono_literal)
            clauses = clauses.unit_propagate(mono_literal)
            mono_literals = clauses.find_mono_literals()

        pure_literals = clauses.find_pure_literals()
        while pure_literals:
            pure_literal = next(iter(pure_literals))
            backtrack.add(pure_literal)
            clauses = clauses.assign_pure_literal(pure_literal)
            pure_literals = clauses.find_pure_literals()

        propositions = list(chain.from_iterable(clauses.clauses))
        if not propositions and backtrack:
            return Clauses(frozenset(
                {frozenset({proposition}) for proposition in backtrack}
            ))
        next_literal = random.choice(propositions)
        positive = clauses.add_clause_to_copy(frozenset({next_literal}))
        negative = clauses.add_clause_to_copy(frozenset({-next_literal}))
        return (self._davis_putnam_algorithm(positive, backtrack)
                or self._davis_putnam_algorithm(negative, backtrack))


if __name__ == "__main__":
    sat_solver = SatSolver.from_file(
        f"{pathlib.Path(__file__).parent.parent}"
        "/tests/sat_solver/satisfiable_clauses.txt"
    )
    sat_solver.solve()
    logicParser = LogicParser(input("Please type in the formula : \n"))
    print(f"{logicParser.formatted_formula} => {logicParser.postfix_formula}")
