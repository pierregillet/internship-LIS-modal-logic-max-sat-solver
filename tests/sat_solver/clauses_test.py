import pytest

from sat_solver.clauses import Clauses, _get_leaves, _get_propositions,\
    _is_mono_literal
from logic_formula_parser.operators import *


class TestClauses:
    def test__from_literal_formulas(self):
        literal_formulas = [
            Or(Proposition('a'), Proposition('b')),
            Or(Proposition('a'), Proposition('c')),
            Or(Proposition('d'), Proposition('e')),
            Or(Proposition('d'), Proposition('f')),
            Or(Proposition('g'), Proposition('h')),
            Or(Not(Proposition('g')), Proposition('i')),
            Or(Not(Proposition('g')), Proposition('j')),
            Proposition('e'),
            Proposition('g'),
        ]
        clauses = Clauses.from_literal_formulas(literal_formulas)
        keys = clauses.translation.keys()

    def test__get_leaves(self):
        # a∨b
        formula = Or(Proposition('a'), Proposition('b'))
        leaves = _get_leaves(formula)
        actual_leaves = {Proposition('a'), Proposition('b')}
        assert leaves == actual_leaves

        # ¬Hd∨¬L¬a∨¬d∧¬d
        formula = Or(Or(Not(H(Proposition('d'))),
                        Not(LNot(Proposition('a')))),
                     And(Not(Proposition('d')), Not(Proposition('d'))))
        leaves = _get_leaves(formula)
        actual_leaves = {H(Proposition('d')),
                         LNot(Proposition('a')),
                         Proposition('d')}
        assert leaves == actual_leaves

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

    def test_is_mono_literal(self):
        multi_literal = {-1, -3, -1}
        assert _is_mono_literal(multi_literal) is False
        mono_literal = {-1}
        assert _is_mono_literal(mono_literal) is True

    def test__unit_propagate(self):
        clauses = Clauses([
            {1, 2},
            {-1, -2},
            {2, 3, 4},
            {-1, -3},
        ])
        expected = [{-3, -1}, {-1}]
        clauses.unit_propagate(2)
        assert clauses.clauses == expected

    def test__find_pure_literals(self):
        clauses = Clauses([
            {-1, -3},
            {-2, 1, 5},
            set(),
            {-1},
        ])
        pure_literals = {-2, -3, 5}
        assert clauses.find_pure_literals() == pure_literals

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
