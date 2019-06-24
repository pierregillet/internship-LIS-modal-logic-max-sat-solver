"""
SAT Solver reading clauses from file. It expects the clauses in conjunctive
normal form.
Based upon the DPLL algorithm.
"""

import pathlib
from copy import copy
from typing import *

from logic_formula_parser.logic_parser import LogicParser
from clauses import Clauses


class SatSolver:
    """SAT Solver using the Davis & Putnam algorithm."""
    def __init__(self, filename: str) -> None:
        self.filename: str = filename

    def solve(self) -> bool:
        """Return True if the the clauses in the file are solvable."""
        clauses: Clauses = Clauses(self._get_formatted_clauses_from_file())
        return self._davis_putnam_algorithm(clauses)

    def _davis_putnam_algorithm(self, clauses: Clauses) -> bool:
        """Return True if the clauses are solvable."""
        # remaining_clauses = copy(clauses)
        if clauses.is_consistant_set_of_literals():
            return True
        if clauses.contains_empty_clause():
            return False
        mono_literals: FrozenSet[int] = clauses.find_mono_literals()
        while mono_literals:
            clauses = self._unit_propagate(clauses, mono_literals[0])
            mono_literals = clauses.find_mono_literals()

        pure_literals = self._find_pure_literals(remaining_clauses)

        # if contains_only_mono_literals(clauses):
        #     mono_literals: List[List[str]] = find_mono_literals(clauses)
        return False

    @staticmethod
    def _unit_propagate(clauses: List[List[str]],
                        mono_literal: List[str]) -> List[List[str]]:

        return clauses

    @staticmethod
    def _find_pure_literals(clauses: List[List[int]]) -> Set[int]:
        literals_set = {literal for clause in clauses for literal in clause}
        return {literal for literal in literals_set
                if -literal not in literals_set}

    def _get_formatted_clauses_from_file(self) -> FrozenSet[Tuple[str]]:
        with open(self.filename) as f:
            return frozenset(LogicParser(line).postfix_formula for line in f)


if __name__ == "__main__":
    sat_solver = SatSolver(
        f"{pathlib.Path(__file__).parent.parent}"
        "/tests/sat_solver/satisfiable_clauses.txt"
    )
    sat_solver.solve()
    logicParser = LogicParser(input("Please type in the formula : \n"))
    print(f"{logicParser.formula} => {logicParser.postfix_formula}")
