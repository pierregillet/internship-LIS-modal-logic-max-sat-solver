from unittest import TestCase

from sat_solver.logic_formula_parser.logic_parser\
    import LogicParser, OPERATORS_BY_PRECEDENCE


class TestLogicParser(TestCase):
    def test__is_syntactically_correct(self):
        incorrect_formulas = ["(aab", "a&¬b)", ")", "(", "(", " ", "())((¬)", "", ]
        correct_formulas = ["(aab)", "()", "¬a∧(b∨¬c)", "(((a∨(¬b))))", "((a)∧(¬b))∨((c)∨◇b)", ]
        for formula in incorrect_formulas:
            with self.subTest(formula=formula), self.assertRaises(ValueError):
                LogicParser(formula)
        for formula in correct_formulas:
            with self.subTest(formula=formula):
                self.assertIsInstance(LogicParser(formula), LogicParser)

    def test_get_operator_weight(self):
        incorrect_operators = ["(aab", "a∧¬b)", ")", "(", "(", " ", "())((¬)", "", "<", ">", "><", "][", "¬<"]
        logic_parser = LogicParser("abcd")
        for operator in incorrect_operators:
            with (self.subTest(operator=operator)
                  and self.assertRaises(ValueError)):
                logic_parser._get_operator_weight(operator)
        for operator_set in OPERATORS_BY_PRECEDENCE:
            for operator in operator_set:
                with self.subTest(operator=operator):
                    self.assertGreaterEqual(
                        logic_parser._get_operator_weight(operator), 0
                    )
        self.assertEqual(logic_parser._get_operator_weight("◇"), 0)
        self.assertEqual(logic_parser._get_operator_weight("☐"), 0)
        self.assertEqual(logic_parser._get_operator_weight("¬"), 0)
        self.assertEqual(logic_parser._get_operator_weight("∧"), 1)
        self.assertEqual(logic_parser._get_operator_weight("∨"), 1)
        self.assertEqual(logic_parser._get_operator_weight("→"), 2)

    def test__split_formula_postfix(self):
        split_formula = {
            "(a∧b)": ["a", "b", "∧"],
            "(a∧(b|c))": ["a", "b", "c", "∨", "∧"],
            "((b|c)∧a)": ["b", "c", "∨", "a", "∧"],
            "((b|c)∧a->(d|c))": ["b", "c", "∨", "a", "∧", "d", "c", "∨", "→"],
        }
        for key, value in split_formula.items():
            logic_parser = LogicParser(key)
            self.assertEqual(logic_parser._split_formula_postfix(), value)
