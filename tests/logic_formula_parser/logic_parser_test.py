import pytest

from logic_formula_parser import logic_parser


class TestLogicParser:
    def test__is_syntactically_correct(self):
        incorrect_formulas = ["(aab", "a&¬b)", ")", "(", "(", " ", "())((¬)",
                              "", ]
        correct_formulas = ["(aab)", "()", "¬a∧(b∨¬c)", "(((a∨(¬b))))",
                            "((a)∧(¬b))∨((c)∨◇b)", ]
        for formula in incorrect_formulas:
            with pytest.raises(ValueError):
                logic_parser.parse_formula(formula)
        for formula in correct_formulas:
            assert isinstance(logic_parser.parse_formula(formula), list)

    def test_get_operator_weight(self):
        incorrect_operators = ["(aab", "a∧¬b)", ")", "(", "(", " ", "())((¬)",
                               "", "<", ">", "><", "][", "¬<"]
        for operator in incorrect_operators:
            with pytest.raises(ValueError):
                logic_parser._get_operator_weight(operator)
        for operator_set in logic_parser.OPERATORS_BY_PRECEDENCE:
            for operator in operator_set:
                assert logic_parser._get_operator_weight(operator) >= 0
        assert logic_parser._get_operator_weight("◇") == 0
        assert logic_parser._get_operator_weight("☐") == 0
        assert logic_parser._get_operator_weight("¬") == 0
        assert logic_parser._get_operator_weight("∧") == 1
        assert logic_parser._get_operator_weight("∨") == 1
        assert logic_parser._get_operator_weight("→") == 2

    def test__split_formula_postfix(self):
        split_formula = {
            "(a∧b)": ["a", "b", "∧"],
            "(a∧(b∨c))": ["a", "b", "c", "∨", "∧"],
            "((b∨c)∧a)": ["b", "c", "∨", "a", "∧"],
            "((b∨c)∧a→(d∨c))": ["b", "c", "∨", "a", "∧", "d", "c", "∨", "→"],
        }
        for key, value in split_formula.items():
            assert logic_parser._split_formula_postfix(key) == value
