from logic_formula_parser import parser, lexer
from logic_formula_parser.operators import *


def test_parse():
    data = 'a&b|c|-Hd&-[H]e|-L-a'
    actual_result = parser.parse(data)
    expected_result = Or(Or(Or(And(Proposition('a'),
                                   Proposition('b')),
                               Proposition('c')),
                            And(Not(H(Proposition('d'))),
                                Not(HBox(Proposition('e'))))),
                         Not(LNot(Proposition('a'))))
    assert expected_result == actual_result
