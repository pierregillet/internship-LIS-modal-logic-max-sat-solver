"""
SAT Solver reading formulas from file.
Based upon the Davis & Putnam algorithm.
"""

from typing import *

from logic_formula_parser import LogicParser


class SatSolver:
    def __init__(self, filename: str) -> None:
        self.filename: str = filename

    def solve(self) -> bool:
        clauses: List[List[str]] = self._get_formatted_clauses_from_file()
        return False

    def _get_formatted_clauses_from_file(self) -> List[List[str]]:
        with open(self.filename) as f:
            return [LogicParser(line).postfix_formula for line in f]

    def _find_mono_literals(self, clauses: List[List[str]]) -> List[List[str]]:
        return [clause for clause in clauses if len(clause) == 1]


if __name__ == "__main__":
    while True:
        logicParser = LogicParser(input("Please type in the formula : \n"))
        print(f"{logicParser.formula} => {logicParser.postfix_formula}")
