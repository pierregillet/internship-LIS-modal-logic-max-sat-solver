"""
SAT Solver reading formulas from file.
Based upon the Davis & Putnam algorithm.
"""

import pathlib
from typing import *

from logic_formula_parser.logic_parser import LogicParser
from clauses_utils import find_mono_literals, is_consistant_set_of_literals,\
                          is_mono_literal, contains_only_mono_literals

class SatSolver:
    def __init__(self, filename: str) -> None:
        self.filename: str = filename

    def solve(self) -> bool:
        clauses: List[List[str]] = self._get_formatted_clauses_from_file()
        return self._davis_putnam_algorithm(clauses)

    def _davis_putnam_algorithm(self, clauses: List[List[str]]) -> bool:
        remaining_clauses = clauses[:]
        # while remaining_clauses and :

        if contains_only_mono_literals(clauses):
            mono_literals: List[List[str]] = find_mono_literals(clauses)
        return False

    def _get_formatted_clauses_from_file(self) -> List[List[str]]:
        with open(self.filename) as f:
            return [LogicParser(line).postfix_formula for line in f]


if __name__ == "__main__":
    sat_solver = SatSolver(
        f"{pathlib.Path(__file__).parent}/satisfiable_clauses.txt"
    )
    sat_solver.solve()
    logicParser = LogicParser(input("Please type in the formula : \n"))
    print(f"{logicParser.formula} => {logicParser.postfix_formula}")
