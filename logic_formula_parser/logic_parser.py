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


def yield_parsed_formulas_from_file(filename: str) \
        -> Generator[List[str], None, None]:
    """Parse and then yield each formula one by one from the file."""
    with open(filename) as f:
        for line in f:
            if line[0] != "#":
                yield parse_formula(line)


def parse_formula(formula: str) -> List[str]:
    formatted_formula = _format(formula)
    if not _is_syntactically_correct(formatted_formula):
        raise ValueError(
            f"Formula {formatted_formula} syntactically incorrect"
        )
    return _split_formula_postfix(formatted_formula)


def _format(formula: str) -> str:
    """Format the formula for further processing.

    Remove the newline characters, replace composite operators passed as
    input with their unicode character, surround the formula with
    parenthesis if it isn't already the case.
    """
    if len(formula) < 1:
        raise ValueError(f"Formula '{formula}' is too short")
    new_formula: str = formula[::].strip("\n")
    for key, value in FORMATTING_SUBSTITUTIONS.items():
        new_formula = new_formula.replace(key, value)
    if new_formula[0] != "(" or new_formula[-1:] != ")":
        new_formula = f"({new_formula})"
    return new_formula


def _split_formula_postfix(formula: str) -> List[str]:
    """Splits the formula to a list of postfixed operands and operators.

    Expects the formula to be syntactically correct and to start and end
    with parenthesis."""
    output: List[str] = []
    stack: List[str] = [formula[0]]
    iterator: Iterator[str] = iter(formula[1::])
    for char in iterator:  # type: str
        if is_operand(char):
            output.append(char)
        elif char == "(":
            stack.append(char)
        elif char == ")":
            while stack:
                element = stack.pop()
                if element == "(":
                    break
                output.append(element)
        else:  # If an operator is encountered
            _get_operator_weight(char)
            operator_found = char
            for operator in stack[::-1]:
                if operator == "(":
                    break
                elif (_get_operator_weight(operator)
                      <= _get_operator_weight(operator_found)):
                    output.append(stack.pop())
            stack.append(operator_found)
    return output


def _is_syntactically_correct(formula: str) -> bool:
    """Return True if the formula is syntactically correct.

    If the operator is unknown, raises a ValueError exception.
    """
    if (len(formula) < 1
            or len(formula.replace(" ", "")) == 0
            or not are_parenthesis_consistent(formula)):
        return False
    for char in formula:
        if (not is_operand(char)
                and char not in "()"
                and char not in FORMATTING_SUBSTITUTIONS.keys()
                and not is_operator(char)):
            return False
    return True


def _get_operator_weight(operator: str) -> int:
    """Return the weight (priority) of the operator.

    If the operator is unknown, raises a ValueError exception.
    """
    for weight, operators_set in enumerate(OPERATORS_BY_PRECEDENCE):
        if operator in operators_set:
            return weight
    raise ValueError(f"Operator {operator} unknown")


def is_operand(char: str) -> bool:
    """Return True of the string passed as parameter is an operand.

    An operand is an alpha character.
    """
    return char.isalpha()


def is_operator(char: str) -> bool:
    """Return True of the string passed as parameter is an operator.

    Operators are compared to a list stored as an attribute.
    """
    for operators in OPERATORS_BY_PRECEDENCE:
        if char in operators:
            return True
    return False


def are_parenthesis_consistent(formula: str) -> bool:
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


if __name__ == "__main__":
    while True:
        input_formula = input("Please type in the formula to parse : \n")
        print(f"Postfix form : {parse_formula(input_formula)}")
