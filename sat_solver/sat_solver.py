"""
SAT Solver reading clauses from file. It expects the clauses in conjunctive
normal form.
Based upon the DPLL algorithm.
"""

import pathlib
from typing import *

from logic_formula_parser.logic_parser import LogicParser
from clauses import Clauses


class SatSolver:
    """SAT Solver using the Davis & Putnam algorithm."""
    def __init__(self, clauses: Clauses) -> None:
        self.clauses = clauses

    @classmethod
    def from_file(cls, filename: str):
        return cls(cls._get_clauses_from_file(filename))

    def solve(self) -> bool:
        """Return True if the the clauses stored as attribute are solvable."""
        return self._davis_putnam_algorithm(self.clauses)

    def _davis_putnam_algorithm(self, clauses: Clauses) -> bool:
        """Return True if the clauses are solvable."""
        # remaining_clauses = copy(clauses)
        if clauses.is_consistant_set_of_literals():
            return True
        if clauses.contains_empty_clause():
            return False
        mono_literals: FrozenSet[int] = clauses.find_mono_literals()
        while mono_literals:
            clauses = self._unit_propagate(clauses, next(iter(mono_literals)))
            mono_literals = clauses.find_mono_literals()

        pure_literals = self._find_pure_literals(clauses)

        return False

    @staticmethod
    def _find_pure_literals(clauses: Clauses) -> Set[int]:
        literals_set = {
            literal for clause in clauses.clauses for literal in clause
        }
        return {literal for literal in literals_set
                if -literal not in literals_set}

    @staticmethod
    def _get_clauses_from_file(filename: str) -> Clauses:
        with open(filename) as f:
            clauses = frozenset(frozenset(LogicParser(line).clause) for line in f)
        return Clauses.from_int(clauses)


if __name__ == "__main__":
    sat_solver = SatSolver.from_file(
        f"{pathlib.Path(__file__).parent.parent}"
        "/tests/sat_solver/satisfiable_clauses.txt"
    )
    sat_solver.solve()
    logicParser = LogicParser(input("Please type in the formula : \n"))
    print(f"{logicParser.formula} => {logicParser.postfix_formula}")
