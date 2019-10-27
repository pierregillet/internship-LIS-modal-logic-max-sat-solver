"""
SAT Solver reading clauses from file. It expects the clauses in conjunctive
normal form.
Based upon the DPLL algorithm.
"""
import re
from copy import copy, deepcopy
import pathlib
import random
from itertools import chain
from typing import *

from logic_formula_parser import parser
from sat_solver.clauses import Clauses


class DpllSatSolver:
    """SAT Solver using the DPLL algorithm."""

    def __init__(self, clauses: Clauses) -> None:
        self.clauses = clauses

    def solve(self) -> Optional[Clauses]:
        """Return the solution if the formula is solvable."""
        return self._davis_putnam_algorithm(deepcopy(self.clauses))

    def _davis_putnam_algorithm(self, clauses: Clauses,
                                backtrack: Optional[Set[int]] = None) \
            -> Optional[Clauses]:
        """Return True if the clauses are solvable.

        Uses the DPLL algorithm to solve the formula under clausal form.
        """
        # TODO: Make recursion a terminal recursion (no context to remember).
        #       It will give marginally but consistently better performance.
        if backtrack is None:
            backtrack = set()

        if clauses.is_consistant_set_of_literals():
            return clauses
        if clauses.contains_empty_clause():
            return None

        while True:
            mono_literals: Set[int] = clauses.find_mono_literals()
            if not mono_literals:
                break
            for mono_literal in mono_literals:
                backtrack.add(mono_literal)
                clauses.unit_propagate(mono_literal)

        while True:
            pure_literals = clauses.find_pure_literals()
            if not pure_literals:
                break
            for pure_literal in pure_literals:
                backtrack.add(pure_literal)
                clauses.assign_pure_literal(pure_literal)

        propositions = list(chain.from_iterable(clauses.clauses))
        if not propositions and backtrack:
            return Clauses([{proposition} for proposition in backtrack],
                           clauses.translation)
        next_literal = random.choice(propositions)
        positive = copy(clauses)
        positive.add_clause({next_literal})
        negative = copy(clauses)
        negative.add_clause({-next_literal})
        positive_solution = self._davis_putnam_algorithm(positive, backtrack)
        if positive_solution:
            return positive_solution
        else:
            # Negative solution
            return self._davis_putnam_algorithm(negative, backtrack)


if __name__ == "__main__":
    sat_solver = DpllSatSolver(Clauses.from_file(
        f"{pathlib.Path(__file__).parent.parent}/clauses_input.txt"
    ))
    solution = sat_solver.solve()
    if solution:
        print(solution.clauses)
        print(solution)
    else:
        print("No solution.")
