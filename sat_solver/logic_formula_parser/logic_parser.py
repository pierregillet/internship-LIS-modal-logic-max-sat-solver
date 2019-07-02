import string
from typing import *

FORMATTING_SUBSTITUTIONS: Dict[str, str] = {
    "[]": "☐",
    "<>": "◇",
    "->": "→",
    "-": "¬",
    "&": "∧",
    "|": "∨",
}

OPERATORS_BY_PRECEDENCE: Tuple[FrozenSet[str], ...] = (
    frozenset({"☐", "◇", "¬"}),
    frozenset({"∧", "∨"}),
    frozenset({"→"}),
)


class LogicParser:
    def __init__(self, formula,
                 formatting_substitutions: Dict[str, str] = None,
                 operators_by_precedence: Tuple[FrozenSet[str], ...] = None):
        self.formatting_substitutions: Dict[str, str]
        self.operators_by_precedence: Tuple[FrozenSet[str], ...]
        self._formula: str

        self.formatting_substitutions = (
            FORMATTING_SUBSTITUTIONS if formatting_substitutions is None
            else formatting_substitutions
        )
        self.operators_by_precedence = (
            OPERATORS_BY_PRECEDENCE if operators_by_precedence is None
            else operators_by_precedence
        )

        if len(formula) < 1:
            raise ValueError(f"Formula {formula} too short")

        formatted_formula: str = self._format(formula)

        if not self._is_syntactically_correct(formatted_formula):
            raise ValueError(
                f"Formula {formatted_formula} syntactically incorrect"
            )
        self._formula: str = formatted_formula

    def _split_formula_postfix(self) -> Tuple[str]:
        """Splits the formula to a list of postfixed operands and operators.

        Expects the formula to be syntactically correct and to start and end
        with parenthesis."""
        output: Tuple[str] = tuple()
        stack: List[str] = [self.formula[0]]
        iterator: Iterator[str] = iter(self.formula[1::])
        for char in iterator:  # type: str
            if self._is_operand(char):
                output += tuple([char])
            elif char == "(":
                stack.append(char)
            elif char == ")":
                while stack:
                    element = stack.pop()
                    if element == "(":
                        break
                    output += tuple([element])
            else:  # If an operator is encountered
                self._get_operator_weight(char)
                operator_found = char
                for operator in stack[::-1]:
                    if operator == "(":
                        break
                    elif (self._get_operator_weight(operator)
                          <= self._get_operator_weight(operator_found)):
                        output += tuple([stack.pop()])
                stack.append(operator_found)
        return output

    def _get_operator_weight(self, operator: str) -> int:
        """Return the weight (priority) of the operator.

        If the operator is unknown, raises a ValueError exception.
        """
        for weight, operators_set in enumerate(self.operators_by_precedence):
            if operator in operators_set:
                return weight
        raise ValueError(f"Operator {operator} unknown")

    def _is_syntactically_correct(self, formula: str) -> bool:
        """Return True if the formula is syntactically correct.

        If the operator is unknown, raises a ValueError exception.
        """
        if (len(formula) < 1
                or len(formula.replace(" ", "")) == 0
                or not self._are_parenthesis_consistent(formula)):
            return False
        for char in formula:
            if (not self._is_operand(char)
                    and char not in "()"
                    and char not in self.formatting_substitutions.keys()
                    and not self._is_operator(char)):
                return False
        return True

    @staticmethod
    def _is_operand(char: str) -> bool:
        """Return True of the string passed as parameter is an operand.

        An operand is an alpha character.
        """
        return char.isalpha()

    def _is_operator(self, char: str) -> bool:
        """Return True of the string passed as parameter is an operator.

        Operators are compared to a list stored as an attribute.
        """
        for operators in self.operators_by_precedence:
            if char in operators:
                return True
        return False

    @staticmethod
    def _are_parenthesis_consistent(formula: str) -> bool:
        """Return True if the parenthesis are consistent.

        Parenthesis are considered consistent iff :
        - there is an equal number of opening and closing parenthesis ;
        - there isn't a closing parenthesis before a corresponding opening
          parenthesis.
        """
        left_parenthesis: int = 0
        right_parenthesis: int = 0
        for char in formula:
            if char is "(":
                left_parenthesis += 1
            elif char is ")":
                right_parenthesis += 1
            if left_parenthesis < right_parenthesis:
                return False
        if left_parenthesis != right_parenthesis:
            return False
        else:
            return True

    def _format(self, formula: str) -> str:
        """

        :param formula:
        :return:
        """
        new_formula: str = formula[::].strip("\n")
        for key, value in self.formatting_substitutions.items():
            new_formula = new_formula.replace(key, value)
        if new_formula[0] != "(" or new_formula[-1:] != ")":
            new_formula = f"({new_formula})"
        return new_formula

    @property
    def formula(self) -> str:
        return self._formula

    @property
    def postfix_formula(self) -> Tuple[str]:
        return self._split_formula_postfix()

    @property
    def clause(self) -> FrozenSet[int]:
        # return frozenset(operand for operand in self._split_formula_postfix()
        #                  if self._is_operand(operand) or operand == "¬")
        return self.as_integers(self.postfix_formula)

    @staticmethod
    def as_integers(clause: Tuple[str, ...]) -> FrozenSet[int]:
        """ Replace literals in each clause with an integer corresponding
        to its position + 1 in the alphabet. If the literal is negative,
        the integer takes a negative value.

        1 is added to avoid the case of 0, which is problematic to work with
        (-0 is the same as +0, and the sign will disappear).
        """
        output: List[int] = []
        for char in clause:
            if char.isalpha():
                output.append(string.ascii_letters.index(char) + 1)
            elif char == "¬":
                output[-1] *= -1
        return frozenset(output)


if __name__ == "__main__":
    while True:
        logicParser = LogicParser(input("Please type in the formula : \n"))
        print(logicParser.formula)
        print(logicParser.postfix_formula)
