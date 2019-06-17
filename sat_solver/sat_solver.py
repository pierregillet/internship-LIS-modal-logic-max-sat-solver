
from typing import *

from logic_formula_parser import LogicParser


class SatSolver:
    def __init__(self, filename: str) -> None:
        self.filename: str = filename

    def read_file(self) -> Generator[str, None, None]:
        with open(self.filename) as f:
            for line in f:
                yield f.readline()


while True:
    logicParser = LogicParser(input("Please type in the formula : \n"))
    print(f"{logicParser.formula} => {logicParser.postfix_formula}")
