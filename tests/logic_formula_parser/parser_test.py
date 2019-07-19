from logic_formula_parser import parser, lexer
from logic_formula_parser.operators import *


def test_tokenize():
    data = 'a&b|c|-d&-[]e|-<>-a'
    actual_result = parser.parse(data)
    expected_result = Or(Or(Or(And(Proposition('a'),
                                   Proposition('b')),
                               Proposition('c')),
                            And(Not(Proposition('d')),
                                Not(Box(Proposition('e'))))),
                         Not(DiamondNot(Proposition('a'))))
    assert expected_result == actual_result
