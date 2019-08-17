import pytest

from sat_solver.clauses import Clauses, _get_leaves, _get_propositions
from logic_formula_parser.operators import *


class TestClauses:
#     def test__is_leaf(self):
#         # a∨b
#         formula = Or(Proposition('a'), Proposition('b'))
#         leaves = _get_leaves(formula)
#         actual_leaves = {Proposition('a'), Proposition('b')}
#         assert leaves == actual_leaves
#
#         # ¬◇d∨¬☐¬a∨d
#         formula = Or(Or(Not(Diamond(Proposition('d'))),
#                         Not(BoxNot(Proposition('a')))),
#                      Proposition('d'))
#         leaves = _get_leaves(formula)
#         actual_leaves = {Not(Diamond(Proposition('d'))),
#                          Not(BoxNot(Proposition('a'))),
#                          Proposition('d')}
#         assert leaves == actual_leaves
#
    def test__get_propositions(self):
        # ¬[H]d∨¬H¬a∨d
        # ¬Le∨[H]a∨¬b
        formulas = [
            Or(Or(Not(HBox(Proposition('d'))),
                  Not(HNot(Proposition('a')))),
               Proposition('d')),
            Or(Or(Not(L(Proposition('e'))),
                  HBox(Proposition('a'))),
               Not(Proposition('b'))),
        ]
        propositions = _get_propositions(formulas)
        actual_propositions = {Proposition('a'), Proposition('b'),
                               Proposition('d'), Proposition('e')}
        assert propositions == actual_propositions

#     def test_is_mono_literal(self):
#         multi_literal = {-1, -3, -1}
#         assert Clauses.is_mono_literal(multi_literal) is False
#         mono_literal = {-1}
#         assert Clauses.is_mono_literal(mono_literal) is True
#
#     def test__unit_propagate(self):
#         clauses = Clauses.from_int([
#             {1, 2},
#             {-1, -2},
#             {2, 3, 4},
#             {-1, -3},
#         ])
#         expected = [{-3, -1}, {-1}]
#         clauses.unit_propagate(2)
#         assert clauses.clauses == expected
#
#     def test_contains_only_mono_literals(self):
#         multi_literal = {-1, -3, -1}
#         assert Clauses.is_mono_literal(multi_literal) is False
#         mono_literal = {-1}
#         assert Clauses.is_mono_literal(mono_literal) is True
#
#     def test__find_pure_literals(self):
#         clauses = Clauses.from_int([
#             {-1, -3},
#             {-2, 1, 5},
#             set(),
#             {-1},
#         ])
#         pure_literals = {-2, -3, 5}
#         assert clauses.find_pure_literals() == pure_literals
#
#     @pytest.mark.skip(reason="Not yet implemented")
#     def test_find_mono_literals(self):
#         assert False
#
#     @pytest.mark.skip(reason="Not yet implemented")
#     def test_is_consistant_set_of_literals(self):
#         assert False
#
#     @pytest.mark.skip(reason="Not yet implemented")
#     def test_convert_literals_to_integers(self):
#         assert False
#
#     @pytest.mark.skip(reason="Not yet implemented")
#     def test_contains_empty_clause(self):
#         assert False
